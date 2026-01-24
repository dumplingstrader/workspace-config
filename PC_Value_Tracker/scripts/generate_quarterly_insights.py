"""
Process Controls Value Tracker - Quarterly Insights Generator
==============================================================
Generates quarterly trend analysis and insights from master database
for strategic planning and improvement identification.

Usage:
    python scripts/generate_quarterly_insights.py --input data/master_combined.json --output output/quarterly_insights_2026-Q1.xlsx --quarter 2026-Q1

Author: Tony Chiu
Created: January 2026
"""

import pandas as pd
import json
from pathlib import Path
import argparse
from datetime import datetime
from collections import Counter


def load_data(json_path: Path) -> pd.DataFrame:
    """Load master database from JSON."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data.get('entries', []))
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df


def filter_by_quarter(df: pd.DataFrame, year: int, quarter: int) -> pd.DataFrame:
    """Filter data to specific quarter."""
    quarter_months = {
        1: [1, 2, 3],
        2: [4, 5, 6],
        3: [7, 8, 9],
        4: [10, 11, 12]
    }
    
    months = quarter_months[quarter]
    return df[(df['Date'].dt.year == year) & (df['Date'].dt.month.isin(months))]


def identify_recurring_issues(df: pd.DataFrame) -> pd.DataFrame:
    """Identify issues that appear multiple times."""
    
    if 'System' not in df.columns or 'Issue_Summary' not in df.columns:
        return pd.DataFrame()
    
    # Look for similar issues (same system + similar keywords)
    recurring = []
    
    # Group by system
    for system in df['System'].dropna().unique():
        system_issues = df[df['System'] == system]
        
        # Count occurrences of similar issues
        issue_summaries = system_issues['Issue_Summary'].dropna()
        
        # Simple keyword-based matching
        keywords = []
        for summary in issue_summaries:
            words = str(summary).lower().split()
            keywords.extend([w for w in words if len(w) > 4])  # Words longer than 4 chars
        
        keyword_counts = Counter(keywords)
        common_keywords = [k for k, v in keyword_counts.most_common(10) if v > 2]
        
        if common_keywords:
            recurring.append({
                'System': system,
                'Occurrence_Count': len(system_issues),
                'Common_Keywords': ', '.join(common_keywords[:5]),
                'Sample_Issue': issue_summaries.iloc[0] if len(issue_summaries) > 0 else ''
            })
    
    if not recurring:
        return pd.DataFrame()
    
    return pd.DataFrame(recurring).sort_values('Occurrence_Count', ascending=False)


def trend_analysis(df: pd.DataFrame, quarter_name: str) -> pd.DataFrame:
    """Analyze trends over the quarter."""
    
    # Group by month
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_counts = df.groupby('Month').size().reset_index(name='Issue_Count')
    monthly_counts['Month'] = monthly_counts['Month'].astype(str)
    
    # Calculate trend
    if len(monthly_counts) > 1:
        trend = "Increasing" if monthly_counts['Issue_Count'].iloc[-1] > monthly_counts['Issue_Count'].iloc[0] else "Decreasing"
    else:
        trend = "Insufficient data"
    
    return monthly_counts, trend


def training_needs_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Identify potential training needs based on recurring questions."""
    
    training_indicators = []
    
    # Look for patterns suggesting training needs
    if 'My_Role' in df.columns:
        consulting = df[df['My_Role'].str.contains('Consulting|Training|How-to', case=False, na=False)]
        
        if len(consulting) > 0:
            for system in consulting['System'].value_counts().head(5).index:
                system_consulting = consulting[consulting['System'] == system]
                training_indicators.append({
                    'System': system,
                    'Question_Count': len(system_consulting),
                    'Recommendation': f'Consider training on {system} basics'
                })
    
    return pd.DataFrame(training_indicators)


def equipment_reliability_concerns(df: pd.DataFrame) -> pd.DataFrame:
    """Identify equipment that generates high support burden."""
    
    if 'System' not in df.columns:
        return pd.DataFrame()
    
    system_issues = df['System'].value_counts().reset_index()
    system_issues.columns = ['System', 'Issue_Count']
    
    # Flag systems with >10 issues as potential concerns
    concerns = system_issues[system_issues['Issue_Count'] > 10].copy()
    concerns['Status'] = concerns['Issue_Count'].apply(
        lambda x: 'High Concern' if x > 20 else 'Monitor'
    )
    
    return concerns


def create_executive_summary(df: pd.DataFrame, quarter_name: str, metrics: dict) -> pd.DataFrame:
    """Create executive summary for leadership."""
    
    summary_data = [
        ['QUARTERLY INSIGHTS REPORT', ''],
        ['Period', quarter_name],
        ['', ''],
        ['KEY METRICS', ''],
        ['Total Issues Handled', metrics.get('total_issues', 0)],
        ['Average per Month', f"{metrics.get('avg_per_month', 0):.1f}"],
        ['Trend', metrics.get('trend', 'N/A')],
        ['', ''],
        ['TOP FINDINGS', ''],
    ]
    
    # Add top findings
    if 'top_system' in metrics:
        summary_data.append([f"Most Active System: {metrics['top_system']['name']}", 
                            f"{metrics['top_system']['count']} issues"])
    
    if 'recurring_count' in metrics:
        summary_data.append(['Recurring Issue Patterns Identified', metrics['recurring_count']])
    
    if 'training_needs' in metrics:
        summary_data.append(['Training Opportunities Identified', metrics['training_needs']])
    
    return pd.DataFrame(summary_data, columns=['Item', 'Value'])


def main():
    parser = argparse.ArgumentParser(description='Generate quarterly insights from master database')
    parser.add_argument('--input', default='data/master_combined.json', help='Master JSON database')
    parser.add_argument('--output', '-o', help='Output Excel file (e.g., output/quarterly_insights_2026-Q1.xlsx)')
    parser.add_argument('--quarter', required=True, help='Quarter in YYYY-QN format (e.g., 2026-Q1)')
    
    args = parser.parse_args()
    
    # Parse quarter
    try:
        year_str, quarter_str = args.quarter.split('-Q')
        year = int(year_str)
        quarter = int(quarter_str)
        if quarter not in [1, 2, 3, 4]:
            raise ValueError()
        quarter_name = f"Q{quarter} {year}"
    except:
        print(f"❌ Invalid quarter format. Use YYYY-QN (e.g., 2026-Q1)")
        return
    
    # Default output filename
    if not args.output:
        args.output = f'output/quarterly_insights_{args.quarter}.xlsx'
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        return
    
    print("\n" + "="*60)
    print(f"Quarterly Insights Generator - {quarter_name}")
    print("="*60)
    
    # Load data
    print(f"\n📊 Loading database: {input_path.name}")
    df = load_data(input_path)
    print(f"  ✓ Loaded {len(df)} total entries")
    
    # Filter to quarter
    df_quarter = filter_by_quarter(df, year, quarter)
    print(f"  ✓ Filtered to {len(df_quarter)} entries for {quarter_name}")
    
    if len(df_quarter) == 0:
        print(f"\n⚠️ No data found for {quarter_name}")
        return
    
    # Analyze data
    print(f"\n🔍 Analyzing trends and patterns...")
    
    # Trend analysis
    monthly_trends, trend = trend_analysis(df_quarter, quarter_name)
    print(f"  ✓ Trend: {trend}")
    
    # Recurring issues
    recurring = identify_recurring_issues(df_quarter)
    print(f"  ✓ Identified {len(recurring)} systems with recurring patterns")
    
    # Training needs
    training = training_needs_analysis(df_quarter)
    print(f"  ✓ Identified {len(training)} training opportunities")
    
    # Equipment reliability
    equipment_concerns = equipment_reliability_concerns(df_quarter)
    print(f"  ✓ Flagged {len(equipment_concerns)} systems for monitoring")
    
    # Calculate summary metrics
    metrics = {
        'total_issues': len(df_quarter),
        'avg_per_month': len(df_quarter) / 3,
        'trend': trend,
        'recurring_count': len(recurring),
        'training_needs': len(training)
    }
    
    if 'System' in df_quarter.columns:
        top_system = df_quarter['System'].value_counts().iloc[0]
        metrics['top_system'] = {
            'name': df_quarter['System'].value_counts().index[0],
            'count': top_system
        }
    
    # Generate report
    print(f"\n📝 Generating insights report...")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Executive summary
        summary_df = create_executive_summary(df_quarter, quarter_name, metrics)
        summary_df.to_excel(writer, sheet_name='Executive_Summary', index=False, header=False)
        print(f"  ✓ Created Executive_Summary")
        
        # Monthly trends
        monthly_trends.to_excel(writer, sheet_name='Monthly_Trends', index=False)
        print(f"  ✓ Created Monthly_Trends")
        
        # Recurring issues
        if not recurring.empty:
            recurring.to_excel(writer, sheet_name='Recurring_Issues', index=False)
            print(f"  ✓ Created Recurring_Issues ({len(recurring)} patterns)")
        
        # Training needs
        if not training.empty:
            training.to_excel(writer, sheet_name='Training_Needs', index=False)
            print(f"  ✓ Created Training_Needs")
        
        # Equipment concerns
        if not equipment_concerns.empty:
            equipment_concerns.to_excel(writer, sheet_name='Equipment_Reliability', index=False)
            print(f"  ✓ Created Equipment_Reliability")
        
        # Format Executive Summary
        worksheet = writer.sheets['Executive_Summary']
        worksheet.column_dimensions['A'].width = 50
        worksheet.column_dimensions['B'].width = 30
    
    print(f"\n{'='*60}")
    print(f"✓ Insights report saved: {output_path}")
    print('='*60)
    
    print(f"\n📊 Key Insights for {quarter_name}:")
    print(f"  • Total Issues: {metrics['total_issues']}")
    print(f"  • Average per Month: {metrics['avg_per_month']:.1f}")
    print(f"  • Trend: {metrics['trend']}")
    if 'top_system' in metrics:
        print(f"  • Most Active System: {metrics['top_system']['name']} ({metrics['top_system']['count']} issues)")
    print(f"  • Recurring Patterns: {metrics['recurring_count']}")
    print(f"  • Training Opportunities: {metrics['training_needs']}")


if __name__ == '__main__':
    main()
