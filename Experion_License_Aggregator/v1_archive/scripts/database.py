"""
SQLite Database Management for License History
Stores snapshots of license data for change detection.
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json


class LicenseDatabase:
    """Manage SQLite database for license history tracking."""
    
    def __init__(self, db_path: str = 'license_history.db'):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Main license snapshots table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS license_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_date TEXT NOT NULL,
                cluster TEXT NOT NULL,
                msid TEXT NOT NULL,
                system_number TEXT NOT NULL,
                product TEXT,
                release TEXT,
                customer TEXT,
                license_date TEXT,
                license_data TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(run_date, cluster, msid, system_number)
            )
        ''')
        
        # Index for fast lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_cluster_msid 
            ON license_snapshots(cluster, msid, system_number)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_run_date 
            ON license_snapshots(run_date DESC)
        ''')
        
        self.conn.commit()
    
    def save_snapshot(self, run_date: str, licenses: List[Dict]):
        """
        Save a snapshot of license data.
        
        Args:
            run_date: Date of this run (YYYY-MM-DD)
            licenses: List of license data dictionaries
        """
        cursor = self.conn.cursor()
        
        for lic in licenses:
            # Serialize all license options to JSON
            license_data = json.dumps({
                k: v for k, v in lic.items() 
                if k not in ['file_path', 'file_name', 'folder_name']
            })
            
            cursor.execute('''
                INSERT OR REPLACE INTO license_snapshots
                (run_date, cluster, msid, system_number, product, release, 
                 customer, license_date, license_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                run_date,
                lic['cluster'],
                lic['msid'],
                lic['system_number'],
                lic.get('product', ''),
                lic.get('release', ''),
                lic.get('customer', ''),
                lic.get('license_date', ''),
                license_data
            ))
        
        self.conn.commit()
        print(f"Saved {len(licenses)} licenses to database (run_date: {run_date})")
    
    def get_previous_snapshot(self, current_date: str) -> Optional[List[Dict]]:
        """
        Get the most recent snapshot before current_date.
        
        Args:
            current_date: Current run date (YYYY-MM-DD)
            
        Returns:
            List of license dictionaries or None if no previous snapshot
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT run_date
            FROM license_snapshots
            WHERE run_date < ?
            ORDER BY run_date DESC
            LIMIT 1
        ''', (current_date,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        previous_date = row['run_date']
        
        cursor.execute('''
            SELECT cluster, msid, system_number, product, release, 
                   customer, license_date, license_data
            FROM license_snapshots
            WHERE run_date = ?
        ''', (previous_date,))
        
        licenses = []
        for row in cursor.fetchall():
            lic = json.loads(row['license_data'])
            lic.update({
                'cluster': row['cluster'],
                'msid': row['msid'],
                'system_number': row['system_number'],
                'product': row['product'],
                'release': row['release'],
                'customer': row['customer'],
                'license_date': row['license_date']
            })
            licenses.append(lic)
        
        return licenses
    
    def detect_changes(self, current_licenses: List[Dict], 
                      previous_licenses: List[Dict]) -> List[Dict]:
        """
        Compare current licenses against previous snapshot.
        
        Args:
            current_licenses: Current license data
            previous_licenses: Previous snapshot data
            
        Returns:
            List of change dictionaries
        """
        changes = []
        
        # Create lookup for previous licenses
        prev_lookup = {
            (lic['cluster'], lic['msid'], lic['system_number']): lic
            for lic in previous_licenses
        }
        
        # Track fields to compare
        compare_fields = [
            'PROCESSPOINTS', 'SCADAPOINTS', 'STATIONS', 'MULTISTATIONS',
            'DIRECTSTATIONS', 'DUAL', 'DAS', 'API', 'SQL', 'TPS'
        ]
        
        for curr in current_licenses:
            key = (curr['cluster'], curr['msid'], curr['system_number'])
            prev = prev_lookup.get(key)
            
            if not prev:
                # New system
                changes.append({
                    'cluster': curr['cluster'],
                    'msid': curr['msid'],
                    'system_number': curr['system_number'],
                    'change_type': 'NEW',
                    'field': 'SYSTEM',
                    'old_value': None,
                    'new_value': 'New system added'
                })
                continue
            
            # Compare each field
            for field in compare_fields:
                curr_val = curr.get(field, 0)
                prev_val = prev.get(field, 0)
                
                if curr_val != prev_val:
                    changes.append({
                        'cluster': curr['cluster'],
                        'msid': curr['msid'],
                        'system_number': curr['system_number'],
                        'change_type': 'MODIFIED',
                        'field': field,
                        'old_value': prev_val,
                        'new_value': curr_val,
                        'delta': curr_val - prev_val
                    })
        
        return changes
    
    def purge_old_data(self, days_to_keep: int = 1095):  # 3 years
        """
        Remove snapshots older than specified days.
        
        Args:
            days_to_keep: Number of days to retain (default 3 years)
        """
        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime('%Y-%m-%d')
        
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM license_snapshots
            WHERE run_date < ?
        ''', (cutoff_date,))
        
        deleted = cursor.rowcount
        self.conn.commit()
        
        if deleted > 0:
            print(f"Purged {deleted} old snapshot records (before {cutoff_date})")
    
    def get_snapshot_dates(self) -> List[str]:
        """Get list of all snapshot dates in database."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT DISTINCT run_date
            FROM license_snapshots
            ORDER BY run_date DESC
        ''')
        return [row['run_date'] for row in cursor.fetchall()]
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


if __name__ == '__main__':
    # Test database operations
    with LicenseDatabase('test_licenses.db') as db:
        # Sample data
        test_licenses = [
            {
                'cluster': 'Carson',
                'msid': 'M0614',
                'system_number': '60806',
                'product': 'PKS',
                'PROCESSPOINTS': 5000,
                'SCADAPOINTS': 2000,
                'STATIONS': 10
            }
        ]
        
        # Save snapshot
        db.save_snapshot('2026-01-27', test_licenses)
        
        # Get snapshot dates
        dates = db.get_snapshot_dates()
        print(f"Snapshot dates: {dates}")
        
        # Purge old data
        db.purge_old_data(days_to_keep=365)
