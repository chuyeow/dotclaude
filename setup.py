#!/usr/bin/env python3
"""
Setup script for Claude settings repository.
Creates necessary directories and validates configuration.
"""

import os
import sys
from pathlib import Path


def create_directory_structure():
    """Create required directory structure for Claude settings."""
    repo_root = Path(__file__).parent
    
    directories = [
        ".claude/hooks/logs",
        ".claude/cache", 
        ".claude/tmp",
        ".claude/agents",
        ".claude/commands"
    ]
    
    print("📁 Creating directory structure...")
    
    for dir_path in directories:
        full_path = repo_root / dir_path
        if full_path.exists():
            print(f"✅ {dir_path} already exists")
        else:
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✨ Created {dir_path}")
    
    print()


def setup_environment_file():
    """Guide user through environment file setup."""
    repo_root = Path(__file__).parent
    env_file = repo_root / ".env"
    env_example = repo_root / ".env.example"
    
    print("🔐 Environment configuration...")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    if not env_example.exists():
        print("⚠️  .env.example not found, skipping environment setup")
        return
    
    print("📝 .env file not found.")
    try:
        response = input("Would you like to create one from .env.example? (y/N): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        response = "n"
        print("n")
    
    if response in ['y', 'yes']:
        try:
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✨ Created .env from .env.example")
            print("⚠️  Remember to edit .env with your actual API keys!")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
    else:
        print("ℹ️  Skipping .env creation. You can copy .env.example manually later.")
    
    print()


def set_permissions():
    """Set proper permissions for scripts."""
    repo_root = Path(__file__).parent
    
    scripts = [
        "validate-config.py",
        ".claude/hooks/log-hooks.py"
    ]
    
    print("🔧 Setting script permissions...")
    
    for script_path in scripts:
        full_path = repo_root / script_path
        if full_path.exists():
            try:
                os.chmod(full_path, 0o755)
                print(f"✅ Set executable permissions for {script_path}")
            except Exception as e:
                print(f"⚠️  Failed to set permissions for {script_path}: {e}")
        else:
            print(f"⚠️  Script not found: {script_path}")
    
    print()


def validate_configuration():
    """Run configuration validation."""
    print("🔍 Running configuration validation...")
    
    try:
        # Import and run validation
        sys.path.insert(0, str(Path(__file__).parent))
        import importlib.util
        
        spec = importlib.util.spec_from_file_location("validate_config", Path(__file__).parent / "validate-config.py")
        validate_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validate_module)
        validate_main = validate_module.main
        
        # Capture validation result
        validate_main()
        
    except SystemExit as e:
        if e.code == 0:
            print("✅ Configuration validation passed!")
        else:
            print("⚠️  Configuration validation found issues (see above)")
            return False
    except ImportError:
        print("⚠️  Could not run validation (validate-config.py not found)")
        return False
    except Exception as e:
        print(f"❌ Validation failed with error: {e}")
        return False
    
    return True


def print_next_steps():
    """Print helpful next steps for the user."""
    print("🎉 Setup completed!")
    print()
    print("📋 Next steps:")
    print("1. Edit .env file with your actual API keys (if created)")
    print("2. Set CLAUDE_PROJECT_DIR environment variable:")
    print(f"   export CLAUDE_PROJECT_DIR={Path(__file__).parent.absolute()}")
    print("3. Test your configuration:")
    print("   ./validate-config.py")
    print("4. Start using Claude with your custom settings!")
    print()
    print("📚 See README.md for detailed usage instructions.")


def main():
    """Main setup function."""
    print("🚀 Claude Settings Repository Setup")
    print("===================================")
    print()
    
    try:
        create_directory_structure()
        setup_environment_file()
        set_permissions()
        
        # Only show success if validation passes
        if validate_configuration():
            print_next_steps()
        else:
            print()
            print("⚠️  Setup completed but with configuration issues.")
            print("   Please review the validation output above and fix any issues.")
            
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()