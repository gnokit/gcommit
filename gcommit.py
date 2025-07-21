#!/usr/bin/env python3
"""
gcommit - AI-powered Git commit message generator
Uses Ollama to generate conventional commit messages from staged changes
"""

import subprocess
import sys
import json
import os
from typing import List, Tuple, Optional
import argparse
import requests


class GitHelper:
    """Helper class for Git operations"""
    
    @staticmethod
    def has_untracked_files() -> Tuple[bool, List[str]]:
        """Check for untracked files in the repository"""
        try:
            result = subprocess.run(
                ['git', 'ls-files', '--others', '--exclude-standard'],
                capture_output=True,
                text=True,
                check=True
            )
            files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
            return len(files) > 0, files
        except subprocess.CalledProcessError:
            return False, []
    
    @staticmethod
    def get_staged_files() -> List[str]:
        """Get list of staged files"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--staged', '--name-only'],
                capture_output=True,
                text=True,
                check=True
            )
            return [f.strip() for f in result.stdout.split('\n') if f.strip()]
        except subprocess.CalledProcessError:
            return []
    
    @staticmethod
    def get_file_diff(filepath: str) -> Optional[str]:
        """Get diff for specific file"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--staged', '--', filepath],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout if result.stdout.strip() else None
        except subprocess.CalledProcessError as e:
            print(f"Error getting diff for {filepath}: {e}", file=sys.stderr)
            return None
    
    @staticmethod
    def commit_changes(message: str) -> bool:
        """Commit changes with the given message"""
        try:
            subprocess.run(
                ['git', 'commit', '-m', message],
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error committing changes: {e}", file=sys.stderr)
            return False


class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "gemma3:4b-it-qat"):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.api_url = f"{self.base_url}/api/generate"
    
    def is_available(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def summarize_file_changes(self, filepath: str, diff: str) -> Optional[str]:
        """Generate one-sentence summary for file changes"""
        if not diff.strip():
            return None
        
        prompt = f"""Summarize the changes in this file in one concise sentence.

File: {filepath}
Changes:
{diff}

Provide only the summary sentence, no additional text."""

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                summary = result.get('response', '').strip()
                return summary if summary else None
            else:
                print(f"Ollama API error for {filepath}: {response.status_code}", file=sys.stderr)
                return None
                
        except requests.RequestException as e:
            print(f"Error connecting to Ollama for {filepath}: {e}", file=sys.stderr)
            return None

    def generate_commit_message(self, file_summaries: List[Tuple[str, str]]) -> Optional[str]:
        """Generate commit message from file summaries"""
        if not file_summaries:
            return None
        
        summaries_text = "\n".join([f"- {filepath}: {summary}" for filepath, summary in file_summaries])
        
        prompt = f"""Generate a git commit message for the following file changes following Conventional Commits format.

The message should be concise but descriptive, following this format:
<type>: <description>

<body explaining the overall changes>

Types: feat, fix, docs, style, refactor, test, chore

File changes:
{summaries_text}

Provide only the commit message, no additional text."""

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result.get('response', '').strip()
                return message if message else None
            else:
                print(f"Ollama API error: {response.status_code}", file=sys.stderr)
                return None
                
        except requests.RequestException as e:
            print(f"Error connecting to Ollama: {e}", file=sys.stderr)
            return None


class GCommit:
    """Main application class"""
    
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "llama3"):
        self.git = GitHelper()
        self.ollama = OllamaClient(ollama_url, model)
    
    def check_untracked_files(self) -> None:
        """Display warning for untracked files"""
        has_untracked, untracked_files = self.git.has_untracked_files()
        if has_untracked:
            print("⚠️  Warning: Untracked files detected:")
            for file in untracked_files:
                print(f"   - {file}")
            print("\nThis file will not be included in the commit. Use 'git add' to track it.\n")
    
    def run(self) -> int:
        """Main application entry point"""
        # Check if we're in a git repository
        try:
            subprocess.run(['git', 'rev-parse', '--git-dir'], 
                         capture_output=True, check=True)
        except subprocess.CalledProcessError:
            print("Error: Not in a git repository", file=sys.stderr)
            return 1
        
        # Check for untracked files
        self.check_untracked_files()
        
        # Get staged files
        staged_files = self.git.get_staged_files()
        if not staged_files:
            print("No staged changes to commit. 😥")
            print("Use 'git add <files>' to stage your changes first.")
            return 0
        
        # Check Ollama availability
        if not self.ollama.is_available():
            print("Error: Ollama is not running or not accessible.", file=sys.stderr)
            print("Please start Ollama with: ollama serve", file=sys.stderr)
            return 1
        
        # Process each file
        print("Analyzing staged files...")
        file_summaries = []
        
        for filepath in staged_files:
            diff = self.git.get_file_diff(filepath)
            if diff:
                print(f"Summarizing changes in {filepath}...")
                summary = self.ollama.summarize_file_changes(filepath, diff)
                if summary:
                    file_summaries.append((filepath, summary))
        
        if not file_summaries:
            print("Error: Could not summarize any file changes", file=sys.stderr)
            return 1
        
        # Generate commit message from summaries
        print("Generating commit message...")
        commit_message = self.ollama.generate_commit_message(file_summaries)
        
        if not commit_message:
            print("Error: Failed to generate commit message", file=sys.stderr)
            return 1
        
        # Display and get confirmation
        print("\nGenerated commit message:")
        print("-" * 40)
        print(commit_message)
        print("-" * 40)
        
        while True:
            choice = input("\nAccept? (y/n) or enter a new message: ").strip()
            
            if choice.lower() == 'y':
                final_message = commit_message
                break
            elif choice.lower() == 'n':
                print("Commit cancelled.")
                return 0
            elif choice:
                final_message = choice
                break
            else:
                print("Please enter 'y', 'n', or a new message.")
        
        # Commit changes
        if self.git.commit_changes(final_message):
            print("✅ Changes committed successfully!")
            return 0
        else:
            return 1


def main():
    """Entry point for the CLI"""
    parser = argparse.ArgumentParser(description='AI-powered git commit message generator')
    parser.add_argument('--ollama-url', default='http://localhost:11434',
                       help='Ollama server URL (default: http://localhost:11434)')
    parser.add_argument('--model', default='gemma3:4b-it-qat',
                       help='Ollama model to use (default: gemma3:4b-it-qat)')
    
    args = parser.parse_args()
    
    app = GCommit(ollama_url=args.ollama_url, model=args.model)
    sys.exit(app.run())


if __name__ == '__main__':
    main()