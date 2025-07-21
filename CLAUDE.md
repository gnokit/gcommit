# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**gcommit** is a Python CLI tool that uses Ollama (local AI) to generate conventional commit messages from staged Git changes.

## Architecture

The codebase follows a modular design with clear separation of concerns:

- **gcommit.py**: CLI entry point with argument parsing
- **gcommit_app.py**: Main application orchestrator (`GCommit` class)
- **git_helper.py**: Git operations wrapper (`GitHelper` class)
- **ollama_client.py**: Ollama API client (`OllamaClient` class)
- **gcommit**: Shell wrapper for venv isolation

### Key Classes

#### GCommit (gcommit_app.py)
- Orchestrates the entire commit message generation flow
- Handles user interaction and confirmation
- Coordinates between GitHelper and OllamaClient

#### GitHelper (git_helper.py)
- `has_untracked_files()`: Detects untracked files for warnings
- `get_staged_files()`: Returns list of staged file paths
- `get_file_diff(filepath)`: Gets diff for specific file
- `commit_changes(message)`: Executes git commit

#### OllamaClient (ollama_client.py)
- `is_available()`: Checks Ollama server connectivity
- `summarize_file_changes(filepath, diff, hint)`: Generates per-file summaries
- `generate_commit_message(file_summaries, hint)`: Creates final commit message

## Development Commands

### Setup
```bash
# Initial setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Make wrapper executable
chmod +x gcommit
```

### Running
```bash
# Standard usage
./gcommit "hint about changes"

# With custom model
./gcommit "fix bug" --model llama3

# Direct Python (for development)
python gcommit.py "implement feature" --ollama-url http://localhost:11434
```

### Development Flow
1. Stage changes: `git add <files>`
2. Generate commit: `./gcommit "description hint"`
3. Review generated message
4. Confirm or edit as needed

## Dependencies

- **requests>=2.28.0**: HTTP client for Ollama API
- **rich>=13.0.0**: Terminal formatting (currently unused, can be removed)

## External Requirements

- **Git**: Must be in PATH
- **Ollama**: Must be running locally (default: http://localhost:11434)
- **Python 3.7+**: For venv compatibility

## Key Behaviors

1. **Untracked file warnings**: Alerts about files not in commit
2. **Conventional commits**: Uses format `<type>: <description>`
3. **Interactive confirmation**: Always prompts before committing
4. **Staged diff analysis**: Only commits what's staged
5. **Hint system**: Accepts user hints for message generation

## Common Issues

- **Ollama not running**: Start with `ollama serve`
- **Permission denied**: `chmod +x gcommit`
- **Venv missing**: Follow setup commands above