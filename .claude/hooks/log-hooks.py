#!/usr/bin/env python3

import json
import sys
import os
import fcntl
from pathlib import Path

# Sensitive keys to redact from logs.
SENSITIVE_KEYS = {
    "api_key", "token", "password", "secret", "authorization",
    "cookie", "session", "access_token", "refresh_token",
    "key", "auth", "bearer", "oauth", "jwt", "private_key",
    "client_secret", "client_id", "webhook_secret", "signing_secret"
}

def redact_sensitive(value):
    """Recursively redact sensitive information from nested data structures."""
    if isinstance(value, dict):
        return {
            key: ("<redacted>" if key.lower() in SENSITIVE_KEYS else redact_sensitive(val))
            for key, val in value.items()
        }
    if isinstance(value, list):
        return [redact_sensitive(v) for v in value]
    return value

def log_hook(hook_data):
    """Log hook call to logs directory."""
    # Ensure logs directory exists.
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
    log_dir = Path(project_dir) / '.claude' / 'hooks' / 'logs'
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"HOOK ERROR: Failed to create logs directory: {e}", file=sys.stderr)
        return
    
    log_file = log_dir / 'hooks-log.jsonl'

    with open(log_file, 'a', encoding='utf-8') as f:
        # Lock file to prevent concurrent write issues.
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            redacted_data = redact_sensitive(hook_data)
            f.write(json.dumps(redacted_data) + '\n')
            f.flush()
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)

def main():
    # Read JSON input from stdin.
    raw = sys.stdin.read()

    try:
        payload = json.loads(raw)

        log_hook(payload)

        # Success - prompt will be processed.
        sys.exit(0)

    except json.JSONDecodeError as e:
        # Truncate raw input in error message to prevent log spam.
        snippet = raw[:500]
        print(f"HOOK ERROR: Error parsing JSON: {e}", file=sys.stderr)
        print(f"Raw input (first 500 bytes): {snippet!r}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
