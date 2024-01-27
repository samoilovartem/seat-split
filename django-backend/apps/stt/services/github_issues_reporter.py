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

    def _fetch_closed_issues(self, repo_name: str):
        issues = self.api.issues.list_for_repo(repo=repo_name, state='closed', since=self.start_date)
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
                <= datetime.strptime(issue.get('closed_at'), '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=UTC)
                <= self.end_date
            ):
                valid_issues.append(issue)

        return valid_issues

    def _fetch_user_real_name(self, username: str) -> str:
        """
        Fetches the real name of a GitHub user given their username.
        """
        try:
            user_data = self.api.users.get_by_username(username)
            return user_data.name or username
        except Exception as e:
            logger.error(f'Error fetching user data for {username}: {e}')
            return username

    def _process_assignees(self, assignees: list[dict], user_real_names: dict) -> list[str]:
        """
        Process assignees and return a list of real names.
        """
        real_names = []
        for assignee in assignees:
            username = assignee.get('login')
            if username not in user_real_names:
                user_real_names[username] = self._fetch_user_real_name(username)
            real_names.append(user_real_names[username])
        return real_names

    def _process_issue(self, issue: dict, user_real_names: dict) -> dict:
        """
        Process a single issue and return a dictionary of real names to issue info.
        """
        labels = issue.get('labels')
        label_info = [{'name': label['name'], 'color': label['color']} for label in labels]

        issue_info = {
            'title': issue.get('title'),
            'html_url': issue.get('html_url'),
            'labels': label_info,
        }

        assignees = issue.get('assignees', [])
        real_names = self._process_assignees(assignees, user_real_names)

        return {real_name: issue_info for real_name in real_names}

    def generate_report(self, repo_names: list[str]) -> dict[str, list[dict]]:
        """Generates a report of closed issues for the given repositories."""
        issues_by_user = {}
        user_real_names = {}

        for repo_name in repo_names:
            issues = self._fetch_closed_issues(repo_name)
            for issue in issues:
                if not re.match(self.issue_title_pattern, issue.get('title')):
                    continue

                issue_info_by_user = self._process_issue(issue, user_real_names)
                for real_name, issue_info in issue_info_by_user.items():
                    issues_by_user.setdefault(real_name, []).append(issue_info)

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

                issue_block = {
                    'type': 'section',
                    'text': {'type': 'mrkdwn', 'text': f'<{issue_url}|{issue_title}>'},
                }

                blocks.append(issue_block)

        message = {'text': 'Weekly GitHub Issues Report', 'blocks': blocks}

        return message
