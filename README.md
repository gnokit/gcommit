# gcommit 🤖

AI-powered Git commit message generator that uses Ollama to create conventional commit messages from your staged changes.

## Features

- **AI-powered**: Uses local Ollama LLM to generate commit messages
- **Conventional Commits**: Follows [Conventional Commits](https://www.conventionalcommits.org/) format
- **Untracked file warnings**: Alerts you about files not included in the commit
- **Interactive confirmation**: Review and edit AI-generated messages before committing
- **Cross-platform**: Works on macOS, Linux, and Windows (WSL)
- **Virtual environment**: Uses isolated Python environment via wrapper script

## Quick Start

### 1. Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai), then pull a model:

```bash
ollama pull llama3  # or your preferred model
```

### 2. Clone and Setup

```bash
git clone <your-repo-url>
cd gcommit
```

### 3. First Run

Simply run the wrapper script:

```bash
./gcommit
```

The wrapper will automatically:
- Create a Python virtual environment
- Install required dependencies
- Use the venv Python interpreter exclusively

## Usage

### Basic Usage

1. Make changes to your code
2. Stage your changes:
   ```bash
   git add <files>
   ```
3. Generate commit message:
   ```bash
   ./gcommit
   ```

### Workflow Example

```bash
# Make some changes
echo "console.log('hello')" > app.js

# Stage the changes
git add app.js

# Generate commit message
./gcommit
# Output:
# ⚠️  Warning: Untracked files detected:
#    - debug.log
#
# This file will not be included in the commit. Use 'git add' to track it.
#
# Generating commit message...
#
# Generated commit message:
# ----------------------------------------
# feat: add console log for debugging
#
# - Added console.log statement to app.js for debugging purposes
# ----------------------------------------
# Accept? (y/n) or enter a new message: y
# ✅ Changes committed successfully!
```

### Options

```bash
# Use custom Ollama URL
./gcommit --ollama-url http://localhost:11434

# Use different model
./gcommit --model mistral

# Get help
./gcommit --help
```

## Requirements

- **Python 3.7+** (automatically handled by venv)
- **Git** (must be in PATH)
- **Ollama** (must be running locally)

## How It Works

1. **Checks for untracked files** - Warns about files not tracked by Git
2. **Reads staged changes** - Gets diff of staged files via `git diff --staged`
3. **AI generation** - Sends diff to Ollama LLM for conventional commit generation
4. **User confirmation** - Shows generated message and asks for approval/editing
5. **Commits changes** - Executes `git commit` with final message

## Troubleshooting

### Ollama Not Running
```bash
# Start Ollama
ollama serve

# In another terminal
./gcommit
```

### Permission Issues
```bash
# Make wrapper executable
chmod +x gcommit
```

### Model Issues
```bash
# List available models
ollama list

# Pull a specific model
ollama pull llama3
```

### Virtual Environment Issues
The wrapper script handles venv automatically. To reset:
```bash
rm -rf venv/
./gcommit  # Will recreate venv
```

## Development

If you want to modify the code:

```bash
# Activate venv manually
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run directly with Python
python gcommit.py --help
```

## License

MIT License - see LICENSE file for details.