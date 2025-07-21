#!/usr/bin/env python3
"""
OllamaClient - Client for interacting with Ollama API
"""

import sys
import json
from typing import List, Tuple, Optional
import requests


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