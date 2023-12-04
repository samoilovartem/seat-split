# Contributing to [STT Backend](https://github.com/lewanddowski/stt_django_backend)

## Commit Message Guidelines
We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for our commit messages. This leads to more readable messages that are easy to follow when looking through the project history and to use automatically generating the changelog from these messages.

Commit Message Format
Each commit message should include a type, an optional scope, and a subject:
```git
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```


### Type
The type is contained at the start of the commit message. The type must be one of the following:

* `feat`: A new feature for the user, not a new feature for a build script.
* `fix`: A bug fix for the user, not a fix to a build script.
* `docs`: Changes to the documentation.
* `style`: Formatting, etc.; no production code change.
* `refactor`: Refactoring production code, eg. renaming a variable.
* `perf`: A code change that improves performance.
* `test`: Adding missing tests, refactoring tests; no production code change.
* `build`: Changes that affect the build system or external dependencies (example scopes: poetry, docker).
* `ci`: Changes to our CI configuration files and scripts (example scopes: GitHub Actions, GitLab CI).
* `chore`: Other changes that don't modify src or test files.
* `revert`: Reverts a previous commit.

### Scope
The scope should be the name of the Django module or feature affected by the change. Below are some common scopes that you might find in a Django project:

* `models`: Changes to Django models (e.g., models.py).
* `views`: Changes to Django views (e.g., views.py or viewsets in DRF).
* `templates`: Changes to Django templates (e.g., HTML files in the templates directory).
* `forms`: Changes to Django forms (e.g., forms.py).
* `admin`: Changes to the Django admin interface (e.g., admin.py).
* `urls`: Changes to URL configurations (e.g., urls.py).
* `settings`: Changes to settings (e.g., settings.py or environment-specific settings files).
* `migrations`: Changes to Django migrations (e.g., files in the migrations directory).
* `management_commands`: Changes to custom management commands.
* `static`: Changes to static files (e.g., CSS, JavaScript, images).
* `middleware`: Changes to middleware components.
* `signals`: Changes to Django signals.
* `tests`: Changes to tests (e.g., tests.py or tests directory).
* `tasks`: Changes to Celery tasks.
* `api`: Changes specific to Django REST Framework or API-related code.
* `auth`: Changes related to authentication and authorization.
* `fixtures`: Changes to data fixtures.
* `utils`: Changes to utility scripts and helper functions.
* `dependencies`: Updates to external packages and dependencies.
* `deployment`: Changes related to deployment configurations.

#### Description
The description contains a succinct description of the change:

* use the imperative, present tense: "change" not "changed" nor "changes".
* don't capitalize the first letter.
* no dot (.) at the end.

#### Body
Just as in the **description**, use the imperative, present tense: "change" not "changed" nor "changes". The body should include the motivation for the change and contrast this with previous behavior.

#### Footer
The footer should contain any information about **Breaking Changes** and is also the place to reference GitHub issues that this commit **Closes**.

## Examples
```git
feat(auth): add support for two-factor authentication

Add support for two-factor authentication. This includes a new model and controller, and a new view for token entry.

BREAKING CHANGE: The user model now requires a phone number.
```

```git
fix(middleware): ensure session middleware handles read-only DB access

Previously, the session middleware would crash when the database was in read-only mode. This fix ensures that we catch the error and handle it gracefully.

Closes #1234
```

## Pull Request Guidelines

Before submitting a pull request, please ensure you adhere to the following guidelines:

### Before You Begin

1. **Check open issues and pull requests** to avoid duplicate submissions.
2. **Update your local repository** to the latest main branch to minimize merge conflicts.
3. **Use the pull request template**: We have provided a pull request template to streamline the submission process. It is located at `.github/pull_request_template.md`. Please use it when creating your pull request.

### Making Changes

1. **Create a new branch** for your changes. Name it in a way that reflects the fix or feature (e.g., `fix/login-error`, `feature/oauth-integration`).
2. **Make your changes** in small, incremental, and logical commits, adhering to the project's commit message guidelines.
3. **Test your changes** thoroughly to ensure they address the issue or add the feature you're working on without introducing new issues.

### Submitting Your Pull Request

1. **Fill out the pull request template**: When you open a new pull request, it will automatically populate with the content from our `pull_request_template.md`. Please fill in all the relevant sections to help us understand your changes.
2. **Title**: Give your pull request a descriptive title that provides an overview of the changes.
3. **Assign a reviewer**: Assign @samoilovartem as a reviewer for your pull request.
4. **Reference Issues**: If your pull request addresses an open issue, include it under Development section in Github.
5. **Draft Pull Requests**: If you're not ready for a full review but want to share your progress or ask for assistance, submit as a draft pull request.

### Pull Request Best Practices

- **Keep changes specific and related**: Your pull request should address a single issue or add a single feature. Avoid combining multiple issues or features into one pull request.
- **Document your changes**: If your changes involve user-facing features or significant alterations, update the README, documentation, or any relevant guides.
- **Follow the code style**: Ensure your code adheres to the existing code style guidelines for the project.
- **Include screenshots or videos**: If your changes affect the UI or user flow, consider adding screenshots or videos to help reviewers understand your changes.

By following these guidelines and using the provided pull request template, you'll help maintain the quality of the project.


## FAQ
In backend development, the distinction between user-facing features and non-user-facing changes can sometimes be less clear than in frontend development, however the principle remains the same: a user-facing feature or fix is something that impacts the functionality, performance, or security of the application as experienced by the user, even if it doesn't directly change the UI.

Here are some guidelines to help you determine if a backend change is a user feature or fix:

1. **User Feature (`feat`)**: If the change introduces new behavior or extends the application in a way that can be directly or indirectly experienced by the user, it's a feature. This could be a new API endpoint, a new data processing service, a new background job that prepares data for users, or a performance improvement that makes the application faster for the user.

2. **User Fix (`fix`)**: If the change corrects a bug that affects the user's interaction with the application, it's a fix. This might be a bug in an API that returns incorrect data, a security patch that fixes a vulnerability, or an issue that causes a background process to fail, resulting in a poor user experience.

3. **Non-User-Facing Changes**: If the change is to code that doesn't affect the user directly, such as a refactoring of the codebase, an update to logging, or a change to the build process, it's not a user feature or fix. These would typically be categorized differently, such as `chore`, `refactor`, `docs`, `style`, `build`, or `ci`.

For example:

- Adding authentication to an API (`feat`): This is a new feature because it changes how users interact with the application, even though they might not "see" the change.
- Fixing a memory leak in a service (`fix`): This is a fix that benefits users by potentially reducing downtime or improving performance.
- Refactoring a database query (`refactor` or `perf`): If it's done purely for code cleanliness and doesn't affect performance, it's a `refactor`. If it improves performance, it might be categorized as `perf` (performance improvement) because users benefit from faster response times.
- Updating a Dockerfile (`build`): Since this doesn't affect users directly but rather affects the deployment process, it would typically be categorized as a `build`.

When in doubt, ask yourself: "Does this change affect the application's behavior from the user's perspective?" If the answer is "yes," it's likely a user-facing feature or fix. If the answer is "no," and it's more about the development process or internal maintenance, categorize it accordingly.
