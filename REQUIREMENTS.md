# Requirements for `gcommit` 🤖

`gcommit` is a command-line interface (CLI) tool that uses AI to generate Git commit messages based on your staged changes. It streamlines the commit process by creating well-formatted messages automatically, which you can then approve or edit.

### Core Functional Requirements 📋

*   **Warn About Untracked Files**: Before generating the commit message, the tool must check for untracked files using `git ls-files --others --exclude-standard`. If any are found, it should display a warning to the user, listing the files that are not currently tracked by Git. ⚠️
*   **Read Git Diff**: The program must capture the output of the `git diff --staged` command to get all the changes ready to be committed.
*   **Handle Empty Diff**: If there are no staged changes, the program should notify the user that there's nothing to commit and exit gracefully. 😥
*   **AI-Powered Message Generation**: It will send the captured diff content to a locally running Ollama Large Language Model (LLM).
*   **Generate Commit Message**: The LLM will be prompted to generate a commit message that follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) best practices. This helps keep the commit history clean and readable.
*   **User Confirmation**: Before committing, the tool must display the AI-generated message to the user and ask for confirmation.
    *   If the user types `y` and presses Enter, the generated message is accepted.
    *   If the user types anything else, that input will be used as the commit message instead.
*   **Execute Git Commit**: After confirmation or custom input, the tool will execute `git commit -m "your-final-message"` to finalize the commit.

### Non-Functional Requirements ⚙️

*   **Dependencies**: The tool requires `git` to be installed on the user's system and accessible in the command line's PATH.
*   **Local LLM Connection**: The user must have Ollama running locally. The tool should allow configuration of the Ollama endpoint and the specific model to be used (e.g., `llama3`, `mistral`).
*   **Platform**: The tool should be cross-platform and compatible with macOS, Windows (via WSL), and Linux.
*   **Performance**: The interaction should be fast. The time from running the command to getting a user prompt should be minimal. ⚡

### User Workflow Example 🚶‍♂️

Here’s how a user would interact with `gcommit`:

1.  The user makes changes to their project and adds a new, untracked file.
2.  They stage some changes using `git add .` but forget to add the new file.
3.  In the terminal, they run the command `gcommit`.
4.  The tool first checks for untracked files and displays a warning:
    ```
    ⚠️ Warning: Untracked files detected:
    - new_feature.py

    This file will not be included in the commit. Use 'git add' to track it.
    ```
5.  The tool proceeds to capture the diff of the *staged* files and sends it to Ollama.
6.  The AI-generated message is displayed:
    ```
    Generated commit message:
    feat: add user authentication endpoint

    - Implemented POST /login to handle user credentials
    - Added JWT generation upon successful login

    Accept? (y/n) or enter a new message:
    ```
7.  The user can either:
    *   Type `y` to accept the message.
    *   Type a new message like `feat: add awesome login feature` and press Enter.
8.  The tool executes the `git commit` command with the chosen message, and a success confirmation is shown. 🎉