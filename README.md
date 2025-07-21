# gcommit 🤖

AI-powered Git commit message generator that uses Ollama to create conventional commit messages from your staged changes.

## Features

- **AI-powered**: Uses local Ollama LLM to generate commit messages
- **Conventional Commits**: Follows [Conventional Commits](https://www.conventionalcommits.org/) format
- **Rich Terminal UI**: Beautiful, modern terminal interface with progress bars and styled output
- **Untracked file warnings**: Alerts you about files not included in the commit
- **Interactive confirmation**: Review and edit AI-generated messages before committing
- **Progress indicators**: Real-time progress bars and spinner animations
- **Cross-platform**: Works on macOS, Linux, and Windows (WSL)
- **Virtual environment**: Uses isolated Python environment via wrapper script

## Quick Start

### 1. Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai), then pull the recommended model:

```bash
ollama pull gemma3:4b-it-qat  # recommended model
```

### 2. Clone and Setup

```bash
git clone <your-repo-url>
cd gcommit
```

### 3. Manual Setup (Required)

You need to manually set up the Python virtual environment:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make wrapper executable
chmod +x gcommit
```

### 4. Add to PATH (Recommended)

To use gcommit from any project directory, add it to your PATH:

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export PATH="$PATH:/path/to/gcommit"

# Or create a symlink
sudo ln -s /path/to/gcommit/gcommit /usr/local/bin/gcommit
```

### 5. First Run

```bash
gcommit <your_initial_commit_message>
```

## Usage

### Workflow Example

```bash
# Make some changes
echo "console.log('hello')" > app.js

# Stage the changes
git add app.js

# Generate commit message
gcommit "add console log message: hello"
# Output:
# ┌─────────────────────────────────────────────────────┐
# │                    Welcome                          │
# │ 🤖 gcommit - AI-powered Git commit message generator │
# └─────────────────────────────────────────────────────┘
# 
# ─────── Analyzing Staged Files ───────
# Processing files... ━━━━━━━━━━━━━━━━━━━━━━━━ 100% 1/1
# Analyzing app.js... 
# 
# ─────── File Analysis Results ───────
# ┌────────────┬─────────────────────────────────────────┐
# │ File       │ Summary                                 │
# ├────────────┼─────────────────────────────────────────┤
# │ app.js     │ Added console.log statement for debugging│
# └────────────┴─────────────────────────────────────────┘
# 
# ─────── Generating Commit Message ───────
# Creating commit message... 
# 
# ─────── Commit Message Preview ───────
# ┌─────────────────────────────┐
# │  Generated Commit Message   │
# │                             │
# │ feat: add console log for   │
# │ debugging                   │
# │                             │
# │ - Added console.log         │
# │   statement to app.js for   │
# │   debugging purposes        │
# └─────────────────────────────┘
# 
# What would you like to do? (accept/reject/edit) [accept]: accept
# ─────── Committing Changes ───────
# Committing... 
# ✅ Changes committed successfully!
```

## Requirements

- **Python 3.7+** (automatically handled by venv)
- **Git** (must be in PATH)
- **Ollama** (must be running locally)

## How It Works

1. **Rich UI Display** - Shows beautiful welcome header and organized sections
2. **Checks for untracked files** - Displays warnings in styled tables
3. **Reads staged changes** - Gets diff of staged files via `git diff --staged`
4. **Progress Tracking** - Shows real-time progress bars and spinners during processing
5. **AI generation** - Sends diff to Ollama LLM for conventional commit generation
6. **Interactive Preview** - Displays commit message in styled panels
7. **User confirmation** - Rich interactive prompts for approval/editing
8. **Commits changes** - Executes `git commit` with final message

## License

MIT License - see LICENSE file for details.