"""
Process Controls Value Tracker - Data Enrichment Script
========================================================
This script enriches the work-history-entries.json with additional fields
for value demonstration analysis.

Usage:
    python enrich_entries.py --input data/work-history-entries.json --output output/enriched_entries.json

Author: Tony Chiu
Created: January 2026
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse


def load_json(filepath: str) -> Dict:
    """Load JSON file and return as dictionary."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict, filepath: str) -> None:
    """Save dictionary to JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)


def keyword_search(text: str, keywords: List[str], case_sensitive: bool = False) -> List[str]:
    """
    Search for keywords in text. Returns list of matched keywords.
    """
    if not text:
        return []
    
    search_text = text if case_sensitive else text.lower()
    matches = []
    
    for keyword in keywords:
        search_keyword = keyword if case_sensitive else keyword.lower()
        if search_keyword in search_text:
            matches.append(keyword)
    
    return matches


def is_amp_related(entry: Dict, amp_keywords: List[str]) -> bool:
    """Check if entry is AMP-related based on keywords."""
    text = entry.get('text', '')
    source = entry.get('source_file', '')
    combined = f"{text} {source}"
    
    matches = keyword_search(combined, amp_keywords)
    return len(matches) > 0


def is_obsolete_equipment(entry: Dict, obsolete_keywords: List[str]) -> bool:
    """Check if entry involves obsolete equipment."""
    text = entry.get('text', '')
    matches = keyword_search(text, obsolete_keywords)
    return len(matches) > 0


def categorize_root_cause(entry: Dict, categories: Dict) -> Dict[str, Any]:
    """
    Attempt to categorize root cause based on keywords.
    Returns dict with category and confidence.
    """
    text = entry.get('text', '')
    
    category_scores = {}
    
    for cat_name, cat_config in categories.items():
        keywords = cat_config.get('keywords', [])
        matches = keyword_search(text, keywords)
        if matches:
            category_scores[cat_name] = {
                'matches': matches,
                'count': len(matches)
            }
    
    if not category_scores:
        return {
            'category': 'unknown',
            'confidence': 'none',
            'matches': [],
            'needs_review': True
        }
    
    # Get category with most matches
    best_cat = max(category_scores.items(), key=lambda x: x[1]['count'])
    
    return {
        'category': best_cat[0],
        'confidence': 'high' if best_cat[1]['count'] >= 3 else 'medium' if best_cat[1]['count'] >= 2 else 'low',
        'matches': best_cat[1]['matches'],
        'all_categories': category_scores,
        'needs_review': best_cat[1]['count'] < 2
    }


def categorize_business_impact(entry: Dict, impact_keywords: Dict) -> Dict[str, Any]:
    """Categorize business impact based on keywords."""
    text = entry.get('text', '')
    
    impacts = []
    for impact_type, config in impact_keywords.items():
        keywords = config.get('keywords', [])
        matches = keyword_search(text, keywords)
        if matches:
            impacts.append({
                'type': impact_type,
                'matches': matches
            })
    
    if not impacts:
        return {
            'primary_impact': 'unknown',
            'all_impacts': [],
            'needs_review': True
        }
    
    return {
        'primary_impact': impacts[0]['type'],
        'all_impacts': impacts,
        'needs_review': False
    }


def identify_system_platform(entry: Dict, platforms: Dict) -> List[str]:
    """Identify which system platforms are mentioned in the entry."""
    text = entry.get('text', '')
    source = entry.get('source_file', '')
    combined = f"{text} {source}"
    
    identified = []
    for platform, keywords in platforms.items():
        if keyword_search(combined, keywords):
            identified.append(platform)
    
    return identified


def enrich_entry(entry: Dict, keywords_config: Dict) -> Dict:
    """
    Enrich a single entry with additional fields.
    Returns the enriched entry.
    """
    enriched = entry.copy()
    
    # AMP-related flag
    amp_keywords = keywords_config.get('amp_related', {}).get('keywords', [])
    enriched['amp_related'] = is_amp_related(entry, amp_keywords)
    
    # Obsolete equipment flag
    obsolete_keywords = keywords_config.get('obsolete_equipment', {}).get('keywords', [])
    enriched['obsolete_equipment'] = is_obsolete_equipment(entry, obsolete_keywords)
    
    # Root cause categorization
    root_cause_cats = keywords_config.get('root_cause_categories', {})
    enriched['root_cause'] = categorize_root_cause(entry, root_cause_cats)
    
    # Business impact
    impact_keywords = keywords_config.get('business_impact', {})
    enriched['business_impact'] = categorize_business_impact(entry, impact_keywords)
    
    # System platforms
    platforms = keywords_config.get('system_platforms', {})
    enriched['systems_involved'] = identify_system_platform(entry, platforms)
    
    # Fields for manual review (placeholders)
    enriched['manual_review'] = {
        'time_spent_hrs': None,
        'was_pc_job': None,  # Yes / No / Partial
        'notes': None,
        'reviewed': False,
        'reviewed_date': None
    }
    
    # Enrichment metadata
    enriched['enrichment'] = {
        'enriched_at': datetime.now().isoformat(),
        'version': '1.0'
    }
    
    return enriched


def enrich_all_entries(data: Dict, keywords_config: Dict, min_score: int = 0) -> Dict:
    """
    Enrich all entries in the data.
    Optionally filter by minimum score.
    """
    enriched_data = data.copy()
    enriched_data['ideas'] = []
    
    stats = {
        'total_processed': 0,
        'amp_related': 0,
        'obsolete_equipment': 0,
        'needs_review': 0,
        'by_root_cause': {},
        'by_business_impact': {},
        'by_system': {}
    }
    
    for entry in data.get('ideas', []):
        score = entry.get('score', 0)
        
        if score >= min_score:
            enriched = enrich_entry(entry, keywords_config)
            enriched_data['ideas'].append(enriched)
            
            # Update stats
            stats['total_processed'] += 1
            if enriched['amp_related']:
                stats['amp_related'] += 1
            if enriched['obsolete_equipment']:
                stats['obsolete_equipment'] += 1
            if enriched['root_cause'].get('needs_review'):
                stats['needs_review'] += 1
            
            # Count by category
            rc = enriched['root_cause']['category']
            stats['by_root_cause'][rc] = stats['by_root_cause'].get(rc, 0) + 1
            
            bi = enriched['business_impact']['primary_impact']
            stats['by_business_impact'][bi] = stats['by_business_impact'].get(bi, 0) + 1
            
            for sys in enriched['systems_involved']:
                stats['by_system'][sys] = stats['by_system'].get(sys, 0) + 1
    
    enriched_data['enrichment_stats'] = stats
    enriched_data['enrichment_metadata'] = {
        'enriched_at': datetime.now().isoformat(),
        'min_score_filter': min_score,
        'keywords_version': keywords_config.get('_metadata', {}).get('version', 'unknown')
    }
    
    return enriched_data


def print_summary(enriched_data: Dict) -> None:
    """Print a summary of the enrichment results."""
    stats = enriched_data.get('enrichment_stats', {})
    
    print("\n" + "="*60)
    print("ENRICHMENT SUMMARY")
    print("="*60)
    
    print(f"\nTotal entries processed: {stats.get('total_processed', 0)}")
    print(f"AMP-related entries: {stats.get('amp_related', 0)}")
    print(f"Obsolete equipment entries: {stats.get('obsolete_equipment', 0)}")
    print(f"Entries needing manual review: {stats.get('needs_review', 0)}")
    
    print("\n--- Root Cause Categories ---")
    for cat, count in sorted(stats.get('by_root_cause', {}).items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")
    
    print("\n--- Business Impact ---")
    for impact, count in sorted(stats.get('by_business_impact', {}).items(), key=lambda x: x[1], reverse=True):
        print(f"  {impact}: {count}")
    
    print("\n--- Systems Involved ---")
    for sys, count in sorted(stats.get('by_system', {}).items(), key=lambda x: x[1], reverse=True):
        print(f"  {sys}: {count}")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description='Enrich work history entries for value tracking')
    parser.add_argument('--input', '-i', required=True, help='Input JSON file path')
    parser.add_argument('--output', '-o', required=True, help='Output JSON file path')
    parser.add_argument('--keywords', '-k', default='config/keywords.json', help='Keywords config file')
    parser.add_argument('--min-score', '-m', type=int, default=0, help='Minimum score to process')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress summary output')
    
    args = parser.parse_args()
    
    # Load data
    print(f"Loading data from {args.input}...")
    data = load_json(args.input)
    print(f"Loaded {len(data.get('ideas', []))} entries")
    
    # Load keywords config
    print(f"Loading keywords from {args.keywords}...")
    keywords_config = load_json(args.keywords)
    
    # Enrich
    print(f"Enriching entries (min_score={args.min_score})...")
    enriched_data = enrich_all_entries(data, keywords_config, min_score=args.min_score)
    
    # Save
    print(f"Saving enriched data to {args.output}...")
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    save_json(enriched_data, args.output)
    
    # Print summary
    if not args.quiet:
        print_summary(enriched_data)
    
    print(f"\nDone! Enriched {enriched_data['enrichment_stats']['total_processed']} entries.")


if __name__ == '__main__':
    main()
