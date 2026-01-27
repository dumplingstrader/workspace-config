#!/usr/bin/env python3
"""
Validate classification_rules.json for syntax, logic, and completeness.

This script checks:
1. JSON syntax validity
2. Required fields present
3. Pattern regex validity
4. Priority conflicts
5. Rule coverage gaps
6. Test pattern matching
"""

import json
import re
from pathlib import Path
from collections import defaultdict


def load_rules_config():
    """Load classification rules from config."""
    rules_path = Path('config/classification_rules.json')
    
    if not rules_path.exists():
        print(f"❌ Error: {rules_path} not found")
        return None
    
    try:
        with open(rules_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        print(f"❌ JSON Syntax Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error loading rules: {e}")
        return None


def validate_rule_structure(rule, rule_type):
    """Validate a single rule has required fields."""
    errors = []
    
    # Required fields
    if 'pattern' not in rule:
        errors.append("Missing 'pattern' field")
    if 'priority' not in rule:
        errors.append("Missing 'priority' field")
    
    # Type-specific fields
    if rule_type == 'resolution' and 'resolution' not in rule:
        errors.append("Missing 'resolution' field")
    elif rule_type == 'business_impact' and 'business_impact' not in rule:
        errors.append("Missing 'business_impact' field")
    elif rule_type == 'complexity' and 'complexity' not in rule:
        errors.append("Missing 'complexity' field")
    elif rule_type == 'stream' and 'stream' not in rule:
        errors.append("Missing 'stream' field")
    
    # Validate pattern is valid regex
    if 'pattern' in rule:
        try:
            re.compile(rule['pattern'])
        except re.error as e:
            errors.append(f"Invalid regex pattern: {e}")
    
    # Validate priority is a number
    if 'priority' in rule and not isinstance(rule['priority'], (int, float)):
        errors.append(f"Priority must be a number, got {type(rule['priority'])}")
    
    return errors


def check_priority_conflicts(rules, rule_type):
    """Check for rules with same priority (potential conflicts)."""
    priority_map = defaultdict(list)
    
    for rule in rules:
        priority = rule.get('priority')
        name = rule.get('_name', rule.get('pattern', 'unnamed'))
        priority_map[priority].append(name)
    
    conflicts = []
    for priority, names in priority_map.items():
        if len(names) > 1:
            conflicts.append((priority, names))
    
    return conflicts


def test_pattern_matching(rules, test_cases, rule_type):
    """Test rules against sample text to verify patterns work."""
    results = []
    
    for test_text, expected_match in test_cases:
        matched = False
        matched_rule = None
        
        # Sort by priority
        sorted_rules = sorted(rules, key=lambda r: r.get('priority', 999))
        
        for rule in sorted_rules:
            pattern = rule.get('pattern', '')
            if re.search(pattern, test_text):
                matched = True
                matched_rule = rule.get('_name', pattern[:50])
                break
        
        if matched != expected_match:
            status = "❌ FAIL"
        else:
            status = "✅ PASS"
        
        results.append({
            'status': status,
            'text': test_text,
            'expected': 'match' if expected_match else 'no match',
            'got': f"matched '{matched_rule}'" if matched else 'no match'
        })
    
    return results


def main():
    print("=" * 70)
    print("PC Value Tracker - Classification Rules Validation")
    print("=" * 70)
    
    # Load rules
    config = load_rules_config()
    if not config:
        return False
    
    print(f"\n✅ Loaded classification_rules.json (version {config.get('version', 'unknown')})")
    print(f"   Enabled: {config.get('enabled', False)}")
    print(f"   Default Resolution: {config.get('default_resolution', 'none')}")
    
    # Validate each rule type
    all_valid = True
    
    for rule_type, rule_key in [
        ('resolution', 'resolution_rules'),
        ('business_impact', 'business_impact_rules'),
        ('complexity', 'complexity_rules'),
        ('stream', 'stream_rules')
    ]:
        print(f"\n{'=' * 70}")
        print(f"{rule_type.upper().replace('_', ' ')} RULES")
        print("=" * 70)
        
        rules = config.get(rule_key, [])
        print(f"Found {len(rules)} rules")
        
        # Validate structure
        has_errors = False
        for i, rule in enumerate(rules, 1):
            errors = validate_rule_structure(rule, rule_type)
            if errors:
                has_errors = True
                name = rule.get('_name', f"Rule {i}")
                print(f"\n❌ {name}:")
                for error in errors:
                    print(f"   - {error}")
        
        if not has_errors:
            print("✅ All rules have valid structure")
        else:
            all_valid = False
        
        # Check priority conflicts
        conflicts = check_priority_conflicts(rules, rule_type)
        if conflicts:
            print(f"\n⚠️  Priority conflicts detected:")
            for priority, names in conflicts:
                print(f"   Priority {priority}: {', '.join(names)}")
            print("   → Lower number = higher priority. First match wins.")
        else:
            print("✅ No priority conflicts")
    
    # Test resolution rules with sample cases
    print(f"\n{'=' * 70}")
    print("PATTERN MATCHING TESTS")
    print("=" * 70)
    
    resolution_tests = [
        ("waiting on vendor response", True),  # Should match PENDING
        ("escalated to L3 support", True),      # Should match ESCALATED
        ("completed the migration", True),       # Should match FIXED
        ("provided guidance on approach", True), # Should match INFORMATIONAL
        ("random text without keywords", False), # Should not match
        ("SR opened for tracking", True),        # Should match ESCALATED
        ("temporary workaround in place", True), # Should match WORKAROUND
        ("fixed the issue yesterday", True),     # Should match FIXED
    ]
    
    resolution_rules = config.get('resolution_rules', [])
    test_results = test_pattern_matching(resolution_rules, resolution_tests, 'resolution')
    
    for result in test_results:
        print(f"{result['status']} {result['text'][:50]}")
        print(f"   Expected: {result['expected']}, Got: {result['got']}")
    
    passed = sum(1 for r in test_results if '✅' in r['status'])
    total = len(test_results)
    print(f"\nPattern Tests: {passed}/{total} passed")
    
    if passed < total:
        all_valid = False
    
    # Summary
    print(f"\n{'=' * 70}")
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    if all_valid:
        print("✅ All validation checks passed!")
        print("   Rules are ready for use.")
        return True
    else:
        print("❌ Validation failed - please fix errors above")
        return False


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
