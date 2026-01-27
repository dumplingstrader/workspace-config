# ACM to APO Migration Comprehensive Checklist - Creation Summary

**Created**: January 27, 2026  
**Updated**: January 27, 2026 (Enhanced with Barbara's feedback)  
**Based on**: Barbara's APO_Deployment_Workflow_Checklist.xlsx + Whitepaper Outline  
**Output**: ACM_to_APO_Migration_Comprehensive_Checklist.xlsx

---

## Barbara's Feedback Implemented ✅

### 1. Better Format for Easy Add/Rearrange
✅ **Auto-numbering system** (1.1, 1.2, 2.1, etc.) - maintains section structure  
✅ **Hierarchical numbering** - Section.Item format for clear organization  
✅ **Collapsible sections** - Excel grouping/outlining for subsections (can expand/collapse)  
✅ **Enhanced color scheme** - Dark blue headers, light blue sections, subsections clearly marked  

### 2. Auto-Formatting with Colors
✅ **Status dropdown list** - ☐ Not Started, ⏳ In Progress, ✓ Complete, ✗ Blocked, ⚠️ On Hold  
✅ **Conditional formatting** based on Status:
   - ✓ Complete = Green background (auto-applied)
   - ⏳ In Progress = Light yellow background
   - ✗ Blocked = Red background
   - ☐ Not Started = Default (white)
✅ **Critical task highlighting** - Red fill for tasks with ⚠️ CRITICAL  
✅ **Warning task highlighting** - Yellow fill for WARNING/CAUTION tasks  

### 3. Easy to Add/Rearrange
✅ **Numbered sections** - Add new items and numbering maintains structure  
✅ **Subsection grouping** - Tasks grouped under subsections with indentation  
✅ **Consistent formatting** - New rows automatically inherit formatting  
✅ **Clear visual hierarchy** - Section → Subsection → Task levels  

---

## What Was Created

A comprehensive 11-sheet Excel workbook combining:
1. **Barbara's practical workflow structure** (her phase-based approach with Owner/Status/Notes columns)
2. **Detailed content from the whitepaper outline** (comprehensive tasks, lessons learned, critical warnings)

---

## Workbook Structure

### Sheet 1: Executive Summary
- ⚠️ **Top 5 Reasons for Delays & Cost Overruns**
  1. Misunderstanding of dependencies (HAMR first, hierarchies aligned)
  2. License miscalculation (30-40% ghost tags, cannot reclaim after ordering)
  3. IT-focused projects (quality/usability ignored)
  4. No pre-migration cleanup (months of work required)
  5. APO maturity gaps (management tools lacking)

- 📊 **Critical Success Factors** (Green/Yellow/Red status framework)
  - Database Health
  - License Sizing
  - Hierarchy Alignment
  - Custom Solutions
  - Training & Change Management
  - Post-Migration Support

### Sheet 2: Phase 0 - Pre-Assessment (6-12 months)
**3 Major Sections:**
1. **Database Health Assessment**
   - ACM DB Health Check (8 checks)
   - M&R DB Health Check (8 checks)
   - EAS EMDB Check (4 checks)

2. **Licensing Analysis**
   - True tag count calculation (exclude ghosts/invalids)
   - ⚠️ CRITICAL: Cannot reclaim licenses after ordering
   - 30-40% ghost tag potential savings

3. **Current System Dependencies**
   - Alarm Help configuration
   - Enforcement mappings (static + dynamic mode - highest risk)
   - Reporting schedules and custom reports

### Sheet 3: Phase 1 - Cleanup (Before License Order)
**3 Major Sections:**
1. **ACM Database Cleanup** (18 tasks)
   - Temporary environment setup
   - Tag cleanup (move to correct assets, fix corruptions)
   - Enforcement preparation
   - ⚠️ DISABLE enforcements in ACM DB before migration

2. **M&R Database Optimization** (7 tasks)
   - Ghost tag removal
   - Performance optimization
   - Retention adjustment

3. **Hierarchy Alignment Validation** (3 tasks)
   - ACM/M&R/EAS compatibility check
   - Console to Operating Position mapping

### Sheet 4: Phase 2 - Custom Solutions
**3 Major Sections:**
1. **Identify ACM→APO Feature Gaps** (8 gaps documented)
   - Tags import/export (only Excel tool in APO)
   - EMDB import/export (only manual)
   - TagSync functionality (missing)
   - BMA support (critical gap)

2. **Marathon Custom Solutions** (9 custom tools)
   - Synchronized backups across all servers
   - "You know before users notice" notifications
   - Daily health check scripts
   - Tag export/import tools
   - Tag Sync replacement

3. **Recommended Settings** (3 items)
   - HAMR rules/processing configuration
   - ACM site settings optimization

### Sheet 5: Phase 3 - Pre-Planning
**4 Major Sections:**
1. **Infrastructure Readiness** (8 tasks)
   - L4 APO server ordering and setup
   - SQL accounts and permissions
   - Email notifications and jobs

2. **Custom Solutions Readiness** (4 validation tasks)
   - ⚠️ CRITICAL: Consistent backup across all servers

3. **Known ACM-APO Gaps Review** (4 tasks)
   - ⚠️ WARNING: Old import files not valid anymore

4. **Installation Order** (4 sequence validations)
   - ⚠️ Do not install without cleanup and hierarchy adjustments first

### Sheet 6: Phase 4 - OSW Completion
**3 Major Sections:**
1. **OSW Data Entry** (5 tasks)
   - Asset hierarchy completion
   - Device inventory
   - External reference classification

2. **External Reference Configuration** (6 tasks)
   - ControlLogix, PLC5/SLC, Triconex
   - Bently Nevada, Analyzers
   - Connection strings documentation

3. **OSW Validation & Sign-Off** (7 tasks)
   - Hexagon and Site review
   - ⚠️ NO additions after sign-off without Change Order
   - Executive sponsor approval (scope locked)

### Sheet 7: Phase 5 - Deployment Readiness
**4 Major Sections:**
1. **Final Backups** (5 tasks)
   - Release all ACM consoles
   - Export all consoles, EMDBs
   - Purge M&R to ~6 months

2. **General Pre-Migration Checks** (6 validations)
   - ACM Test Server operational
   - Hierarchies optimal across all systems
   - Cleanup completion confirmed

3. **ACM DB Pre-Migration Preparation** (8 safety tasks)
   - Prevent accidental Enforce
   - Disable all Enforcements
   - Re-run and Disable TagSyncs
   - Delete BMA points if APO < 3.1

4. **ACM Health Checks** (3 repeat checks)
   - Compare to pre-cleanup baseline

### Sheet 8: Phase 6 - Migration Execution
**2 Major Sections:**
1. **Initial Migration** (8 vendor tasks)
   - Run APO migration tool
   - Import DCS, PLC, Safety configurations
   - Spot-check 10% of tags

2. **Initial APO Configuration** (5 setup tasks)
   - Configure consoles and map to HAMR OPs
   - User permissions
   - Health monitoring deployment

### Sheet 9: Phase 7 - Validation & Go-Live
**4 Major Sections:**
1. **Site Acceptance Testing (SAT)** (7 tests)
   - Asset search, signal tracing
   - Alarm configuration accuracy
   - User permissions verification

2. **Parallel Operations (30-90 days)** (5 parallel tasks)
   - Run ACM and APO concurrently
   - Compare enforcement results
   - Monitor performance

3. **User Training** (5 training sessions)
   - M&R refresher
   - ACM-APO "what was lost" training
   - Advanced rationalization expert training

4. **Go-Live Preparation** (8 tasks)
   - Freeze ACM configuration
   - Configure automated refresh/backups
   - Announce go-live date
   - Execute final backup

### Sheet 10: Phase 8 - Cutover
**3 Major Sections:**
1. **Cutover Day** (9 critical tasks)
   - Health check validation
   - Alarm Help verification
   - Switch TagSync
   - Disable ACM enforcements
   - ⚠️ Ensure no overlapping Enforcements or TagSyncs
   - Monitor first 24 hours continuously

2. **Post-Cutover Support (2-4 weeks)** (5 support tasks)
   - Monitor data import jobs
   - 48-hour issue response
   - 2-week and 1-month checkpoint meetings

3. **ACM Decommission** (9 cleanup tasks)
   - Delta migration review
   - ⚠️ KEEP ACM SERVER powered off but available
   - Un-DSA, uninstall clients
   - Disable L4 ACM Web

### Sheet 11: Phase 9 - Post-Migration
**3 Major Sections:**
1. **Performance Monitoring (First 90 days)** (4 metrics)
   - Alarm performance KPIs vs baseline
   - APO rationalization quality
   - User adoption tracking

2. **Continuous Improvement** (4 optimization tasks)
   - Refine alarm priorities
   - Implement APO recommendations
   - Enhance custom tools

3. **Standards Compliance Review** (3 audits)
   - ISA 18.2 compliance
   - EEMUA 191 KPI validation
   - Update Alarm Philosophy document

---

## Key Features

### From Barbara's Structure
✅ **Owner column** (Site, Vendor, Custom, IT/OT) - Clear accountability  
✅ **Status column** - Track progress (blank = to-do, can use ☐/☑/✓/✗)  
✅ **Notes column** - Document lessons learned, issues, decisions  
✅ **Prerequisites column** - Dependencies and sequence  
✅ **Phase-based organization** - Clear workflow progression  

### From Whitepaper Outline
✅ **Executive Summary with top failure reasons** - Learn from others' mistakes  
✅ **Comprehensive task lists** - Nothing missed  
✅ **Critical warnings highlighted** (⚠️) - Red/yellow cell formatting  
✅ **License calculation guidance** - 30-40% ghost tag impact  
✅ **Custom solutions documented** - Marathon-proven tools  
✅ **Training requirements** - "What was lost" focus  
✅ **Standards compliance** - ISA 18.2, EEMUA 191  

---

## How to Use This Checklist

### 1. Executive Summary Review (Week 1)
- Review top 5 failure reasons with stakeholders
- Assess current site against success factors (Green/Yellow/Red)
- Identify immediate gaps requiring attention

### 2. Phase 0 Assessment (Months 1-3)
- Run all health check scripts (Custom solutions may be needed)
- Calculate true license count (exclude ghosts - save 30-40%)
- **Decision point**: Order licenses or do cleanup first?

### 3. Phase 1 Cleanup (Months 3-6)
- Set up temporary ACM environment
- Execute 18-step ACM cleanup procedure
- Optimize M&R database
- **Milestone**: Sign-off on database health

### 4. Phases 2-3 Custom Solutions & Planning (Months 6-8)
- Identify gaps in APO vs ACM features
- Build/test Marathon custom solutions
- Order infrastructure (L4 server)
- **Milestone**: Custom solutions tested and ready

### 5. Phase 4 OSW Completion (Months 8-9)
- Complete Onsite Scoping Workbook
- External reference configuration
- **CRITICAL**: Executive sign-off (no additions after)

### 6. Phase 5 Deployment Readiness (Month 9-10)
- Final backups and exports
- Disable enforcements in ACM DB
- Repeat health checks
- **Milestone**: Migration execution approved

### 7. Phase 6 Migration Execution (Weeks 1-2)
- Vendor runs migration tool
- Site validates 10% of tags
- Configure APO consoles
- **Milestone**: APO operational in parallel

### 8. Phase 7 Validation (Months 10-12)
- Site Acceptance Testing (SAT)
- Parallel operations (30-90 days)
- User training (focus on "what was lost")
- **Milestone**: SAT passed, users trained

### 9. Phase 8 Cutover (Days 1-30)
- Cutover day (switch from ACM to APO)
- 24-hour continuous monitoring
- 2-week and 1-month checkpoints
- **Milestone**: ACM decommissioned, APO primary

### 10. Phase 9 Post-Migration (Months 1-3 after cutover)
- Monitor KPIs vs baseline
- Continuous improvement
- Standards compliance audit
- **Milestone**: Operational excellence achieved

---

## Critical Success Factors (From Executive Summary)

### ✅ Database Health
- **Green**: ACM health check passed, M&R optimized, <5% ghost tags
- **Yellow**: Some corruptions, 5-15% ghost tags, minor hierarchy issues
- **Red**: >15% ghost tags, major corruptions, hierarchy conflicts

### ✅ License Sizing
- **Green**: True count validated, ghost tags removed, 5-10% buffer
- **Yellow**: Count estimated, some ghosts remain, tight budget
- **Red**: Count based on current DB without cleanup, cannot reclaim excess

### ✅ Hierarchy Alignment
- **Green**: ACM/M&R/EAS paths compatible, consoles map to OPs
- **Yellow**: Minor misalignments, manual mapping needed
- **Red**: Major hierarchy conflicts, cannot proceed

### ✅ Custom Solutions
- **Green**: Marathon solutions deployed, tested, documented
- **Yellow**: Partial solutions, workarounds planned
- **Red**: No custom solutions, relying only on vendor tools

### ✅ Training & Change Management
- **Green**: Workflow changes documented, "what was lost" training complete
- **Yellow**: Basic training only, workflow impacts underestimated
- **Red**: No training plan, assume APO = ACM

### ✅ Post-Migration Support
- **Green**: 24/7 monitoring, custom tool support, issue response <48hrs
- **Yellow**: Business hours support, limited custom tool maintenance
- **Red**: Vendor-only support, no custom solutions expertise

---

## Files Created

1. **ACM_to_APO_Migration_Comprehensive_Checklist.xlsx** - Main deliverable
2. **create_comprehensive_checklist.py** - Generator script (for future updates)

---

## Next Steps

1. **Share with Barbara for review** - Validate tasks and Owner assignments
2. **Customize for specific site** - Add site-specific tasks, adjust timelines
3. **Populate Prerequisites column** - Define dependencies between tasks
4. **Create site-specific version** - Rename and track progress
5. **Update PROJECT_HANDOFF_SUMMARY.md** - Document this checklist creation

---

## Differences from Barbara's Original Checklist

### What We Kept
- ✅ Owner/Status/Notes/Prerequisites column structure
- ✅ Phase-based organization (0-7 phases)
- ✅ Critical warnings and safety checks
- ✅ Custom solutions emphasis

### What We Enhanced
- ✅ Added Executive Summary with top failure reasons
- ✅ Expanded from 7 to 9 phases (added Pre-Assessment and Post-Migration)
- ✅ Increased task count from ~150 to ~250+ comprehensive tasks
- ✅ Added specific content from whitepaper outline (license calculations, training needs)
- ✅ Highlighted critical tasks with ⚠️ symbols and colored cells
- ✅ Added standards compliance review (ISA 18.2, EEMUA 191)
- ✅ Documented all ACM→APO feature gaps
- ✅ Included Marathon custom solutions list

### What We Simplified
- ✅ Removed placeholder "Integrity" references (replaced with "Site" or specific roles)
- ✅ Consolidated duplicate checks
- ✅ Cleaner formatting with section headers

---

## Questions for Barbara

1. **Owner assignments**: Validate Site/Vendor/Custom/IT/OT for each task?
2. **Prerequisites**: Should we populate dependencies or leave blank for site-specific?
3. **Custom solutions**: Are all Marathon tools documented, or should we add more?
4. **Timeline**: 6-12 months realistic for pre-assessment + cleanup?
5. **Parallel operations**: 30-90 days sufficient, or site-dependent?

---

**End of Summary**
