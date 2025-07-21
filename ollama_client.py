#!/usr/bin/env python3
"""
OllamaClient - Client for interacting with Ollama API
"""

import sys
import json
from typing import List, Tuple, Optional
import requests
from rich.console import Console

console = Console()


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
    
    def summarize_file_changes(self, filepath: str, diff: str, hint: str = "") -> Optional[str]:
        """Generate one-sentence summary for file changes"""
        if not diff.strip():
            return None
        
        hint_text = f"User Initial Commit Message:\n{hint}" if hint else ""
        prompt = f"""Analyze the following git diff and summarize the changes for this file in one concise sentence.

File: {filepath}
Git Diff:
{diff}
{hint_text}

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
                console.print(f"[danger]Ollama API error for {filepath}: {response.status_code}[/danger]")
                return None
                
        except requests.RequestException as e:
            console.print(f"[danger]Error connecting to Ollama for {filepath}: {e}[/danger]")
            return None
    
    def generate_commit_message(self, file_summaries: List[Tuple[str, str]], hint: str = "") -> Optional[str]:
        """Generate commit message from file summaries"""
        if not file_summaries:
            return None
        
        summaries_text = "\n".join([f"- {filepath}: {summary}" for filepath, summary in file_summaries])
        
        hint_text = f"\nUser Initial Commit Message:\n{hint}" if hint else ""
        prompt = f"""You are an expert at writing git commit messages following the Conventional Commits specification.
Your task is to analyze the provided file changes and generate a well-formed commit message.

### Rules
1.  **Format:** The commit message must follow this structure: `<type>: <subject>\n\n<body>`.
2.  **Type Selection:** First, you MUST determine the single most appropriate commit `type` by analyzing the user's intent from the file changes. Choose from this list only:
    *   **feat**: A new feature is introduced.
    *   **fix**: A bug in the code is fixed.
    *   **docs**: Changes are made only to documentation (e.g., README, comments).
    *   **style**: Code style changes that don't affect logic (e.g., formatting, whitespace).
    *   **refactor**: A code change that neither fixes a bug nor adds a feature.
    *   **test**: Adding new tests or correcting existing ones.
    *   **chore**: Changes to the build process, tooling, or repository maintenance.
3.  **Subject Line:** The `<subject>` must be a concise summary of the change, written in the imperative mood (e.g., "add," not "added" or "adds"). Start with a lowercase letter and do not end with a period.
4.  **Body:** The `<body>` should explain the "what" and "why" of the change in detail.
5.  **Output:** CRITICAL: Your response must contain ONLY the raw commit message and nothing else. Do not include any explanations or introductory text.

### File Changes to Analyze
{summaries_text}
{hint_text}
"""


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
                console.print(f"[danger]Ollama API error: {response.status_code}[/danger]")
                return None
                
        except requests.RequestException as e:
            console.print(f"[danger]Error connecting to Ollama: {e}[/danger]")
            return None