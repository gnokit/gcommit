#!/usr/bin/env python3
"""
GCommit - Main application class for AI-powered git commit message generation
"""

import subprocess
import sys
from typing import List, Tuple
from git_helper import GitHelper
from ollama_client import OllamaClient


class GCommit:
    """Main application class"""
    
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "llama3", hint: str = ""):
        self.git = GitHelper()
        self.ollama = OllamaClient(ollama_url, model)
        self.hint = hint
    
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
        
        for i, filepath in enumerate(staged_files, 1):
            diff = self.git.get_file_diff(filepath)
            if diff:
                print(f"({i}/{len(staged_files)}) Summarizing changes in {filepath}...")
                summary = self.ollama.summarize_file_changes(filepath, diff, self.hint)
                if summary:
                    file_summaries.append((filepath, summary))
        
        if not file_summaries:
            print("Error: Could not summarize any file changes", file=sys.stderr)
            return 1
        
        # Generate commit message from summaries
        print("Generating commit message...")
        commit_message = self.ollama.generate_commit_message(file_summaries, self.hint)
        
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