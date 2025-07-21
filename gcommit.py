#!/usr/bin/env python3
"""
gcommit - AI-powered Git commit message generator
Uses Ollama to generate conventional commit messages from staged changes
"""

import sys
import argparse
from gcommit_app import GCommit


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