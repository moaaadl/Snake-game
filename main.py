#!/usr/bin/env python3
"""
Pro Snake Elite - A professional implementation of the classic Snake game.
"""

import sys
from src.engine import GameEngine

def main():
    try:
        engine = GameEngine()
        engine.run()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
