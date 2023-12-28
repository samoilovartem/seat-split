import re
import warnings

warnings.filterwarnings('ignore', category=SyntaxWarning)  # noqa: E402

from datetime import UTC, datetime, timedelta  # noqa: E402

from ghapi.core import GhApi  # noqa: E402
from loguru import logger  # noqa: E402


class GitHubIssuesReporter:
    """Fetches closed issues from GitHub and generates a report."""

    def __init__(self, access_token: str):
        self.api = GhApi(token=access_token, owner='lewanddowski')
        self.end_date = datetime.now(UTC)
        self.start_date = self.end_date - timedelta(days=7)
        self.issue_title_pattern = r'\[.+\] .+'

    def fetch_closed_issues(self, repo_name: str):
        issues = self.api.issues.list_for_repo(
            repo=repo_name, state='closed', since=self.start_date
        )
        valid_issues = []

        logger.info(
            'Fetching closed issues from GitHub from {} to {}',
            self.start_date,
            self.end_date,
        )

        for issue in issues:
            if (
                issue.get('closed_at')
                and self.start_date
                <= datetime.strptime(
                    issue.get('closed_at'), '%Y-%m-%dT%H:%M:%SZ'
                ).replace(tzinfo=UTC)
                <= self.end_date
            ):
                valid_issues.append(issue)

        return valid_issues

    def generate_report(self, repo_names: list[str]):
        issues_by_user = {}

        for repo_name in repo_names:
            issues = self.fetch_closed_issues(repo_name)
            for issue in issues:
                if not re.match(self.issue_title_pattern, issue.get('title')):
                    continue

                labels = issue.get('labels')
                label_info = [
                    {'name': label['name'], 'color': label['color']} for label in labels
                ]

                issue_info = {
                    'title': issue.get('title'),
                    'html_url': issue.get('html_url'),
                    'labels': label_info,
                }

                assignees = [
                    assignee.get('login') for assignee in issue.get('assignees', [])
                ]
                for assignee in assignees:
                    issues_by_user.setdefault(assignee, []).append(issue_info)

        return issues_by_user

    def format_slack_message(self, issues_by_user: dict[str, list[dict]]) -> dict:
        """
        Formats the issues report as a Slack message.
        """
        blocks = [
            {
                'type': 'header',
                'text': {'type': 'plain_text', 'text': 'Weekly GitHub Issues Report'},
            },
            {'type': 'divider'},
        ]

        for user, issues in issues_by_user.items():
            user_section = {
                'type': 'section',
                'text': {'type': 'mrkdwn', 'text': f'*{user}:*'},  # noqa: E231
            }
            blocks.append(user_section)

            for issue in issues:
                issue_title = issue['title']
                issue_url = issue['html_url']
                issue_labels = issue['labels']
                label_fields = [f"`{label['name']}`" for label in issue_labels]

                issue_block = {
                    'type': 'section',
                    'text': {'type': 'mrkdwn', 'text': f'<{issue_url}|{issue_title}>'},
                }
                if label_fields:
                    issue_block['fields'] = [
                        {'type': 'mrkdwn', 'text': label} for label in label_fields
                    ]

                blocks.append(issue_block)
                blocks.append({'type': 'divider'})

        message = {'text': 'Weekly GitHub Issues Report', 'blocks': blocks}

        return message
