# Experion HMI Graphics - Factory Acceptance Test (FAT) Support Document

---

## Executive Summary

This document provides a comprehensive framework for Factory Acceptance Testing (FAT) of Honeywell Experion HMI graphics. It is intended for project engineers, system integrators, and client stakeholders to ensure graphics meet design, performance, and compliance requirements prior to site deployment. The document covers pre-test setup, detailed validation checklists, troubleshooting, best practices, and references to applicable standards and guides.

## Document Control & Project Metadata

| Field                            | Value                                 |
| -------------------------------- | ------------------------------------- |
| **Project Name**           | __________________________            |
| **Project ID**             | __________________________            |
| **Site/Location**          | __________________________            |
| **Document Version**       | __________________________            |
| **Date Prepared**          | __________________________            |
| **Prepared By**            | __________________________            |
| **Vendor Name**            | __________________________            |
| **Vendor Contact**         | __________________________            |
| **Vendor Email**           | __________________________            |
| **Vendor Phone**           | __________________________            |
| **Marathon Petroleum PCE** | __________________________            |
| **Test Environment**       | ☐ Simulation  ☐ Factory  ☐ On-Site |
| **Experion Version**       | __________________________            |

---

## Document Purpose & Scope

This document provides structured guidance for conducting Factory Acceptance Testing (FAT) of Experion HMI graphics, ensuring compliance with:

- **Honeywell HMI Style Guide** (Reference: AMP-LAR-AUT-SPC-0050 Rev 1)
- **Experion HMI Specification** (R520)
- **Display Builder Assistant Performance Standards**

### FAT Objectives

1. Validate HMI graphics against approved design standards
2. Confirm performance compliance with Honeywell benchmarks
3. Document all deviations and corrective actions
4. Obtain formal acceptance signatures

---

<div style="page-break-before: always;"></div>

## 1. Pre-Test Setup

### 1.1 Validation Reports & Quality Checks

- ☐ **HMI Web Validation Checks** - Green checks obtained from HMI Web validation tool
- ☐ **HLV (High-Level Validation) Logs** - Clean logs with no new errors
- ☐ Existing critical errors in HLV logs **flagged for correction** with remediation plan
- ☐ **Review Reports Package** compiled including:
  - HMI Web validation check results
  - HLV log audit report
  - Individual graphics files for review
- ☐ Review package **sent to MPC Project team** (Tucker and/or PCE) with adequate review time before CFAT
- ☐ **CFAT Checklist/Procedure** included in review package for execution guidance

### 1.2 Design Approval & Sign-Offs

- ☐ **Sign-offs for initial design discussions and decisions** obtained and documented
- ☐ **Sign-offs for internal review** completed by project team
- ☐ **Sign-offs for third-party review** completed and approved
- ☐ All design approval documentation filed in project records

### 1.3 Final Approval & Implementation Readiness

- ☐ **Final approved graphics packages** sent to PCE for approval
- ☐ **PCE buy-off** obtained before implementation
- ☐ All pre-FAT deliverables documented and archived
- ☐ Confirmation that all prerequisite approvals are in place

### 1.4 Test Environment Preparation

- ☐ Install current Experion version: **____________________**
- ☐ Deploy graphics package version: **____________________**
- ☐ Configure test operator accounts with appropriate access levels
- ☐ Set up screen recording/documentation capture tools
- ☐ Prepare issue tracking log (Section 6)
- ☐ Establish communication channels with vendor support team

---

<div style="page-break-before: always;"></div>

## 2. HMI Graphics Validation Checklist

This section provides detailed checklists to validate HMI graphics for compliance with design standards, usability, performance, and alarm management. Each subsection targets a specific aspect of HMI graphics to ensure a thorough and consistent review process.

<div style="page-break-before: always;"></div>

### 2.1 Static Elements

Checklist for verifying static (non-changing) elements of HMI graphics, such as layout, labeling, and visual standards. Ensures all displays are consistent, readable, and meet project style requirements.

| Item # | Description                   | Acceptance Criteria                                                      | Pass | Fail | Notes/Issues | Ref. File/Line |
| ------ | ----------------------------- | ------------------------------------------------------------------------ | ---- | ---- | ------------ | -------------- |
| SE-01  | **Header/Title Block**  | Project name, unit ID, graphic ID present per style guide                | ☐ | ☐ |              |                |
| SE-02  | **Navigation Elements** | Home, back, forward buttons functional and consistently placed           | ☐ | ☐ |              |                |
| SE-03  | **Line Thickness**      | Process lines: 2pt; Instrument lines: 1pt per AMP-LAR-AUT-SPC-0050       | ☐ | ☐ |              |                |
| SE-04  | **Grayscale Standards** | Equipment/piping grayscale per ASM; color reserved for alarm/abnormal states | ☐ | ☐ |              |                |
| SE-05  | **Equipment Labels**    | All major equipment clearly labeled with tag numbers                     | ☐ | ☐ |              |                |
| SE-06  | **Background Color**    | Standard background color (typically #E0E0E0 or per spec)                | ☐ | ☐ |              |                |
| SE-07  | **Unit of Measure**     | Engineering units displayed for all analog values                        | ☐ | ☐ |              |                |
| SE-08  | **Graphic Borders**     | Consistent border style and thickness throughout displays                | ☐ | ☐ |              |                |
| SE-09  | **Button Styles**       | Uniform button appearance (size, shape, color, 3D effect)                | ☐ | ☐ |              |                |
| SE-10  | **Text Readability**    | All text legible at target screen resolution (1920x1080)                 | ☐ | ☐ |              |                |
| SE-11  | **Layer Organization**  | Graphics organized in logical layers (background, equipment, data)       | ☐ | ☐ |              |                |
| SE-12  | **Spacing & Density**   | Adequate white space; not overcrowded (< 60% screen coverage)            | ☐ | ☐ |              |                |
| SE-13  | **Flow Direction**      | Process flow indicated with arrows; direction consistent                 | ☐ | ☐ |              |                |
| SE-14  | **Status Indicators**   | Visual indicators for equipment state (running, stopped, fault)          | ☐ | ☐ |              |                |
| SE-15  | **Alarm Summary Area**  | Dedicated alarm banner/summary area visible on all displays              | ☐ | ☐ |              |                |

<div style="page-break-before: always;"></div>

### 2.2 Dynamic Elements

Checklist for dynamic (changing) elements, including real-time data, animations, and operator interactions. Focuses on correct behavior, feedback, and compliance with abnormal situation management (ASM) protocols.

| Item # | Description                          | Acceptance Criteria                                                        | Pass | Fail | Notes/Issues | Ref. File/Line |
| ------ | ------------------------------------ | -------------------------------------------------------------------------- | ---- | ---- | ------------ | -------------- |
| DE-01  | **Analog Values**              | Real-time values display with correct precision (e.g., XX.X)               | ☐ | ☐ |              |                |
| DE-02  | **Digital Status**             | ON/OFF, OPEN/CLOSED states update correctly                                | ☐ | ☐ |              |                |
| DE-03  | **Grayscale/ASM Compliance**   | Equipment grayscale during normal operation; color reserved for alarms/abnormal states | ☐ | ☐ |              |                |
| DE-04  | **Trend Pens**                 | Trend displays update in real-time; pen colors distinct                    | ☐ | ☐ |              |                |
| DE-05  | **Faceplates**                 | Right-click or button-click opens correct faceplate                        | ☐ | ☐ |              |                |
| DE-06  | **Point Detail Navigation**    | Double-click on point opens detail view with correct tag                   | ☐ | ☐ |              |                |
| DE-07  | **Setpoint Adjustment**        | Operator can modify setpoints; changes persist after save                  | ☐ | ☐ |              |                |
| DE-08  | **Mode Changes**               | Auto/Manual mode switches function; appropriate interlocks active          | ☐ | ☐ |              |                |
| DE-09  | **Alarm Shelving**             | Shelve/unshelve operations work; status indicators update                  | ☐ | ☐ |              |                |
| DE-10  | **Valve Position Indication**  | Valves show intermediate positions during travel (0-100%)                  | ☐ | ☐ |              |                |
| DE-11  | **Pump Status Animation**      | Running pumps show rotation/animation; stopped pumps static                | ☐ | ☐ |              |                |
| DE-12  | **Level Indication**           | Tank levels update dynamically; grayscale for normal, color for alarm states | ☐ | ☐ |              |                |
| DE-13  | **Setpoint Limits**            | High/low setpoint limits enforced; user notified on violation              | ☐ | ☐ |              |                |
| DE-14  | **Data Refresh Consistency**   | All points on display refresh at consistent rate (no stale data)           | ☐ | ☐ |              |                |
| DE-15  | **Out-of-Service Indication**  | Equipment in maintenance mode clearly marked (hatched/grayed)              | ☐ | ☐ |              |                |

<div style="page-break-before: always;"></div>

### 2.3 Navigation & Usability

Checklist for navigation structure and usability features. Ensures operators can efficiently move between displays, access information, and use controls with minimal effort.

| Item # | Description                             | Acceptance Criteria                                                      | Pass | Fail | Notes/Issues | Ref. File/Line |
| ------ | --------------------------------------- | ------------------------------------------------------------------------ | ---- | ---- | ------------ | -------------- |
| NU-01  | **Breadcrumb Navigation**         | Current location in hierarchy shown; clickable path navigation           | ☐ | ☐ |              |                |
| NU-02  | **Context Menu Functionality**    | Right-click menus provide relevant actions (trends, faceplates, details) | ☐ | ☐ |              |                |
| NU-03  | **Keyboard Shortcuts**            | Common shortcuts work (F5=refresh, Esc=close, Tab=navigate)              | ☐ | ☐ |              |                |
| NU-04  | **Display Hierarchy Consistency** | Overview → Area → Unit → Detail navigation structure maintained       | ☐ | ☐ |              |                |
| NU-05  | **Search Functionality**          | Tag/equipment search works; results clickable to navigate                | ☐ | ☐ |              |                |
| NU-06  | **Multi-Monitor Support**         | Displays scale/position correctly across multiple screens                | ☐ | ☐ |              |                |
| NU-07  | **Back Button Behavior**          | Back button returns to previously viewed display (history stack)         | ☐ | ☐ |              |                |
| NU-08  | **Pop-up Window Management**      | Faceplates open as modeless windows; don't block main display            | ☐ | ☐ |              |                |
| NU-09  | **Display Launch Speed**          | Displays accessible within 3 clicks from home screen                     | ☐ | ☐ |              |                |
| NU-10  | **Print Functionality**           | Display print/screenshot captures current state accurately               | ☐ | ☐ |              |                |
| NU-11  | **Responsiveness**                | No lag or delay in button clicks; immediate visual feedback              | ☐ | ☐ |              |                |

<div style="page-break-before: always;"></div>

### 2.4 Alarm & Event Management

Checklist for alarm and event handling in graphics. Validates alarm visibility, navigation, operator actions, and compliance with alarm philosophy and ASM color standards.

| Item # | Description                        | Acceptance Criteria                                                   | Pass | Fail | Notes/Issues | Ref. File/Line |
| ------ | ---------------------------------- | --------------------------------------------------------------------- | ---- | ---- | ------------ | -------------- |
| AE-01  | **Alarm Banner Visibility**  | Alarm banner shows latest unacked alarms; auto-updates                | ☐ | ☐ |              |                |
| AE-02  | **Alarm Sound Notification** | Audible alarm on new high-priority alarms; silence button works       | ☐ | ☐ |              |                |
| AE-03  | **Alarm Filtering**          | Users can filter alarms by area, priority, state                      | ☐ | ☐ |              |                |
| AE-04  | **Alarm Sorting**            | Alarms sortable by time, priority, tag, or area                       | ☐ | ☐ |              |                |
| AE-05  | **Alarm Navigation**         | Clicking alarm jumps to associated graphic with highlighted equipment | ☐ | ☐ |              |                |
| AE-06  | **Alarm Comment Capability** | Operators can add comments to alarms for shift turnover               | ☐ | ☐ |              |                |
| AE-07  | **Event Logging**            | Operator actions logged (setpoint changes, mode switches, acks)       | ☐ | ☐ |              |                |
| AE-08  | **Alarm Return to Normal**   | Alarms clear when process returns to normal; RTN logged               | ☐ | ☐ |              |                |
| AE-09  | **Alarm Color Standards**    | Alarm colors per ASM standards (Critical=Red, High=Orange, Medium=Yellow) | ☐ | ☐ |              |                |

<div style="page-break-before: always;"></div>

### 2.5 Performance Metrics

Checklist for performance-related criteria, including display load times, data update rates, and script execution. Ensures graphics meet Honeywell and project-specific performance benchmarks.

| Item # | Description                          | Benchmark/Target                                     | Measured Value  | Pass | Fail | Notes |
| ------ | ------------------------------------ | ---------------------------------------------------- | --------------- | ---- | ---- | ----- |
| PM-01  | **Display Call-Up Time**       | < 2 seconds (simple) / < 5 seconds (complex)         | _______ sec     | ☐ | ☐ |       |
| PM-02  | **Data Update Rate**           | 1-2 seconds for critical parameters                  | _______ sec     | ☐ | ☐ |       |
| PM-03  | **Trend Update Latency**       | < 2 seconds from controller to display               | _______ sec     | ☐ | ☐ |       |
| PM-04  | **Max Trend Pens per Display** | ≤ 8 pens recommended (per Honeywell guidance)       | _______ pens    | ☐ | ☐ |       |
| PM-05  | **Trend Sampling Rate**        | Not exceeding 1 second intervals for performance     | _______ sec     | ☐ | ☐ |       |
| PM-06  | **DOM Node Count**             | < 1500 nodes per graphic (Display Builder Assistant) | _______ nodes   | ☐ | ☐ |       |
| PM-07  | **Script Execution Time**      | < 100ms for OnChange/OnTimer events (R520)           | _______ ms      | ☐ | ☐ |       |
| PM-08  | **Memory Usage per Display**   | Monitor for excessive growth (baseline + 20% max)    | _______ MB      | ☐ | ☐ |       |
| PM-09  | **Concurrent Display Load**    | Test with 3-5 displays open; no degradation          | ☐ | ☐ |                 |       |
| PM-10  | **Navigation Responsiveness**  | Button clicks respond within 500ms                   | _______ ms      | ☐ | ☐ |       |

<div style="page-break-before: always;"></div>

### 2.6 Compliance & Standards

Checklist for adherence to referenced standards, specifications, and project requirements.

| Item # | Description                         | Standard Reference                   | Pass | Fail | Notes/Issues | Action Required |
| ------ | ----------------------------------- | ------------------------------------ | ---- | ---- | ------------ | --------------- |
| CS-01  | **Line Thickness Compliance** | AMP-LAR-AUT-SPC-0050 Rev 1 § 3.2    | ☐ | ☐ |              |                 |
| CS-02  | **Color Palette Adherence**   | AMP-LAR-AUT-SPC-0050 Rev 1 § 3.3    | ☐ | ☐ |              |                 |
| CS-03  | **Font Standards**            | AMP-LAR-AUT-SPC-0050 Rev 1 § 3.4    | ☐ | ☐ |              |                 |
| CS-04  | **Alarm Iconography**         | AMP-LAR-AUT-SPC-0050 Rev 1 § 4.1    | ☐ | ☐ |              |                 |
| CS-05  | **Window Management**         | Experion HMI Spec R520 § 2.3        | ☐ | ☐ |              |                 |
| CS-07  | **Script Optimization**       | R520 Scripting Guidance § 6.1       | ☐ | ☐ |              |                 |
| CS-08  | **Point Naming Convention**   | Project Tag Database Standards       | ☐ | ☐ |              |                 |
| CS-09  | **Alarm Priority Mapping**    | Experion Alarm Philosophy Document   | ☐ | ☐ |              |                 |
| CS-10  | **Security/Access Control**   | Operator authority levels per design | ☐ | ☐ |              |                 |

---

<div style="page-break-before: always;"></div>

## 3. Troubleshooting Guide

### 3.1 Using Experion HLV Log for Script Error Troubleshooting

The High-Level Validation (HLV) log is a critical diagnostic tool for identifying and resolving script errors in Experion HMI graphics. This section provides guidance on how to effectively use the HLV log during FAT.

#### Accessing the HLV Log

**Location:**

- Access via **Experion PKS Server Log** on the Experion server
- Quick access: Click Windows search (magnifying glass) and type "HLV" to launch Experion PKS Server Log
- HLV log file is located at: `C:\ProgramData\Honeywell\HMIWebLog\Log.txt`

**Real-Time Monitoring:**

- Use the **logServer.txt** tab in Experion PKS Server Log to view errors in real-time
- Errors appear as HMIWeb graphics are brought up on operator stations
- Monitor this tab during FAT testing to immediately identify script errors

#### Understanding HLV Log Entries

HLV log entries are categorized by severity:

| Severity Level    | Description                                         | Action Required                       |
| ----------------- | --------------------------------------------------- | ------------------------------------- |
| **ERROR**   | Critical issues that prevent display operation      | Immediate correction required         |
| **WARNING** | Potential issues that may cause unexpected behavior | Review and fix before production      |
| **INFO**    | Informational messages about validation process     | Review for optimization opportunities |

#### Common Script Errors in HLV Log

##### Error 1: Undefined Variable/Object Reference

**HLV Log Entry Example:**

```
ERROR [2026-01-07 14:23:15] Display: P101_Overview.htm
Line 127: ReferenceError: 'pumpSpeed' is not defined
Script Block: OnChange event handler
```

**Root Cause:**

- Variable declared in script but not initialized
- Typo in variable name
- Variable scope issue (local vs. global)

**Resolution:**

1. Open the graphic in Display Builder
2. Navigate to the reported line number (Line 127)
3. Verify variable declaration: `var pumpSpeed = 0;`
4. Check spelling matches all references in the script
5. Ensure variable is accessible in the event handler scope
6. Re-validate graphic and check HLV log for clearance

---

##### Error 2: Invalid Point Binding Syntax

**HLV Log Entry Example:**

```
ERROR [2026-01-07 14:25:42] Display: TK101_Level.htm
Line 89: Invalid binding syntax - Expected format: 'CM.TAG.PARAMETER'
Binding: 'CM.TANK_TK101.LVL.PV' (extra dot notation)
```

**Root Cause:**

- Incorrect point binding format
- Extra or missing delimiters
- Binding to non-existent parameter

**Resolution:**

1. Locate the binding in the graphic (Line 89)
2. Verify correct binding syntax: `CM.TANK_TK101.LVL_PV`
3. Cross-reference with Control Builder tag database
4. Update binding in Display Builder
5. Test binding with live data connection
6. Confirm error cleared in HLV log

---

##### Error 3: Script Execution Timeout

**HLV Log Entry Example:**

```
WARNING [2026-01-07 14:30:18] Display: Process_Overview.htm
Script execution exceeded 500ms threshold
Event: OnTimer (interval: 1000ms)
Execution Time: 847ms - Consider optimization
```

**Root Cause:**

- Heavy processing in timer events
- Synchronous data calls blocking execution
- Inefficient loops or calculations

**Resolution:**

1. Review the OnTimer event script
2. Identify performance bottlenecks:
   - Move complex calculations to OnChange events
   - Batch multiple point reads into single request
   - Use asynchronous callbacks for data retrieval
3. Increase timer interval if appropriate (e.g., 1000ms → 2000ms)
4. Re-test and verify execution time < 100ms (per R520 guidance)
5. Document optimization in graphic change log

---

##### Error 4: Type Mismatch / Data Conversion Error

**HLV Log Entry Example:**

```
ERROR [2026-01-07 14:35:55] Display: V201_Valve.htm
Line 156: TypeError: Cannot convert 'OPEN' to numeric value
Attempted operation: valvePosition = status + 10
```

**Root Cause:**

- Attempting arithmetic on string/text values
- Incorrect data type returned from point binding
- Missing type conversion function

**Resolution:**

1. Identify the variable types involved (Line 156)
2. Add explicit type conversion:
   ```javascript
   var valvePosition = parseInt(status) + 10;
   // or use parseFloat() for decimal values
   ```
3. Validate data type from point binding (should be numeric)
4. Add error handling:
   ```javascript
   if (!isNaN(status)) {
       valvePosition = parseInt(status) + 10;
   }
   ```
5. Test with various input values
6. Verify HLV log shows no errors

---

##### Error 5: Missing or Corrupted Script Library

**HLV Log Entry Example:**

```
ERROR [2026-01-07 14:40:22] Display: Multiple displays affected
Cannot load script library: 'CommonFunctions.js'
Path: /HMIWeb/Scripts/CommonFunctions.js
HTTP Status: 404 Not Found
```

**Root Cause:**

- Script library file missing from server
- Incorrect file path reference
- File permissions issue

**Resolution:**

1. Verify file exists at specified path on Experion server
2. Check file permissions (IIS_IUSRS should have Read access)
3. If missing, restore from backup or source control
4. Update file path in affected graphics if location changed
5. Restart IIS or HMIWeb service if necessary
6. Clear browser cache on operator stations
7. Verify all displays load correctly

---

#### HLV Log Analysis Workflow

**Step 1: Extract and Filter Logs**

```powershell
# PowerShell command to filter ERROR entries
Get-Content "C:\ProgramData\Honeywell\HMIWebLog\Log.txt" | 
Select-String "ERROR" | 
Out-File "HLV_Errors_Summary.txt"
```

**Step 2: Categorize Errors by Display**

- Group errors by graphic file name
- Prioritize displays with multiple errors
- Identify patterns (same error across multiple displays)

**Step 3: Create Remediation Matrix**

| Display              | Error Type         | Line # | Severity | Status      | Assigned To | Target Date |
| -------------------- | ------------------ | ------ | -------- | ----------- | ----------- | ----------- |
| P101_Overview.htm    | Undefined Variable | 127    | ERROR    | Open        | Developer   | 2026-01-10  |
| TK101_Level.htm      | Invalid Binding    | 89     | ERROR    | In Progress | Developer   | 2026-01-09  |
| Process_Overview.htm | Script Timeout     | -      | WARNING  | Open        | Developer   | 2026-01-12  |

**Step 4: Fix, Test, and Verify**

1. Implement fix in Display Builder
2. Save and deploy updated graphic
3. Re-run HLV validation
4. Check HLV log for clearance
5. Document fix in change log
6. Move to next error

**Step 5: Final Clean HLV Log Verification**

- Run full HLV validation on all graphics
- Confirm zero ERROR entries
- Review and document any remaining WARNING entries
- Archive clean HLV log as FAT deliverable

---

#### Best Practices for HLV Log Management

- ✓ **Run HLV validation after every graphic change**
- ✓ **Address ERROR-level issues immediately**
- ✓ **Document all WARNING-level items with justification**
- ✓ **Maintain HLV log history for trend analysis**
- ✓ **Include clean HLV log in FAT acceptance package**
- ✓ **Use HLV log as first diagnostic tool for runtime issues**
- ✓ **Set up automated HLV log monitoring in production**

---

### 3.2 Additional Common Issues & Resolutions

#### Issue 1: Display Call-Up Time Exceeds Performance Target

**Symptoms:**

- Graphics load slowly (> 5 seconds)
- Screen freezes during navigation
- CPU usage spikes when opening displays

**Root Causes:**

- Excessive DOM nodes (> 1500)
- Heavy VBScript in OnTimer or OnChange events
- Too many concurrent trend pens
- Large image files not optimized

**Resolution Steps:**

1. Run Display Builder Assistant on affected graphics
2. Review performance report for flagged items:
   - Reduce DOM complexity (flatten nested groups)
   - Optimize scripts (move logic from OnTimer to change-based events)
   - Limit trend pens to ≤ 8 per display
   - Compress/optimize image resources
3. Implement recommended changes
4. Re-test call-up time
5. Document performance improvement

**Display Builder Assistant Report Location:**

```
<Project_Root>\Reports\DisplayPerformance_<timestamp>.xml
```

---

#### Issue 2: Overloaded Graphics Exceeding Performance Benchmarks

**Symptoms:**

- Display Analysis report shows values exceeding recommended thresholds
- DOM node count > 1500
- Script execution time > 100ms
- Call-up time exceeds performance targets

**Root Causes:**

- Complex nested groupings and layering
- Excessive use of dynamic objects on single display
- Unoptimized scripts running on timer events
- Large embedded images or unnecessary visual elements

**Resolution Steps:**

1. Review Display Builder Assistant analysis report
2. Identify specific metrics exceeding thresholds:
   - DOM nodes, script timing, memory usage
3. Simplify graphics:
   - Break complex displays into multiple screens (overview → detail hierarchy)
   - Remove redundant or non-critical visual elements
   - Use shared symbols/templates instead of duplicating objects
4. Optimize scripting:
   - Replace OnTimer with OnChange events where possible
   - Consolidate repetitive code into functions
   - Remove unnecessary data reads
5. Re-run Display Analysis to verify improvements
6. Document changes and retest performance metrics (Section 2.5)

**Performance Target Reference:**

- DOM Nodes: < 1500 (PM-06)
- Script Execution: < 100ms (PM-07)
- Call-Up Time: < 5 seconds complex displays (PM-01)

---

### 3.3 Persistent Anomalies - Escalation Path

If issues persist after applying documented resolutions:

1. **Gather diagnostic data:**

   - System event logs (Experion and controllers)
   - Screen recordings demonstrating issue
   - Configuration export files
   - Network trace (if communication-related)
2. **Review advanced documentation:**

   - Honeywell Experion PKS Release Notes
   - Experion HMI Configuration Guide
   - Product bulletins for known issues
3. **Escalate to Honeywell support:**

   - Open support case via Honeywell Customer Portal
   - Provide project metadata (see Document Control section)
   - Attach diagnostic data package
   - Reference this FAT document and specific test item numbers

**Honeywell Support Contact:**

- Portal: [https://support.honeywell.com](https://support.honeywell.com)
- Phone: __________________________ (insert regional support number)
- Email: __________________________ (insert support email)

---

<div style="page-break-before: always;"></div>

## 4. Best Practices & Performance Optimization

### 4.1 Graphics Design Guidelines

✓ **Limit graphics complexity** to maintain operator station performance:

- Target < 1500 DOM nodes per display
- Avoid deeply nested groups (max 3 levels)
- Use shared graphics/symbols for repeated elements

✓ **Optimize scripting:**

- Prefer change-driven events (OnChange) over polling (OnTimer)
- Batch parameter reads instead of individual calls
- Avoid synchronous operations in event handlers
- Keep script execution time < 100ms

✓ **Trend configuration:**

- Limit to ≤ 8 pens per trend widget
- Set appropriate sampling rates (not < 1 second)
- Consider separate displays for high-frequency vs. historical trends

✓ **Image resources:**

- Use PNG format with appropriate compression
- Avoid embedding large images (> 100KB)
- Reuse image assets across displays

### 4.2 Testing & Validation Tools

✓ **Use Honeywell Display Builder Assistant:**

- Run performance analysis on all graphics before FAT
- Address all HIGH severity findings
- Review MEDIUM findings with Honeywell guidance
- Generate baseline performance report for acceptance

✓ **Implement version control:**

- Maintain graphics in source control (e.g., Git, SVN)
- Tag releases with version numbers
- Document change history in commit messages
- Archive approved FAT baseline

✓ **Conduct peer reviews:**

- Have second engineer review complex graphics
- Validate against style guide checklist
- Test on target hardware configuration

### 4.3 Maintenance Considerations

✓ **Document customizations:**

- Note any deviations from standard templates
- Explain rationale for custom scripting
- Provide maintenance instructions for complex logic

✓ **Operator training materials:**

- Include annotated screenshots in training docs
- Highlight navigation paths
- Explain alarm response procedures

✓ **Backup and recovery:**

- Establish backup schedule for graphics configuration
- Document restore procedure
- Test recovery process before site deployment

---

<div style="page-break-before: always;"></div>

## 5. Deliverables & Acceptance Criteria

### 5.1 Required Deliverables

- ☐ **Completed FAT Checklist** (this document) with all sections marked Pass/Fail
- ☐ **Issue Log** (Section 6) with documented resolutions
- ☐ **Performance Metrics Report** (extracted from Section 2.3)
- ☐ **Display Builder Assistant Reports** (for all tested graphics)
- ☐ **Point Mapping Validation Spreadsheet** (Section 3)
- ☐ **Screen Recordings** of critical operations
- ☐ **Updated Graphics Package** (final version tested and accepted)
- ☐ **Configuration Backup Files** (Experion export)
- ☐ **As-Built Documentation** reflecting any changes during FAT

### 5.2 Acceptance Criteria

**FAT is considered PASSED when:**

- [ ] All checklist items in Section 2 marked "Pass" OR documented deviations approved by project stakeholders
- [ ] Performance metrics (Section 2.5) meet or exceed benchmarks
- [ ] All HIGH severity issues resolved (Section 6)
- [ ] MEDIUM severity issues documented with resolution plan
- [ ] Deliverables (Section 5.1) completed and submitted
- [ ] Formal signatures obtained (Section 7)

**Conditional Acceptance:**

If minor issues remain, document as "Conditional Pass" with:

- List of outstanding items
- Assigned responsibility for resolution
- Target completion date
- Re-test plan

---

<div style="page-break-before: always;"></div>

## 6. Issue Tracking Log

| Issue # | Date Found | Description | Severity              | Ref. Section/File | Root Cause | Resolution | Status                           | Closed Date |
| ------- | ---------- | ----------- | --------------------- | ----------------- | ---------- | ---------- | -------------------------------- | ----------- |
|         |            |             | ☐ High ☐ Med ☐ Low |                   |            |            | ☐ Open ☐ In Progress ☐ Closed |             |
|         |            |             | ☐ High ☐ Med ☐ Low |                   |            |            | ☐ Open ☐ In Progress ☐ Closed |             |
|         |            |             | ☐ High ☐ Med ☐ Low |                   |            |            | ☐ Open ☐ In Progress ☐ Closed |             |
|         |            |             | ☐ High ☐ Med ☐ Low |                   |            |            | ☐ Open ☐ In Progress ☐ Closed |             |
|         |            |             | ☐ High ☐ Med ☐ Low |                   |            |            | ☐ Open ☐ In Progress ☐ Closed |             |

**Severity Definitions:**

- **High:** Prevents system operation or violates safety requirements
- **Medium:** Impacts usability or performance but workarounds exist
- **Low:** Cosmetic or minor deviation from standards

---

<div style="page-break-before: always;"></div>

## 7. Formal Acceptance & Signatures

By signing below, all parties acknowledge that the Factory Acceptance Test has been conducted according to the procedures outlined in this document.

| Role                             | Name | Signature | Date |
| -------------------------------- | ---- | --------- | ---- |
| **Test Lead / Engineer**   |      |           |      |
| **Vendor Representative**  |      |           |      |
| **Marathon Petroleum PCE** |      |           |      |
| **Project Manager**        |      |           |      |
| **End User / Client**      |      |           |      |

### Acceptance Status

☐ **PASS** - All acceptance criteria met; graphics approved for deployment
☐ **CONDITIONAL PASS** - Minor items remain; see Issue Log for details
☐ **FAIL** - Significant issues require resolution and re-test

**Comments:**

```
___________________________________________________________________________
___________________________________________________________________________
___________________________________________________________________________
```

---

<div style="page-break-before: always;"></div>


## 8. References

| Document                             | Revision         | Purpose/Link               |
| ------------------------------------ | ---------------- | -------------------------- |
| AMP-LAR-AUT-SPC-0050                 | Rev 1            | Honeywell HMI Style Guide  |
| Experion PKS R520                    | Latest           | Experion HMI Specification |
| Display Builder Assistant User Guide | Latest           | Performance Analysis Tool  |
| Experion Alarm Philosophy            | Project-Specific | Alarm Priority & Response  |
| Control Builder Documentation        | Latest           | Controller Configuration   |

---

<div style="page-break-before: always;"></div>


## Appendix A: Glossary

| Term                | Definition                                                      |
| ------------------- | --------------------------------------------------------------- |
| **DOM**             | Document Object Model - structure of HTML elements in a graphic |
| **ENG Scale**       | Engineering scale - real-world units (PSI, °F, GPM, etc.)      |
| **FAT**             | Factory Acceptance Test                                         |
| **HMIWeb**          | Honeywell's web-based HMI technology for Experion               |
| **PKS**             | Process Knowledge System - Honeywell's Experion platform        |
| **PLC**             | Programmable Logic Controller                                   |
| **R520**            | Experion release/specification version                          |
| **VBScript**        | Visual Basic Scripting - legacy scripting in HMIWeb             |

---

## Document Revision History

| Version | Date       | Author | Changes         |
| ------- | ---------- | ------ | --------------- |
| 1.0     | YYYY-MM-DD |        | Initial release |
|         |            |        |                 |
|         |            |        |                 |

---

**END OF DOCUMENT**

