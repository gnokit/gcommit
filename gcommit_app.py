#!/usr/bin/env python3
"""
GCommit - Main application class for AI-powered git commit message generation
"""

import subprocess
import sys
from typing import List, Tuple
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich.prompt import Prompt, Confirm
from rich.text import Text
from git_helper import GitHelper
from ollama_client import OllamaClient


class GCommit:
    """Main application class"""
    
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "llama3", hint: str = ""):
        self.git = GitHelper()
        self.ollama = OllamaClient(ollama_url, model)
        self.hint = hint
        
        # Set up Rich console with custom theme
        custom_theme = Theme({
            "info": "dim cyan",
            "warning": "yellow",
            "danger": "bold red",
            "success": "bold green",
            "header": "bold magenta",
            "filename": "cyan",
            "highlight": "bold yellow"
        })
        self.console = Console(theme=custom_theme)
    
    def check_untracked_files(self) -> None:
        """Display warning for untracked files"""
        has_untracked, untracked_files = self.git.has_untracked_files()
        if has_untracked:
            self.console.print(Panel(
                "[warning]⚠️  Warning: Untracked files detected[/warning]",
                title="Git Status",
                border_style="yellow"
            ))
            
            table = Table(show_header=True, header_style="warning")
            table.add_column("Untracked Files", style="filename")
            for file in untracked_files:
                table.add_row(file)
            
            self.console.print(table)
            self.console.print("[info]These files will not be included in the commit.[/info]")
            self.console.print("[info]Use [highlight]git add <files>[/highlight] to track them.[/info]\n")
    
    def run(self) -> int:
        """Main application entry point"""
        # Display welcome header
        self.console.print(Panel(
            "[header]🤖 gcommit[/header] - AI-powered Git commit message generator",
            title="Welcome",
            border_style="magenta"
        ))
        
        # Check if we're in a git repository
        try:
            subprocess.run(['git', 'rev-parse', '--git-dir'], 
                         capture_output=True, check=True)
        except subprocess.CalledProcessError:
            self.console.print("[danger]Error: Not in a git repository[/danger]")
            return 1
        
        # Check for untracked files
        self.check_untracked_files()
        
        # Get staged files
        staged_files = self.git.get_staged_files()
        if not staged_files:
            self.console.print(Panel(
                "[warning]No staged changes to commit[/warning] 😥",
                title="Git Status",
                border_style="yellow"
            ))
            self.console.print("[info]Use [highlight]git add <files>[/highlight] to stage your changes first.[/info]")
            return 0
        
        # Check Ollama availability
        if not self.ollama.is_available():
            self.console.print("[danger]Error: Ollama is not running or not accessible.[/danger]")
            self.console.print("[info]Please start Ollama with: [highlight]ollama serve[/highlight][/info]")
            return 1
        
        # Process each file
        self.console.rule("[header]Analyzing Staged Files[/header]")
        file_summaries = []
        
        for filepath in track(staged_files, description="Processing files..."):
            diff = self.git.get_file_diff(filepath)
            if diff:
                with self.console.status(f"[info]Analyzing[/info] [filename]{filepath}[/filename]...") as status:
                    summary = self.ollama.summarize_file_changes(filepath, diff, self.hint)
                    if summary:
                        file_summaries.append((filepath, summary))
        
        if not file_summaries:
            self.console.print("[danger]Error: Could not summarize any file changes[/danger]")
            return 1
        
        # Display file summaries table
        self.console.rule("[header]File Analysis Results[/header]")
        summary_table = Table(show_header=True, header_style="header")
        summary_table.add_column("File", style="filename", width=30)
        summary_table.add_column("Summary", style="white")
        
        for filepath, summary in file_summaries:
            summary_table.add_row(filepath, summary)
        
        self.console.print(summary_table)
        
        # Generate commit message from summaries
        self.console.rule("[header]Generating Commit Message[/header]")
        with self.console.status("[info]Creating commit message...[/info]") as status:
            commit_message = self.ollama.generate_commit_message(file_summaries, self.hint)
        
        if not commit_message:
            self.console.print("[danger]Error: Failed to generate commit message[/danger]")
            return 1
        
        # Display and get confirmation
        self.console.rule("[header]Commit Message Preview[/header]")
        self.console.print(Panel(
            commit_message,
            title="Generated Commit Message",
            border_style="green",
            expand=False
        ))
        
        choices = ["Accept and commit", "Reject and cancel", "Edit message"]
        choice = Prompt.ask(
            "\nWhat would you like to do?",
            choices=["accept", "reject", "edit"],
            default="accept"
        )
        
        if choice == "accept":
            final_message = commit_message
        elif choice == "reject":
            self.console.print("[warning]Commit cancelled.[/warning]")
            return 0
        elif choice == "edit":
            final_message = Prompt.ask("Enter your commit message", default=commit_message)
        
        # Commit changes
        self.console.rule("[header]Committing Changes[/header]")
        with self.console.status("[info]Committing...[/info]") as status:
            if self.git.commit_changes(final_message):
                self.console.print("[success]✅ Changes committed successfully![/success]")
                return 0
            else:
                return 1