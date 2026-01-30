"""
Deduplicator - Version-based duplicate removal for license data.

This module implements the deduplication strategy that selects the highest
version of each license when multiple XML files exist for the same system.

Strategy:
- Group licenses by unique_key (cluster, msid, system_number)
- Keep the version with highest file_version
- Track all removed duplicates for audit trail
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import defaultdict

from v2.models.license import LicenseData


@dataclass
class DeduplicationResult:
    """
    Result of deduplication operation with audit trail.
    
    Attributes:
        unique_licenses: List of deduplicated licenses (1 per system)
        duplicates_removed: List of licenses that were superseded
        conflicts: Dict mapping unique_key to list of conflicting versions
        stats: Summary statistics for reporting
    
    Examples:
        >>> result = deduplicator.deduplicate(licenses)
        >>> print(f"Kept {len(result.unique_licenses)}, removed {len(result.duplicates_removed)}")
        Kept 36, removed 8
    """
    unique_licenses: List[LicenseData]
    duplicates_removed: List[LicenseData]
    conflicts: Dict[Tuple[str, str, str], List[int]]
    stats: Dict[str, int]


class Deduplicator:
    """
    Version-based deduplication for license data.
    
    Implements the file versioning strategy where multiple XML files
    for the same system are reconciled by choosing the highest version.
    
    The deduplication key is (cluster, msid, system_number) from the
    unique_key property of LicenseData.
    
    Examples:
        >>> deduplicator = Deduplicator()
        >>> licenses = [
        ...     LicenseData(..., file_version=29),
        ...     LicenseData(..., file_version=40),  # Same system
        ... ]
        >>> result = deduplicator.deduplicate(licenses)
        >>> assert len(result.unique_licenses) == 1
        >>> assert result.unique_licenses[0].file_version == 40
    """
    
    def __init__(self):
        """Initialize deduplicator with empty state"""
        pass
    
    def deduplicate(self, licenses: List[LicenseData]) -> DeduplicationResult:
        """
        Remove duplicate licenses, keeping highest version for each system.
        
        Args:
            licenses: List of LicenseData instances (may contain duplicates)
        
        Returns:
            DeduplicationResult with unique licenses and audit trail
        
        Algorithm:
        1. Group licenses by unique_key
        2. For each group, select license with highest file_version
        3. Track removed duplicates and version conflicts
        4. Generate summary statistics
        
        Raises:
            ValueError: If licenses list is empty
        """
        if not licenses:
            raise ValueError("Cannot deduplicate empty license list")
        
        # Group licenses by unique key
        groups = defaultdict(list)
        for license_obj in licenses:
            key = license_obj.unique_key
            groups[key].append(license_obj)
        
        unique_licenses = []
        duplicates_removed = []
        conflicts = {}
        
        # Process each group
        for key, group in groups.items():
            if len(group) == 1:
                # No duplicates for this system
                unique_licenses.append(group[0])
            else:
                # Multiple versions exist - pick highest version
                sorted_group = sorted(group, key=lambda x: x.file_version, reverse=True)
                winner = sorted_group[0]
                losers = sorted_group[1:]
                
                unique_licenses.append(winner)
                duplicates_removed.extend(losers)
                
                # Track version conflict
                versions = [lic.file_version for lic in group]
                conflicts[key] = sorted(versions, reverse=True)
        
        # Calculate stats
        stats = {
            'total_input': len(licenses),
            'unique_systems': len(unique_licenses),
            'duplicates_removed': len(duplicates_removed),
            'systems_with_conflicts': len(conflicts)
        }
        
        return DeduplicationResult(
            unique_licenses=unique_licenses,
            duplicates_removed=duplicates_removed,
            conflicts=conflicts,
            stats=stats
        )
    
    def get_version_conflicts(
        self, 
        licenses: List[LicenseData]
    ) -> Dict[Tuple[str, str, str], List[int]]:
        """
        Identify systems with multiple versions without deduplicating.
        
        Args:
            licenses: List of LicenseData instances
        
        Returns:
            Dict mapping unique_key to list of file versions (sorted desc)
        
        Example:
            >>> conflicts = deduplicator.get_version_conflicts(licenses)
            >>> for key, versions in conflicts.items():
            ...     print(f"{key}: versions {versions}")
            ('Carson', 'M0614', '60806'): versions [40, 29, 28]
        """
        groups = defaultdict(list)
        for license_obj in licenses:
            key = license_obj.unique_key
            groups[key].append(license_obj.file_version)
        
        # Return only systems with conflicts (>1 version)
        conflicts = {}
        for key, versions in groups.items():
            if len(versions) > 1:
                conflicts[key] = sorted(set(versions), reverse=True)
        
        return conflicts
    
    def generate_conflict_report(
        self, 
        result: DeduplicationResult
    ) -> str:
        """
        Generate human-readable conflict report.
        
        Args:
            result: DeduplicationResult from deduplicate()
        
        Returns:
            Multi-line string report of version conflicts
        
        Example Output:
            Version Conflicts Report
            ========================
            Total systems: 36
            Systems with conflicts: 8
            
            Conflicts:
            - Carson/M0614/60806: versions [40, 29, 28] → kept v40
            - Carson/M0615/60807: versions [35, 30] → kept v35
        """
        lines = [
            "Version Conflicts Report",
            "=" * 24,
            f"Total systems: {result.stats['unique_systems']}",
            f"Systems with conflicts: {result.stats['systems_with_conflicts']}",
            ""
        ]
        
        if result.conflicts:
            lines.append("Conflicts:")
            for key, versions in sorted(result.conflicts.items()):
                cluster, msid, sys_num = key
                kept_version = max(versions)
                versions_str = str(versions)
                lines.append(
                    f"- {cluster}/{msid}/{sys_num}: versions {versions_str} "
                    f"→ kept v{kept_version}"
                )
        else:
            lines.append("No version conflicts detected")
        
        return "\n".join(lines)
