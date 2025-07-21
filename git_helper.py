#!/usr/bin/env python3
"""
GitHelper - Helper class for Git operations
"""

import subprocess
import sys
from typing import List, Tuple, Optional


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