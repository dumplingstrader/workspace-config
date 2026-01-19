# **Process Controls Skill Matrix – Handoff Summary**

## 1. **Project Purpose**

This project builds a **complete, role‑based Process Controls Skill Matrix** for a refinery/operations environment, integrating:

* **MPC Career Guide** role expectations and competencies
* **Historical RACI** ownership patterns from controls/PLC/SIS duties
* A **modern taxonomy** of Control Systems, Technologies, Complex Control, Applications, Development, Tools, Business, and Soft Skills
* A unified **0–4 proficiency scale**
* A structured Excel workbook for assessments, training, gap analysis, and succession planning

The goal is a **single system of record** defining skills, targets, training needs, and responsibility alignment for all Process Controls, APC, and Technologist roles.

---

## 2. **Source Documents Used**

These files were loaded and used to generate the skill matrix:

* **Training_Attendance_Tracker.xlsx**

  *Source: User workspace; 40 employees tracked across 11 training courses*
  
  Used to populate Individual_Assessments with baseline proficiency levels from formal training completions

* **Refining_IC_Career Guide_Final (1).pdf**

  *Source: Marathon Petroleum; MPC career framework and proficiency definitions*
  
  Used as reference for role-based proficiency targets and career progression patterns

* **RACI Chart – Process Control Duties (PLC/SIS)**

  *Source: Historic RACI duties from Process Controls group*

  Available for future integration of task-based skill mappings

* **Process Controls Engineer Skill Matrix (sample)**

  *Source: Original template; initial skill categories*

* **Generated Files:**
  - **Process_Controls_Skill_Matrix_Enhanced.xlsx** – Main output workbook
  - **enhance_skill_matrix.py** – Workbook generator script
  - **populate_role_requirements.py** – Role requirements population script
  - **import_training_to_assessments.py** – Training data import automation

---

## 3. **Finalized Category Taxonomy (Top-Level)**

*(Updated: Reorganized for clarity and logical workflow — January 2026)*

1. **Control Platforms**
2. **Process Knowledge**
3. **Programming & Control Logic**
4. **Advanced Process Control**
5. **Enterprise Systems**
6. **Infrastructure & Networking**
7. **Implementation & Commissioning**
8. **Engineering Tools & Methods**
9. **Professional Development**
10. **Business & Leadership**

This taxonomy organizes skills from technical platforms through process knowledge, programming, optimization, supporting systems, execution, tools, knowledge sharing, and leadership.

---

## 4. **Sub‑Skills Under Each Category**

*(Updated: Reorganized and refined — January 2026)*

### **Control Platforms**

* Honeywell Experion
* Honeywell TDC 3000
* Triconex SIS
* Allen‑Bradley ControlLogix
* Allen‑Bradley Legacy PLC (PLC‑5, SLC500, MicroLogix)
* GE Mark VIe
* BN3500
* DCS HMI (Honeywell)
* AB HMI (PanelView/FTView)

### **Process Knowledge**

* Fired heaters
* Compressors
* Rotating equipment fundamentals
* Instrumentation fundamentals
* Electrical fundamentals
* Advanced regulatory control

### **Programming & Control Logic**

* TDC Control Language (CL)
* Experion SCM
* Interlocks & permissives
* Startup/shutdown sequences
* Cause‑and‑effect logic

### **Advanced Process Control**

* Aspen APC
* Imubit APC

### **Enterprise Systems**

* SAP
* Dynamo M&R
* ACM (Alarm Management)
* Integrity (SIS/LOPA)
* PI System
* OPC/PCDI/OPCI

### **Infrastructure & Networking**

* Historian connections
* SCADA/network routing
* Controller redundancy & health
* Network diagnostics
* Virtual machines

### **Implementation & Commissioning**

* Commissioning & loop checks
* Logic migration & upgrades
* Patching & updates
* Troubleshooting guides
* Peer reviews

### **Engineering Tools & Methods**

* Python scripting
* App development
* Data analytics (Excel, Power BI)
* Version control

### **Professional Development**

* Create training content
* Deliver training/workshops
* Mentoring
* Write procedures/standards
* Knowledge management

### **Business & Leadership**

* Leadership
* Project management
* Coordination
* Budget planning
* Cost estimation
* Vendor evaluation
* Lifecycle cost analysis
* Industry presentation
* Documentation quality
* Communication
* Stakeholder management
* Time management
* Safety/MOC proficiency

---

## 5. **Proficiency Scale (Finalized)**

*(Using MPC 1–5 scale directly)*

| MPC Level | Meaning    | Description                                                                 |
| --------- | ---------- | --------------------------------------------------------------------------- |
| 1         | Forming    | Awareness level, basic understanding                                        |
| 2         | Developing | Can perform with guidance, developing proficiency                          |
| 3         | Applying   | Independent practitioner, consistent quality                               |
| 4         | Leading    | Expert, can guide others, drives improvements                              |
| 5         | Shaping    | Subject matter expert, strategic influence, sets standards                 |

---

## 6. **Role List Included in the System**

### **Process Controls Engineers**

* Process Controls Engineer I
* Process Controls Engineer II
* Process Controls Engineer III / Senior
* Lead Process Controls Engineer

### **Advanced Process Controls Engineers**

* APC Engineer II
* APC Engineer III / Senior
* Lead APC Engineer

### **Process Controls & APC Technologists**

* Senior Technologist (P3)
* Lead Technologist (P4)
* Principal Technologist (P5)

These role names must be preserved to match MPC alignment.

---

## 7. **RACI → Skill Mapping Decisions**

### **How RACI letters convert to target levels:**

| RACI        | Meaning     | Target Level Impact     |
| ----------- | ----------- | ----------------------- |
| **A** | Accountable | 3–4 (Lead biased to 4) |
| **R** | Responsible | 2–3                    |
| **C** | Consulted   | 1–2                    |
| **I** | Informed    | 0–1                    |

### **How Tasks Map to Sub‑Skills**

A keyword mapping system was used. Examples:

* MOC → **Skills ▸ Safety/MOC proficiency**
* Program Storage / Repository / Version → **Control Systems ▸ Version control**
* Patching → **Control Systems ▸ Patching & updates**
* Alarms / HMI → **Control Systems ▸ Alarm configuration**
* SAP → **Critical Applications ▸ SAP PM**
* PI → **Critical Applications ▸ PI System**
* Fiber / Ports / BootP → **Critical Applications ▸ OPC/PCDI/OPCI**
* Laptop / VM / Passwords → **Tools ▸ Virtual machines**

This mapping is traceable in the **RACI_Crosswalk** sheet.

---

## 8. **Workbook Contents (Generated Output)**

Found in **Process_Controls_Skill_Matrix_Enhanced.xlsx**

### **Sheets:**

1. **Summary** – Dashboard with overview, statistics, and usage instructions
2. **Individual_Assessments** – Main data entry table with **40 employees populated** from training data
3. **Role_Requirements** – Target proficiency levels (1-5) populated for all 10 roles across 60 skills
4. **Proficiency_Scale** – MPC 1-5 scale reference with detailed descriptions
5. **Skill_Dictionary** – All 60 skills with category and definition

### **Key Features:**

* **60 total skills** organized across 10 categories
* **40 employees imported** from Training_Attendance_Tracker.xlsx with training-based proficiency levels
* **Role requirements populated** based on career progression framework (Engineer I → Lead → Technologist)
* **Training-to-skill mapping** applied (formal training = proficiency 2-3 baseline)
* **People as rows** layout for easy individual assessment entry
* **Category headers** merged above skill columns for visual grouping
* **Frozen panes** for easy navigation during data entry
* **Professional formatting** with color-coded headers and borders

### **Data Sources Integrated:**

1. **Training_Attendance_Tracker.xlsx** – 11 courses mapped to relevant skills
   - Triconex/SIS training: 36 total completions
   - ControlLogix training: 14 completions
   - Mark VIe training: 11 completions
   - DCS training: 9 completions
   - Python training: 4 completions
   
2. **Career progression framework** – Role-based proficiency targets aligned with MPC career levels

---

## 9. **Key Decisions to Preserve**

Another agent must adhere to the following:

* **Category names organized for logical workflow** (platforms → knowledge → programming → optimization → systems → infrastructure → implementation → tools → development → leadership)
* **Sub-skills are platform-specific and task-oriented**
* **Proficiency scale = MPC 1–5 (Forming, Developing, Applying, Leading, Shaping)**
* **60 skills total** across 10 categories
* **Individual assessments use people-as-rows layout** for efficient data entry
* **Training completion baseline = Level 2-3** (ready for manual adjustment)
* **Role proficiency targets follow career progression** (Engineer I=1-2, II=2-3, Senior=3-4, Lead=4-5)
* **MPC competencies must not be modified**
* **Skill Dictionary definitions are the canonical reference**
* **Excel workbook structure (sheet names and order) must remain stable**
* **Professional formatting preserved** (colors, borders, frozen panes)
* **Python scripts enable regeneration** with modifications when needed

---

## 10. **Remaining TODO Items (Optional Enhancements)**

Future agents may continue work by adding:

* ~~**Training data integration**~~ ✓ Complete – 40 employees imported
* ~~**Role requirements population**~~ ✓ Complete – All 10 roles populated
* **Manual refinement** – Adjust proficiency levels based on experience and manager input
* **Data validation** – Add Excel data validation to restrict assessment cells to 1-5
* **Gap analysis formulas** – Automated comparison of current vs target proficiency
* **Development plan generator** – Create personalized training paths from gaps
* **Visual dashboards** – Skills heat maps, coverage charts (Excel or Power BI)
* **Training curriculum links** – Add resources and course links per skill
* **Evidence requirements** – Define what demonstrates each proficiency level
* **Unit-specific sub-skills** – Add FCCU, HCU, SRU, etc. specializations
* **SME redundancy analysis** – Identify single points of failure
* **Competency-based interview questions** – Question bank per skill and level
* **Automated reporting** – Weekly/monthly skills progress tracking
* **Export capabilities** – PDF reports for individual development plans

---

## 11. **How to Continue the Project**

To continue seamlessly, the new agent/chat should be given:

1. **This Handoff Summary** (process_controls_skill_matrix_handoff_summary.md)
2. **The generated workbook** (Process_Controls_Skill_Matrix_Enhanced.xlsx)
3. **The Python generator scripts**:
   - `enhance_skill_matrix.py` – Main workbook generator
   - `populate_role_requirements.py` – Role requirements population logic
   - `import_training_to_assessments.py` – Training data import automation
4. **The source data files**:
   - Training_Attendance_Tracker.xlsx – Current employee training records
   - Refining_IC_Career Guide_Final (1).pdf – MPC career framework reference
   - RACI Chart_Process Control Duties_PLCSIS.xlsx (optional)

Then instruct:

> "Continue development of the Process Controls Skill Matrix using the attached context."

The new agent will have 100% of the necessary context.

---

## 12. **Summary Statistics**

* **Total Skills:** 60
* **Categories:** 10 (Control Platforms → Process Knowledge → Programming → APC → Enterprise Systems → Infrastructure → Implementation → Engineering Tools → Professional Development → Business & Leadership)
* **Roles:** 10 (Process Controls Engineers I-Lead, APC Engineers II-Lead, Technologists P3-P5)
* **Employees Tracked:** 40 (imported from training tracker)
* **Proficiency Scale:** MPC 1-5 (Forming, Developing, Applying, Leading, Shaping)
* **Layout:** People as rows, skills as columns
* **Training Courses Mapped:** 11 courses → 16 skill mappings
* **Data Status:**
  - Role Requirements: ✓ Populated (all 10 roles × 60 skills)
  - Individual Assessments: ✓ Baseline from training (ready for manual refinement)
  - Skill Dictionary: ✓ Complete
* **Generated:** January 2026
* **Status:** Ready for manual refinement and gap analysis
