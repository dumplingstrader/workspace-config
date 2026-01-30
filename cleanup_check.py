"""
Cleanup Check Script - Suggests file organization improvements

Scans a project directory and recommends files to move to _scratch/ or _output/.
Runs in dry-run mode by default. Use --fix to actually move files.
Checks Python files for unused imports by default (use --skip-imports to disable).

Usage:
    python cleanup_check.py [project_path] [--fix] [--skip-imports]

Examples:
    python cleanup_check.py Training/
    python cleanup_check.py SpendTracker/ --fix
    python cleanup_check.py . --skip-imports  # File organization only
"""

import os
import sys
import ast
from pathlib import Path
from typing import Dict, List, Tuple, Set
import argparse


# Files that should always stay at root level
ROOT_ALLOWED = {
    'README.md', 'HANDOFF.md', '_TODO.md', 'CLAUDE.md',
    '.gitignore', 'requirements.txt', 'setup.py', 'setup.ps1',
    'pyproject.toml', 'package.json', 'Dockerfile', 'docker-compose.yml',
    '.env.example', 'LICENSE', 'Makefile', 'cleanup_check.py'
}

# Main scripts (should stay at root) - common patterns
MAIN_SCRIPT_PATTERNS = [
    'main.py',
    'run_*.py',
    'consolidate_*.py',
    'generate_*.py',
    'process_*.py',
]

# Project-specific main scripts (add yours here)
# These exact filenames stay at root even if they match scratch patterns
PROJECT_MAIN_SCRIPTS = {
    'consolidate_training_data.py',
    'create_training_tracker.py',
    'run_tracker.ps1',
    'run_production_analysis.py',
}

# Prefixes/patterns that indicate one-off/debug work → _scratch/
SCRATCH_PREFIXES = ['check_', 'debug_', 'test_', 'temp_', 'tmp_', 'experiment_']
SCRATCH_SUFFIXES = ['_test', '_debug', '_temp', '_tmp', '_old', '_backup', '_v1', '_v2', '_v3']
SCRATCH_PATTERNS = [
    'test_*.py',
    'test*.py',
    '*_test.py',
    'check_*.py',
    'debug_*.py',
    'temp_*.py',
    'tmp_*.py',
    'experiment_*.py',
    '*.bak',
    '*.tmp',
    '*_backup.*',
    '*_old.*',
    '*_v[0-9].*',
]

# Keywords in filename suggesting scratch (conservative list)
SCRATCH_KEYWORDS = [
    'test', 'debug', 'temp', 'tmp', 'experiment', 'trial',
    'draft', 'backup', 'old', 'scratch', 'wip'
]

# Patterns that indicate generated output → _output/
OUTPUT_PATTERNS = [
    '*_output.*',
    '*_result.*',
    '*_report.*',
    '*Tracker.*',
    '*_Tracker.*',
    '*Report.*',
    '*_Report.*',
    '*Output.*',
    '*Final.*',
    '*Generated.*',
    'output.*',
    'result.*',
]

# Keywords suggesting generated output (conservative)
OUTPUT_KEYWORDS = [
    'tracker', 'report', 'output', 'result', 'generated',
    'summary', 'consolidated', 'compiled', 'final'
]

# System folders and files to ignore completely
IGNORE_FILES = {
    '.git', '__pycache__', '.venv', 'venv', 'node_modules',
    '.pytest_cache', '.mypy_cache', '.DS_Store', 'Thumbs.db'
}

# Input file threshold: Only suggest data/ folder if more than this many input files
INPUT_FILE_THRESHOLD = 20


def matches_pattern(filename: str, patterns: List[str]) -> bool:
    """Check if filename matches any glob pattern."""
    from fnmatch import fnmatch
    return any(fnmatch(filename.lower(), pattern.lower()) for pattern in patterns)


def contains_keyword(filename: str, keywords: List[str]) -> bool:
    """Check if filename contains any keyword."""
    filename_lower = filename.lower()
    return any(keyword in filename_lower for keyword in keywords)


def should_ignore(path: Path) -> bool:
    """Check if path should be ignored."""
    return path.name in IGNORE_FILES or any(ignore in str(path) for ignore in IGNORE_FILES)


def is_main_script(filename: str) -> bool:
    """Check if file is a main script that should stay at root."""
    # Exact match for project-specific main scripts
    if filename in PROJECT_MAIN_SCRIPTS:
        return True
    # Pattern match for common main script names
    return matches_pattern(filename, MAIN_SCRIPT_PATTERNS)


def find_unused_imports(filepath: Path) -> Set[str]:
    """
    Detect unused imports in a Python file using AST parsing.
    Returns set of import names that are imported but never used.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(filepath))
    except (SyntaxError, UnicodeDecodeError):
        # Skip files with syntax errors or encoding issues
        return set()
    
    imports = set()
    used_names = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name != '*':  # Skip wildcard imports
                    imports.add(alias.asname or alias.name)
        elif isinstance(node, ast.Name):
            used_names.add(node.id)
    
    return imports - used_names


def categorize_files(project_path: Path) -> Dict[str, List[Tuple[Path, str]]]:
    """
    Categorize files in project into: scratch, output, correct, or input.
    Returns dict with lists of (file_path, reason) tuples.
    """
    results = {
        'scratch': [],
        'output': [],
        'correct': [],
        'input': []
    }
    
    # Skip if already in organized folders
    organized_folders = {'_scratch', '_output', '_archive', '.github', 'scripts', 'config', 'data', 'docs'}
    
    for item in project_path.iterdir():
        if item.is_dir():
            if item.name in organized_folders:
                continue
            # Don't categorize subdirectories
            continue
            
        if should_ignore(item):
            continue
        
        filename = item.name
        
        # Files explicitly allowed at root
        if filename in ROOT_ALLOWED:
            results['correct'].append((item, "core project file"))
            continue
        
        # Main scripts stay at root
        if is_main_script(filename):
            results['correct'].append((item, "main script"))
            continue
        
        # Check for scratch patterns
        if matches_pattern(filename, SCRATCH_PATTERNS):
            reason = f"matches scratch pattern"
            results['scratch'].append((item, reason))
            continue
        
        # Check for scratch keywords
        if contains_keyword(filename, SCRATCH_KEYWORDS):
            reason = f"contains keyword suggesting experiment/test"
            results['scratch'].append((item, reason))
            continue
        
        # Check for output patterns
        if matches_pattern(filename, OUTPUT_PATTERNS):
            reason = f"matches output pattern"
            results['output'].append((item, reason))
            continue
        
        # Check for output keywords (but be more conservative)
        if contains_keyword(filename, OUTPUT_KEYWORDS):
            # Don't move if it looks like a main script
            if not is_main_script(filename):
                reason = f"appears to be generated output"
                results['output'].append((item, reason))
                continue
        
        # Check if it's a data/input file
        if item.suffix in ['.csv', '.xlsx', '.json', '.xml', '.txt'] and not item.name.startswith('_'):
            # Count similar files - only suggest data/ folder if many files
            similar_files = list(project_path.glob(f'*{item.suffix}'))
            if len(similar_files) > INPUT_FILE_THRESHOLD:
                results['input'].append((item, f"one of {len(similar_files)} {item.suffix} files - consider data/ folder"))
            else:
                results['correct'].append((item, "input file"))
            continue
        
        # Everything else stays at root
        results['correct'].append((item, "production file"))
    
    return results


def check_unused_imports(project_path: Path) -> Dict[Path, Set[str]]:
    """
    Check all Python files in project for unused imports.
    Returns dict of {file_path: set of unused imports}.
    """
    unused_by_file = {}
    
    # Find all Python files (skip _scratch, _archive, .venv, etc.)
    for py_file in project_path.rglob('*.py'):
        # Skip files in system/organized folders
        if any(skip in py_file.parts for skip in ['_scratch', '_archive', '.venv', 'venv', '__pycache__', '.git']):
            continue
        
        unused = find_unused_imports(py_file)
        if unused:
            unused_by_file[py_file.relative_to(project_path)] = unused
    
    return unused_by_file


def print_results(results: Dict[str, List[Tuple[Path, str]]], project_path: Path, fix: bool = False, unused_imports: Dict[Path, Set[str]] = None):
    """Print categorization results."""
    print("=" * 60)
    print(f"CLEANUP CHECK {'(executing moves)' if fix else '(dry-run)'}")
    print(f"Scanning: {project_path.absolute()}")
    print("=" * 60)
    print()
    
    total_suggestions = len(results['scratch']) + len(results['output']) + len(results['input'])
    
    if total_suggestions == 0:
        print("✓ No cleanup suggestions - project is well organized!")
        print()
        if results['correct']:
            print(f"✓ {len(results['correct'])} files at root (correct)")
    else:
        print(f"⚠️  {total_suggestions} files could be organized:")
        print()
        
        # Print scratch suggestions
        if results['scratch']:
            print("  → _scratch/  (experiments, tests, work in progress)")
            for file, reason in results['scratch']:
                print(f"      {file.name}")
                print(f"        (reason: {reason})")
            print()
        
        # Print output suggestions
        if results['output']:
            print("  → _output/  (generated files)")
            for file, reason in results['output']:
                print(f"      {file.name}")
                print(f"        (reason: {reason})")
            print()
        
        # Print input suggestions
        if results['input']:
            print("  → data/ or _input/  (input data files)")
            for file, reason in results['input']:
                print(f"      {file.name}")
                print(f"        (reason: {reason})")
            print()
        
        # Print files staying at root
        if results['correct']:
            print("✓ Files staying at root (correct):")
            for file, reason in results['correct']:
                print(f"      {file.name} ({reason})")
            print()
        
        print("-" * 60)
        if not fix:
            print("Run with --fix to move files automatically")
            print("Or manually review and move files as appropriate")
        else:
            print("Files moved. Review and adjust as needed.")
    
    # Print unused imports if provided
    if unused_imports is not None:
        print()
        print("=" * 60)
        print("UNUSED IMPORTS CHECK")
        print("=" * 60)
        print()
        
        if not unused_imports:
            print("✓ No unused imports detected")
        else:
            print(f"⚠️  Found unused imports in {len(unused_imports)} files:")
            print()
            for file, imports in sorted(unused_imports.items()):
                print(f"  {file}:")
                for imp in sorted(imports):
                    print(f"    • {imp}")
                print()
            print("Consider removing these imports to keep code clean.")


def execute_moves(results: Dict[str, List[Tuple[Path, str]]], project_path: Path):
    """Actually move files to suggested locations."""
    moved_count = 0
    
    # Create folders if they don't exist
    scratch_dir = project_path / '_scratch'
    output_dir = project_path / '_output'
    
    if results['scratch']:
        scratch_dir.mkdir(exist_ok=True)
        for file, _ in results['scratch']:
            dest = scratch_dir / file.name
            file.rename(dest)
            moved_count += 1
    
    if results['output']:
        output_dir.mkdir(exist_ok=True)
        for file, _ in results['output']:
            dest = output_dir / file.name
            file.rename(dest)
            moved_count += 1
    
    # Don't auto-move input files - just suggest
    if results['input']:
        print("\nNote: Input files not moved automatically. Consider creating data/ folder manually.")
    
    return moved_count


def main():
    parser = argparse.ArgumentParser(
        description='Check project for cleanup opportunities',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cleanup_check.py Training/
  python cleanup_check.py . --fix
  python cleanup_check.py SpendTracker/ --skip-imports
        """
    )
    parser.add_argument('project_path', nargs='?', default='.',
                        help='Path to project directory (default: current directory)')
    parser.add_argument('--fix', action='store_true',
                        help='Actually move files (default: dry-run only)')
    parser.add_argument('--skip-imports', action='store_true',
                        help='Skip checking Python files for unused imports')
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path).resolve()
    
    if not project_path.exists():
        print(f"Error: Path does not exist: {project_path}")
        sys.exit(1)
    
    if not project_path.is_dir():
        print(f"Error: Path is not a directory: {project_path}")
        sys.exit(1)
    
    # Categorize files
    results = categorize_files(project_path)
    
    # Check for unused imports by default (unless skipped)
    unused_imports = None
    if not args.skip_imports:
        unused_imports = check_unused_imports(project_path)
    
    # Print results
    print_results(results, project_path, args.fix, unused_imports)
    
    # Execute moves if --fix flag is set
    if args.fix:
        moved_count = execute_moves(results, project_path)
        print(f"\n✓ Moved {moved_count} files")


if __name__ == '__main__':
    main()
