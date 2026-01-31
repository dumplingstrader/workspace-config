#!/usr/bin/env python3

"""
Resource Index Builder
Scans .claude/skills and _reference/awesome-copilot to create lightweight indexes
This reduces AI token costs by providing metadata without full content
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

WORKSPACE_DIR = Path(__file__).parent.parent  # E:\_Development
REFERENCE_DIR = WORKSPACE_DIR / '_reference' / 'awesome-copilot'
OUTPUT_DIR = Path(__file__).parent / 'indexes'

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)


def parse_frontmatter(content: str) -> Dict[str, Any]:
    """Parse YAML frontmatter from markdown files"""
    frontmatter_pattern = r'^---\s*\n(.*?)\n---'
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if not match:
        return {}

    frontmatter = {}
    lines = match.group(1).split('\n')

    for line in lines:
        if ':' not in line:
            continue

        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()

        # Remove quotes if present
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]

        frontmatter[key] = value

    return frontmatter


def extract_summary(content: str, max_length: int = 200) -> str:
    """Extract first paragraph after frontmatter as summary"""
    # Remove frontmatter
    without_frontmatter = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    # Get first non-empty paragraph
    paragraphs = without_frontmatter.split('\n\n')
    for para in paragraphs:
        cleaned = para.strip().lstrip('#').strip()  # Remove headers
        if cleaned and not cleaned.startswith('```'):
            return cleaned[:max_length] + '...' if len(cleaned) > max_length else cleaned

    return ''


def index_claude_skills() -> List[Dict[str, Any]]:
    """Index Claude skills from .claude/skills"""
    skills_dir = WORKSPACE_DIR / '.claude' / 'skills'
    if not skills_dir.exists():
        print('No .claude/skills directory found')
        return []

    skills = []

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / 'SKILL.md'
        if not skill_file.exists():
            continue

        try:
            content = skill_file.read_text(encoding='utf-8')
            frontmatter = parse_frontmatter(content)
            summary = extract_summary(content)

            skills.append({
                'name': frontmatter.get('name', skill_dir.name),
                'description': frontmatter.get('description', summary),
                'type': 'claude-skill',
                'path': str(skill_file.relative_to(WORKSPACE_DIR)).replace('\\', '/'),
                'tags': [t.strip() for t in frontmatter.get('tags', '').split(',')] if frontmatter.get('tags') else [],
                'size': len(content.encode('utf-8'))
            })
        except Exception as e:
            print(f'Error processing {skill_file}: {e}')

    return skills


def index_agents() -> List[Dict[str, Any]]:
    """Index agents from .github/awesome-copilot-main/agents"""
    agents_dir = REFERENCE_DIR / 'agents'
    if not agents_dir.exists():
        print('No agents directory found')
        return []

    agents = []

    for agent_file in agents_dir.glob('*.agent.md'):
        try:
            content = agent_file.read_text(encoding='utf-8')
            frontmatter = parse_frontmatter(content)

            # Parse tools array
            tools = []
            if 'tools' in frontmatter:
                tools_str = frontmatter['tools'].strip()
                if tools_str.startswith('[') and tools_str.endswith(']'):
                    # Parse JSON-like array
                    tools_str = tools_str.replace("'", '"')
                    try:
                        tools = json.loads(tools_str)
                    except:
                        # Fallback to simple split
                        tools = [t.strip().strip('"').strip("'") for t in tools_str[1:-1].split(',')]

            agents.append({
                'name': frontmatter.get('name', agent_file.stem.replace('.agent', '')),
                'description': frontmatter.get('description', ''),
                'type': 'copilot-agent',
                'path': str(agent_file.relative_to(WORKSPACE_DIR)).replace('\\', '/'),
                'tools': tools,
                'size': len(content.encode('utf-8'))
            })
        except Exception as e:
            print(f'Error processing {agent_file}: {e}')

    return agents


def index_prompts() -> List[Dict[str, Any]]:
    """Index prompts from .github/awesome-copilot-main/prompts"""
    prompts_dir = REFERENCE_DIR / 'prompts'
    if not prompts_dir.exists():
        print('No prompts directory found')
        return []

    prompts = []

    for prompt_file in prompts_dir.glob('*.prompt.md'):
        try:
            content = prompt_file.read_text(encoding='utf-8')
            frontmatter = parse_frontmatter(content)

            prompts.append({
                'name': frontmatter.get('name', prompt_file.stem.replace('.prompt', '')),
                'description': frontmatter.get('description', ''),
                'type': 'copilot-prompt',
                'path': str(prompt_file.relative_to(WORKSPACE_DIR)).replace('\\', '/'),
                'tags': [t.strip() for t in frontmatter.get('tags', '').split(',')] if frontmatter.get('tags') else [],
                'size': len(content.encode('utf-8'))
            })
        except Exception as e:
            print(f'Error processing {prompt_file}: {e}')

    return prompts


def index_instructions() -> List[Dict[str, Any]]:
    """Index instructions from .github/awesome-copilot-main/instructions"""
    instructions_dir = REFERENCE_DIR / 'instructions'
    if not instructions_dir.exists():
        print('No instructions directory found')
        return []

    instructions = []

    for instruction_file in instructions_dir.glob('*.instruction.md'):
        try:
            content = instruction_file.read_text(encoding='utf-8')
            frontmatter = parse_frontmatter(content)

            instructions.append({
                'name': frontmatter.get('name', instruction_file.stem.replace('.instruction', '')),
                'description': frontmatter.get('description', ''),
                'type': 'copilot-instruction',
                'path': str(instruction_file.relative_to(WORKSPACE_DIR)).replace('\\', '/'),
                'appliesTo': frontmatter.get('appliesTo', frontmatter.get('patterns', '')),
                'size': len(content.encode('utf-8'))
            })
        except Exception as e:
            print(f'Error processing {instruction_file}: {e}')

    return instructions


def build_index():
    """Build master index"""
    print('Building resource index...\n')

    skills = index_claude_skills()
    print(f'[OK] Indexed {len(skills)} Claude skills')

    agents = index_agents()
    print(f'[OK] Indexed {len(agents)} Copilot agents')

    prompts = index_prompts()
    print(f'[OK] Indexed {len(prompts)} Copilot prompts')

    instructions = index_instructions()
    print(f'[OK] Indexed {len(instructions)} Copilot instructions')

    master_index = {
        'generatedAt': datetime.utcnow().isoformat() + 'Z',
        'stats': {
            'totalResources': len(skills) + len(agents) + len(prompts) + len(instructions),
            'skills': len(skills),
            'agents': len(agents),
            'prompts': len(prompts),
            'instructions': len(instructions)
        },
        'resources': {
            'skills': skills,
            'agents': agents,
            'prompts': prompts,
            'instructions': instructions
        }
    }

    # Write master index
    index_path = OUTPUT_DIR / 'master-index.json'
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(master_index, f, indent=2)
    print(f'\n[OK] Master index written to {index_path.relative_to(WORKSPACE_DIR)}')

    # Write separate indexes for faster lookups
    (OUTPUT_DIR / 'skills-index.json').write_text(json.dumps(skills, indent=2), encoding='utf-8')
    (OUTPUT_DIR / 'agents-index.json').write_text(json.dumps(agents, indent=2), encoding='utf-8')
    (OUTPUT_DIR / 'prompts-index.json').write_text(json.dumps(prompts, indent=2), encoding='utf-8')
    (OUTPUT_DIR / 'instructions-index.json').write_text(json.dumps(instructions, indent=2), encoding='utf-8')

    print('[OK] Separate indexes written\n')

    # Print statistics
    total_size = sum(r['size'] for r in skills + agents + prompts + instructions)
    index_size = len(json.dumps(master_index).encode('utf-8'))

    print('Statistics:')
    print(f'  Total resources: {master_index["stats"]["totalResources"]}')
    print(f'  Total content size: {total_size / 1024:.2f} KB')
    print(f'  Index size: {index_size / 1024:.2f} KB')
    print(f'  Space savings: {(1 - index_size / total_size) * 100:.1f}%')


if __name__ == '__main__':
    build_index()
