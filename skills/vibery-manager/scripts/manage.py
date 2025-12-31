#!/usr/bin/env python3
"""
Vibery Manager - Unified management for templates and kits.

Usage:
    python manage.py template <action> [args]
    python manage.py kit <action> [args]
    python manage.py sync
    python manage.py publish
    python manage.py deploy   # sync + publish in one command
"""

import argparse
import sys
from pathlib import Path

# Add operations to path
sys.path.insert(0, str(Path(__file__).parent / "operations"))

from template import template_command
from kit import kit_command
from sync import sync_command
from publish import publish_command


def deploy_command(dry_run: bool = False):
    """Full deploy: sync + publish."""
    print("\n\033[34m═══ DEPLOY: Full deployment pipeline ═══\033[0m\n")
    sync_command(dry_run)
    publish_command(dry_run)


def main():
    parser = argparse.ArgumentParser(
        description="Vibery Manager - Templates & Kits",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  template pull <source>         Pull template from git/URL
  template create <type> <name>  Create new template
  template list [--type TYPE]    List templates

  kit create <name>              Create new kit
  kit add <kit> <item>           Add template/skill to kit
  kit remove <kit> <item>        Remove from kit
  kit list [kit-name]            List kits or kit contents

  sync                           Sync to local folders (CLI + website)
  publish                        Push to GitHub + deploy website
  deploy                         Full deploy (sync + publish)

Examples:
  python manage.py template pull https://github.com/user/skills
  python manage.py kit create backend-stack
  python manage.py deploy        # One command to deploy everything
        """
    )

    parser.add_argument("command", choices=["template", "kit", "sync", "publish", "deploy"])
    parser.add_argument("args", nargs="*", help="Command arguments")
    parser.add_argument("--type", "-t", help="Filter by type")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")

    args = parser.parse_args()

    try:
        if args.command == "template":
            template_command(args.args, args.type, args.dry_run)
        elif args.command == "kit":
            kit_command(args.args, args.dry_run)
        elif args.command == "sync":
            sync_command(args.dry_run)
        elif args.command == "publish":
            publish_command(args.dry_run)
        elif args.command == "deploy":
            deploy_command(args.dry_run)
    except Exception as e:
        print(f"\033[31mError: {e}\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    main()
