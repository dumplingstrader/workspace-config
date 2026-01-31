#!/usr/bin/env python3

"""
Resource Loader
Provides functions to search and load resources efficiently
Designed for use as a tool by AI models to minimize token usage
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

WORKSPACE_DIR = Path(__file__).parent.parent  # E:\_Development
INDEX_DIR = Path(__file__).parent / 'indexes'


def load_index(index_type: str = 'master') -> Dict[str, Any]:
    """Load index files"""
    index_path = INDEX_DIR / f'{index_type}-index.json'
    if not index_path.exists():
        raise FileNotFoundError(f'Index not found: {index_type}. Run index_builder.py first.')

    with open(index_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def search_resources(
    query: str,
    resource_type: Optional[str] = None,
    tags: Optional[List[str]] = None,
    limit: int = 10,
    include_content: bool = False
) -> List[Dict[str, Any]]:
    """Search resources by query"""
    master_index = load_index('master')
    all_resources = (
        master_index['resources']['skills'] +
        master_index['resources']['agents'] +
        master_index['resources']['prompts'] +
        master_index['resources']['instructions']
    )

    # Filter by type if specified
    if resource_type:
        all_resources = [r for r in all_resources if r['type'] == resource_type]

    # Filter by tags if specified
    if tags:
        all_resources = [
            r for r in all_resources
            if 'tags' in r and any(tag in r['tags'] for tag in tags)
        ]

    # Search in name and description
    query_lower = query.lower()
    results = [
        r for r in all_resources
        if query_lower in r['name'].lower() or
           (r.get('description') and query_lower in r['description'].lower())
    ]

    # Sort by relevance (exact matches first, then name matches, then description matches)
    def sort_key(r):
        name_exact = 1 if r['name'].lower() == query_lower else 0
        name_match = 1 if query_lower in r['name'].lower() else 0
        return (-name_exact, -name_match, r['name'])

    results.sort(key=sort_key)

    # Limit results
    results = results[:limit]

    # Load full content if requested
    if include_content:
        for r in results:
            r['content'] = load_resource_content(r['path'])

    return results


def load_resource_content(resource_path: str) -> str:
    """Load full content of a resource by path (all paths relative to workspace)."""
    full_path = WORKSPACE_DIR / resource_path
    if not full_path.exists():
        raise FileNotFoundError(f'Resource not found: {resource_path}')

    return full_path.read_text(encoding='utf-8')


def get_resource_by_name(name: str, resource_type: Optional[str] = None) -> Dict[str, Any]:
    """Get resource by exact name"""
    master_index = load_index('master')
    all_resources = (
        master_index['resources']['skills'] +
        master_index['resources']['agents'] +
        master_index['resources']['prompts'] +
        master_index['resources']['instructions']
    )

    if resource_type:
        all_resources = [r for r in all_resources if r['type'] == resource_type]

    # Try exact match first
    resource = next((r for r in all_resources if r['name'] == name), None)

    # Try case-insensitive match
    if not resource:
        resource = next((r for r in all_resources if r['name'].lower() == name.lower()), None)

    if not resource:
        raise ValueError(f'Resource not found: {name}')

    # Load content
    resource['content'] = load_resource_content(resource['path'])
    return resource


def list_resources(resource_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all available resources (metadata only)"""
    master_index = load_index('master')

    if resource_type:
        type_map = {
            'claude-skill': 'skills',
            'copilot-agent': 'agents',
            'copilot-prompt': 'prompts',
            'copilot-instruction': 'instructions'
        }
        if resource_type not in type_map:
            raise ValueError(f'Unknown type: {resource_type}')
        return master_index['resources'][type_map[resource_type]]

    return (
        master_index['resources']['skills'] +
        master_index['resources']['agents'] +
        master_index['resources']['prompts'] +
        master_index['resources']['instructions']
    )


def get_stats() -> Dict[str, Any]:
    """Get statistics about indexed resources"""
    master_index = load_index('master')
    return {
        **master_index['stats'],
        'generatedAt': master_index['generatedAt']
    }


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print('Usage:')
        print('  resource_loader.py search <query> [--type=<type>] [--content]')
        print('  resource_loader.py get <name> [--type=<type>]')
        print('  resource_loader.py list [type]')
        print('  resource_loader.py stats')
        print('')
        print('Types: claude-skill, copilot-agent, copilot-prompt, copilot-instruction')
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == 'search':
            if len(sys.argv) < 3:
                print('Usage: resource_loader.py search <query> [--type=<type>] [--content]')
                sys.exit(1)

            query = sys.argv[2]
            resource_type = None
            include_content = False

            for arg in sys.argv[3:]:
                if arg.startswith('--type='):
                    resource_type = arg.split('=', 1)[1]
                elif arg == '--content':
                    include_content = True

            results = search_resources(query, resource_type=resource_type, include_content=include_content)
            print(json.dumps(results, indent=2))

        elif command == 'get':
            if len(sys.argv) < 3:
                print('Usage: resource_loader.py get <name> [--type=<type>]')
                sys.exit(1)

            name = sys.argv[2]
            resource_type = None

            for arg in sys.argv[3:]:
                if arg.startswith('--type='):
                    resource_type = arg.split('=', 1)[1]

            resource = get_resource_by_name(name, resource_type)
            print(json.dumps(resource, indent=2))

        elif command == 'list':
            resource_type = sys.argv[2] if len(sys.argv) > 2 else None
            resources = list_resources(resource_type)
            print(json.dumps(resources, indent=2))

        elif command == 'stats':
            stats = get_stats()
            print(json.dumps(stats, indent=2))

        else:
            print(f'Unknown command: {command}')
            sys.exit(1)

    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
