# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**gcommit** is a Python CLI tool that uses AI (via Ollama) to generate Git commit messages from staged changes, following conventional commits format.

## Architecture

- **gcommit.py**: Main Python CLI script with Git integration and Ollama API client
- **gcommit**: Shell wrapper script that uses venv Python interpreter
- **requirements.txt**: Single dependency (requests) for HTTP API calls
- **REQUIREMENTS.md**: Original project requirements specification

## Key Components

### CLI Script (gcommit.py)
- **GitHelper** class: Handles git operations (diff, commit, untracked file detection)
- **OllamaClient** class: Manages Ollama API communication for AI message generation
- **GCommit** class: Main application logic coordinating Git operations and AI generation
- Supports command-line arguments: `--ollama-url`, `--model`

### Wrapper Script (gcommit)
- Simple shell script that runs Python via venv
- Checks for existing venv at `./venv/`
- Provides clear setup instructions if venv missing

## Setup Commands

```bash
# Initial setup (user responsibility)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the tool
./gcommit

# Development
python gcommit.py --help
python gcommit.py --ollama-url http://localhost:11434 --model llama3
```

## Usage Flow

1. **Check untracked files** via `git ls-files --others --exclude-standard`
2. **Get staged diff** via `git diff --staged`
3. **Generate commit message** via Ollama API
4. **User confirmation** with option to edit
5. **Execute commit** via `git commit -m "message"`

## Dependencies

- **Python 3.7+** (via venv)
- **requests** library for Ollama HTTP API
- **Git** must be in PATH
- **Ollama** must be running locally