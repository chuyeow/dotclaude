#!/usr/bin/env python3
"""
Configuration validation script for Claude settings repository.
Validates JSON files and checks for common configuration issues.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def validate_json_file(file_path: Path) -> Dict[str, Any]:
    """Validate that a JSON file is properly formatted."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {"valid": True, "data": data}
    except json.JSONDecodeError as e:
        return {"valid": False, "error": f"JSON parse error: {e}"}
    except FileNotFoundError:
        return {"valid": False, "error": "File not found"}
    except Exception as e:
        return {"valid": False, "error": f"Unexpected error: {e}"}


def validate_mcp_config(data: Dict[str, Any]) -> List[str]:
    """Validate MCP server configuration."""
    issues = []
    
    if "mcpServers" not in data:
        issues.append("Missing 'mcpServers' key in root object")
        return issues
    
    servers = data["mcpServers"]
    if not isinstance(servers, dict):
        issues.append("'mcpServers' must be an object")
        return issues
    
    for server_name, config in servers.items():
        if not isinstance(config, dict):
            issues.append(f"Server '{server_name}' config must be an object")
            continue
            
        # Check required fields
        if "type" not in config:
            issues.append(f"Server '{server_name}' missing 'type' field")
        else:
            valid_types = ["stdio", "sse", "http"]
            if config["type"] not in valid_types:
                issues.append(f"Server '{server_name}' has invalid type '{config['type']}'. Must be one of: {valid_types}")
        
        # Type-specific validation
        if config.get("type") == "stdio":
            if "command" not in config:
                issues.append(f"Server '{server_name}' (stdio) missing 'command' field")
        elif config.get("type") in ["sse", "http"]:
            if "url" not in config:
                issues.append(f"Server '{server_name}' ({config.get('type')}) missing 'url' field")
        
        # Check for placeholder values
        if "env" in config and isinstance(config["env"], dict):
            for key, value in config["env"].items():
                if isinstance(value, str) and ("get-this-from" in value.lower() or "your_" in value.lower()):
                    issues.append(f"Server '{server_name}' has placeholder value for env var '{key}': {value}")
        
        if "headers" in config and isinstance(config["headers"], dict):
            for key, value in config["headers"].items():
                if isinstance(value, str) and ("get-this-from" in value.lower() or "your_" in value.lower()):
                    issues.append(f"Server '{server_name}' has placeholder value for header '{key}': {value}")
    
    return issues


def validate_claude_settings(data: Dict[str, Any]) -> List[str]:
    """Validate Claude settings.json configuration."""
    issues = []
    
    # Check for known configuration keys
    valid_keys = {"model", "statusLine", "hooks", "outputStyle", "memory"}
    unknown_keys = set(data.keys()) - valid_keys
    if unknown_keys:
        issues.append(f"Unknown configuration keys: {', '.join(unknown_keys)}")
    
    # Validate model
    if "model" in data:
        valid_models = {"sonnet", "haiku", "opus", "claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"}
        if data["model"] not in valid_models:
            issues.append(f"Unknown model '{data['model']}'. Consider using one of: {', '.join(valid_models)}")
    
    # Validate statusLine
    if "statusLine" in data:
        status_config = data["statusLine"]
        if isinstance(status_config, dict):
            if "type" not in status_config:
                issues.append("statusLine missing 'type' field")
            elif status_config["type"] == "command" and "command" not in status_config:
                issues.append("statusLine with type 'command' missing 'command' field")
    
    return issues


def main():
    """Main validation function."""
    repo_root = Path(__file__).parent
    issues_found = False
    
    print("🔍 Validating Claude Settings Repository Configuration...")
    print()
    
    # Validate .mcp.json
    print("📋 Validating MCP configuration (.mcp.json)...")
    mcp_result = validate_json_file(repo_root / ".mcp.json")
    if not mcp_result["valid"]:
        print(f"❌ .mcp.json: {mcp_result['error']}")
        issues_found = True
    else:
        mcp_issues = validate_mcp_config(mcp_result["data"])
        if mcp_issues:
            print("⚠️  .mcp.json issues found:")
            for issue in mcp_issues:
                print(f"   • {issue}")
            issues_found = True
        else:
            print("✅ .mcp.json is valid")
    print()
    
    # Validate .claude/settings.json
    print("⚙️  Validating Claude settings (.claude/settings.json)...")
    settings_result = validate_json_file(repo_root / ".claude" / "settings.json")
    if not settings_result["valid"]:
        print(f"❌ .claude/settings.json: {settings_result['error']}")
        issues_found = True
    else:
        settings_issues = validate_claude_settings(settings_result["data"])
        if settings_issues:
            print("⚠️  .claude/settings.json issues found:")
            for issue in settings_issues:
                print(f"   • {issue}")
            issues_found = True
        else:
            print("✅ .claude/settings.json is valid")
    print()
    
    # Check for required directories
    print("📁 Checking directory structure...")
    required_dirs = [
        ".claude/hooks/logs",
        ".claude/cache",
        ".claude/tmp"
    ]
    
    for dir_path in required_dirs:
        full_path = repo_root / dir_path
        if full_path.exists():
            print(f"✅ {dir_path} exists")
        else:
            print(f"⚠️  {dir_path} does not exist (will be created when needed)")
    print()
    
    # Check for .env file
    print("🔐 Checking environment configuration...")
    env_file = repo_root / ".env"
    env_example = repo_root / ".env.example"
    
    if env_example.exists():
        print("✅ .env.example found")
    else:
        print("⚠️  .env.example not found")
        issues_found = True
    
    if env_file.exists():
        print("✅ .env file found")
    else:
        print("ℹ️  .env file not found (optional, but recommended for API keys)")
    print()
    
    # Final summary
    if issues_found:
        print("❌ Configuration validation completed with issues")
        sys.exit(1)
    else:
        print("✅ All configuration files are valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()