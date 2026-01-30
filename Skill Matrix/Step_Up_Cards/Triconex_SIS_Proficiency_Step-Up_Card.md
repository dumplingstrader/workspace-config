# Triconex SIS - Proficiency Step-Up Card

**Skill Category:** Safety Systems - Safety Instrumented Systems
**Assessment Tool:** Process Controls Skill Matrix
**Last Updated:** January 19, 2026

---

## Proficiency Scale Overview

| Level | Label | Description |
|-------|-------|-------------|
| **1** | Forming | Awareness - Basic understanding, requires constant supervision |
| **2** | Developing | Guided practice - Can perform with supervision and guidance |
| **3** | Applying | Independent work - Performs tasks independently with occasional consultation |
| **4** | Leading | Expert - Mentors others, handles complex scenarios, troubleshoots system issues |
| **5** | Shaping | Subject Matter Expert - Defines standards, strategic planning, enterprise-wide expertise |

---

## Level 1: Forming (Awareness)

### Knowledge Requirements
- Basic understanding of safety instrumented systems (SIS) concepts
- Awareness of SIL ratings (SIL 1, 2, 3) and their significance
- Basic understanding of Triple Modular Redundancy (TMR) architecture
- Familiarity with safety lifecycle concepts (IEC 61511)
- Knowledge of the difference between BPCS and SIS
- Awareness of proof testing requirements
- Basic understanding of fail-safe principles
- Recognition of Triconex hardware components (chassis, MPs, I/O modules)

### Task Performance
- **Viewing logic** - Can open and navigate TriStation with supervision
- **Reading programs** - Can follow simple safety logic with explanation
- **Monitoring I/O** - Can view I/O status and alarm summaries with guidance
- **Documentation review** - Can review Cause & Effect diagrams and understand basic safety functions
- **Safety awareness** - Understands importance of change control in safety systems
- **Observation** - Observes experienced engineers during maintenance or modifications

### Limitations
- Cannot modify safety logic independently
- Does not troubleshoot SIS issues
- No authority to download programs to controllers
- Requires supervision for any hands-on tasks
- Cannot perform proof testing
- Does not interpret safety requirements specifications (SRS)

### Time in Role
Typically: 0-6 months in SIS environment

---

## Level 2: Developing (Guided Practice)

### Knowledge Requirements
- Understanding of Triconex system architecture (MPs, Communication Modules, I/O)
- Familiar with TriStation 1131 programming environment
- Basic knowledge of function block programming and ladder logic in TriStation
- Understanding of safety function types (ESD, F&G, BMS, HIPPS)
- Knowledge of voting architectures (2oo3, 1oo2, 2oo2D)
- Familiarity with I/O module types (digital, analog, pulse, HART)
- Basic understanding of TRICON, Tricon CX, and Trident controller families
- Awareness of common failure modes and diagnostic capabilities
- Understanding of bypass philosophy and procedures

### Task Performance
- **Program navigation** - Navigates safety programs independently, locates specific functions
- **Simple modifications** - Makes minor logic changes following approved MOC procedures (with supervision)
- **I/O monitoring** - Monitors I/O health, identifies module faults with guidance
- **Documentation** - Updates Cause & Effect diagrams after changes
- **Proof test support** - Assists with proof testing activities following procedures
- **Alarm analysis** - Reviews diagnostic alarms and categorizes by severity
- **Backup/restore** - Performs system backups following procedures
- **Status monitoring** - Uses TriStation to monitor system health and redundancy status

### Capabilities (With Supervision)
- Modifies simple interlocks or permissives
- Adds or modifies timer functions
- Forces I/O for testing purposes (following bypass procedures)
- Downloads programs after review and approval
- Generates system reports (I/O status, diagnostics, SOE)
- Performs online/offline comparisons
- Configures communication settings for HMI integration
- Participates in proof testing activities

### Limitations
- Cannot design safety functions independently
- Requires guidance for complex troubleshooting
- Does not perform SIL verification calculations
- No authority for major program restructuring
- Does not lead Management of Change (MOC) processes
- Limited understanding of functional safety standards

### Time in Role
Typically: 6-18 months in SIS role with consistent practice

---

## Level 3: Applying (Independent Work)

### Knowledge Requirements
- Proficient in TriStation 1131 programming (FBD, LD, ST)
- Comprehensive understanding of TMR architecture and voting mechanisms
- Knowledge of IEC 61511 safety lifecycle requirements
- Understanding of SIL verification methodologies (PFDavg calculations)
- Familiar with safety integrity requirements and hardware fault tolerance
- Knowledge of proof test procedures and intervals
- Understanding of common cause failures and systematic failures
- Familiar with Triconex communication protocols (TriStation, Modbus, OPC)
- Knowledge of FMEDA (Failure Modes, Effects, and Diagnostic Analysis)
- Understanding of safe state determination for all I/O types

### Task Performance
- **Independent programming** - Creates complete safety functions without supervision
- **Troubleshooting** - Diagnoses and resolves routine SIS logic and I/O issues
- **I/O configuration** - Configures I/O modules and communication settings independently
- **Proof testing** - Leads proof test execution for safety instrumented functions
- **MOC execution** - Executes approved Management of Change procedures independently
- **Documentation** - Creates comprehensive Cause & Effect diagrams and logic narratives
- **Commissioning** - Leads commissioning activities for SIS modifications
- **Integration** - Coordinates SIS integration with BPCS and F&G systems

### Capabilities (Independent)
- Designs and implements safety functions per SRS requirements
- Troubleshoots TMR voting discrepancies
- Performs online program uploads and compares with master copies
- Configures TriStation peer-to-peer communication
- Implements SOE (Sequence of Events) capture and reporting
- Performs partial stroke testing logic for valves
- Configures diagnostic alarm thresholds and responses
- Creates custom function blocks for reusable logic
- Trains Level 1-2 personnel on Triconex fundamentals
- Coordinates proof test schedules and documentation

### Decision Authority
- Makes routine programming changes following MOC procedures
- Determines when to escalate complex issues
- Approves minor I/O configuration changes
- Selects appropriate voting configurations for new functions
- Determines proof test intervals (within approved procedures)

### Limitations
- Does not design complete SIS architectures independently
- Major safety function design requires Level 4 review
- SIL verification calculations require Level 4 oversight
- Does not establish site-wide SIS standards
- Functional safety assessments require Level 4+ involvement
- Does not lead HAZOP or LOPA studies independently

### Time in Role
Typically: 2-4 years with consistent SIS experience

---

## Level 4: Leading (Expert)

### Knowledge Requirements
- Expert-level understanding of Triconex product line (TRICON, CX, Trident)
- Advanced knowledge of IEC 61511 and ISA-84 safety lifecycle
- Expert in SIL verification (PFDavg, PFH, SFF calculations)
- In-depth knowledge of functional safety standards (IEC 61508, ISO 13849)
- Proficient in HAZOP and LOPA methodologies
- Expert in safety requirements specification (SRS) development
- Understanding of risk assessment techniques (frequency, consequence, risk matrices)
- Knowledge of proof test optimization and RCM principles
- Familiar with cybersecurity for safety systems (IEC 62443)
- Expert in TMR diagnostics and fault tolerance analysis
- Understanding of safety validation and verification methods
- Knowledge of Safety Lifecycle Management software tools

### Task Performance
- **SIS architecture design** - Designs complete SIS including redundancy and communication
- **SIL verification** - Performs comprehensive SIL calculations and validation
- **LOPA facilitation** - Leads or participates in LOPA studies
- **SRS development** - Authors Safety Requirements Specifications
- **Advanced troubleshooting** - Resolves complex TMR, communication, and voting issues
- **Performance optimization** - Analyzes scan times, optimizes safety function execution
- **Integration leadership** - Leads integration with F&G, BPCS, ESD systems
- **Project management** - Manages SIS upgrade or expansion projects
- **Functional safety assessment** - Conducts FSA per IEC 61511 requirements

### Capabilities (Expert Authority)
- Designs SIS architectures for new facilities or major expansions
- Creates site SIS programming standards and style guides
- Performs PFDavg calculations for SIL verification
- Develops proof test procedures and intervals based on reliability data
- Troubleshoots complex MP synchronization and voting issues
- Implements remote I/O configurations over Tricon networks
- Designs and validates partial stroke testing strategies
- Evaluates spurious trip rates and implements reduction strategies
- Mentors Level 1-3 personnel; provides formal training
- Conducts root cause analysis for SIS-related incidents
- Performs pre-startup safety reviews (PSSR)
- Leads Management of Change reviews for SIS modifications
- Authors functional safety documentation (FSA, SIL verification reports)

### Decision Authority
- Approves all major SIS designs and modifications
- Defines hardware selection criteria and approved I/O lists
- Establishes SIS programming standards and documentation requirements
- Authorizes bypass procedures and limits
- Determines proof test strategies and frequencies
- Approves SIL verification methodologies

### Strategic Contributions
- Participates in long-term safety system planning
- Identifies opportunities for SIS modernization
- Develops training programs for operations and engineering
- Establishes KPIs for SIS performance (spurious trip rates, proof test results)
- Represents site in corporate functional safety strategy
- Leads incident investigations involving SIS

### Limitations
- Enterprise-wide safety standards require Level 5 involvement
- Major capital project safety strategies require Level 5 input
- Corporate functional safety policy typically involves Level 5

### Time in Role
Typically: 5-10+ years with diverse SIS project experience

---

## Level 5: Shaping (Subject Matter Expert)

### Knowledge Requirements
- Recognized industry expert in Triconex and functional safety
- Deep understanding of entire SIS vendor landscape (Triconex, SIS-TECH, HIMA, others)
- Expert in IEC 61511, IEC 61508, and emerging safety standards
- Strategic understanding of safety lifecycle management across asset lifecycle
- Expert in functional safety management systems (FSM)
- Thought leader in SIS cybersecurity and risk assessment
- Advanced knowledge of safety performance indicators and benchmarking
- Expert in regulatory compliance (API, OSHA PSM, EPA RMP)
- Understanding of safety culture and human factors in safety systems
- Knowledge of AI/ML applications in predictive safety (emerging)

### Task Performance
- **Enterprise strategy** - Defines corporate standards for SIS implementations
- **Safety architecture** - Designs enterprise-wide safety system architectures
- **Technology roadmap** - Develops 5-10 year safety technology roadmaps
- **Complex problem solving** - Resolves enterprise-impacting or unprecedented safety issues
- **Innovation leadership** - Pilots emerging safety technologies and methodologies
- **Vendor management** - Engages directly with Schneider Electric (Triconex) executives
- **Risk governance** - Evaluates safety risks across enterprise, defines risk tolerance
- **Standards authorship** - Authors corporate functional safety management system (FSMS)
- **Regulatory interface** - Primary interface with regulatory bodies on safety compliance

### Capabilities (SME Authority)
- Establishes corporate SIS design standards and engineering practices
- Approves all major safety system projects enterprise-wide
- Defines functional safety competency requirements and certification programs
- Develops corporate SIL verification and validation procedures
- Represents company in industry safety forums (CCPS, ISA)
- Authors technical papers on functional safety best practices
- Evaluates strategic vendor partnerships and system integrators
- Leads due diligence for M&A involving safety systems
- Defines migration strategies for legacy safety systems
- Establishes corporate SIS cybersecurity policies
- Develops enterprise proof test management strategies
- Creates corporate incident investigation protocols for safety systems
- Defines safety performance metrics and benchmarking programs

### Decision Authority
- Final authority on safety system platform selection
- Approves capital budgets for safety infrastructure
- Determines corporate functional safety policies
- Authorizes exceptions to safety standards (with risk assessment)
- Defines organization structure and staffing for functional safety
- Approves SIL targets for corporate risk tolerance

### Strategic Leadership
- Provides vision for functional safety program maturity
- Builds relationships with vendor executives and regulatory bodies
- Identifies opportunities for risk reduction through technology
- Develops succession planning for functional safety expertise
- Mentors senior engineers and builds organizational capability
- Influences industry standards and regulatory frameworks
- Champions safety culture and continuous improvement
- Integrates safety systems strategy with digital transformation

### External Recognition
- Invited speaker at safety conferences (Mary Kay O'Connor, CCPS, Automation Fair)
- Published author in safety journals (Journal of Loss Prevention, Process Safety Progress)
- Recognized by ISA/IEC as functional safety expert or standards contributor
- Consulted by other companies and government agencies
- Serves on industry committees (ISA84, IEC TC65, API committees)
- Active in professional societies (AIChE CCPS, ISA, IEC)
- Certified Functional Safety Expert (TÜV, Exida, other certification bodies)

### Time in Role
Typically: 15+ years with extensive multi-industry functional safety experience

---

## Assessment Guidelines

### How to Use This Step-Up Card

1. **Review all competencies** at each level with the employee
2. **Identify demonstrated capabilities** based on actual work performance
3. **Consider time in role** but prioritize demonstrated competency
4. **Look for consistent performance** across multiple task categories
5. **Assign the highest level** where employee meets 80%+ of criteria
6. **Document gaps** for development planning
7. **Verify safety training** - Functional safety work requires formal training/certification

### Assessment Tips

- **Safety credentials matter** - Formal training (TÜV FS Engineer, Exida CFSE) supports rating
- **Don't over-rate based on BPCS experience** - SIS programming requires different mindset
- **Require evidence** - Use specific examples of safety functions designed or troubleshooting
- **Consider risk awareness** - Does employee understand consequences of errors in safety systems?
- **Differentiate "has done" from "can do consistently"** - Safety work requires reproducible quality
- **Factor in documentation quality** - SIS work demands rigorous documentation per IEC 61511
- **Evaluate adherence to procedures** - Bypassing MOC or test procedures is disqualifying

### Red Flags for Over-Rating

- Employee cannot explain SIL concepts or safety integrity requirements
- Weak understanding of TMR voting and fault tolerance
- Casual approach to bypasses or proof test procedures
- Frequent shortcuts in documentation or change management
- Heavy reliance on vendor support for routine troubleshooting
- Avoids SIL verification calculations or functional safety assessments
- Limited understanding of IEC 61511 requirements
- Treats SIS like BPCS (lacks safety mindset)

### Development Path Indicators

**From 1 to 2:** Formal Triconex training, supervised programming tasks, study IEC 61511 basics  
**From 2 to 3:** Reduce supervision, lead proof tests, complete SIL verification training  
**From 3 to 4:** Lead projects, SRS development, LOPA facilitation, formal CFSE or FS Engineer certification  
**From 4 to 5:** Multi-site FSA leadership, standards development, external engagement, strategic safety roles

---

## Typical Role Alignment

| Level | Typical Job Titles |
|-------|-------------------|
| **1** | Entry-level Controls Engineer, Safety Systems Intern, Co-op (safety exposure) |
| **2** | SIS Technician, Junior Safety Engineer, Instrumentation Tech (SIS focus) |
| **3** | Safety Systems Engineer II, SIS Specialist, Functional Safety Engineer |
| **4** | Senior Safety Systems Engineer, SIS Lead, Functional Safety Specialist |
| **5** | Principal Safety Engineer, Corporate Functional Safety Manager, Safety SME |

---

## Example Scenarios for Assessment

### Scenario 1: Spurious Trip Investigation
- **Level 1:** Reports that emergency shutdown occurred, reviews alarm sequence
- **Level 2:** Pulls SOE report, identifies sensor signal that triggered trip, documents event
- **Level 3:** Analyzes complete trip sequence, identifies intermittent sensor failure, coordinates sensor replacement, validates no other contributing factors
- **Level 4:** Performs root cause analysis, identifies common cause failures across multiple sensors, implements sensor redundancy upgrade, updates proof test procedures
- **Level 5:** Evaluates spurious trip rate enterprise-wide, identifies systemic issues, implements predictive diagnostics program across all sites

### Scenario 2: New Safety Function Implementation
- **Level 1:** Reviews Cause & Effect diagram to understand new safety function
- **Level 2:** Configures I/O modules per specification, tests under supervision
- **Level 3:** Implements complete safety function per SRS, performs FAT/SAT testing, documents commissioning
- **Level 4:** Develops SRS from LOPA requirements, designs safety function with appropriate voting, performs SIL verification, leads commissioning and validation, authors FSA
- **Level 5:** Defines corporate standards for safety function design, reviews all SRS documents for compliance with corporate risk tolerance, approves SIL verification methodologies

### Scenario 3: TMR Voting Mismatch Alarm
- **Level 1:** Reports voting mismatch alarm to supervisor
- **Level 2:** Uses TriStation to identify which MP shows discrepancy, follows troubleshooting guide
- **Level 3:** Analyzes voting pattern, determines sensor drift as root cause, coordinates calibration, validates TMR synchronization restored
- **Level 4:** Identifies systematic voting discrepancies across multiple functions, analyzes common mode failures, implements improved diagnostic alarming, updates maintenance procedures
- **Level 5:** Establishes enterprise-wide TMR health monitoring program, defines acceptable voting mismatch rates, implements predictive analytics for voting issues

---

## Related Skills

The following skills often correlate with Triconex SIS proficiency:

**Category: Safety Systems**
- Fire & Gas Systems (Det-Tronics, MSA, others)
- Emergency Shutdown (ESD) Systems
- High-Integrity Pressure Protection Systems (HIPPS)
- Burner Management Systems (BMS)

**Category: Functional Safety & Risk Assessment**
- HAZOP Facilitation
- LOPA (Layer of Protection Analysis)
- SIL Verification & Validation
- Process Safety Management (PSM)

**Category: Instrumentation**
- Field Instrumentation (Pressure, Temperature, Flow, Level)
- Smart Instrumentation (HART, FOUNDATION Fieldbus)
- Safety Valve Sizing and Partial Stroke Testing

**Category: Process Control**
- BPCS/DCS Systems (Experion, DeltaV)
- Control System Integration
- Industrial Networking

**Category: Compliance & Standards**
- IEC 61511 / ISA-84 (SIS Lifecycle)
- IEC 61508 (Functional Safety)
- API RP 554 / API RP 556 (Fire & Gas, Instrumented Systems)
- OSHA PSM / EPA RMP Compliance

---

## Development Resources

### Recommended Training Path by Level

**Level 1 → 2:**
- Triconex System Overview (Vendor or SI training)
- Introduction to Safety Instrumented Systems
- IEC 61511 Fundamentals course
- Hands-on lab time with trainer system
- Shadow Level 3+ personnel during proof tests

**Level 2 → 3:**
- Triconex TriStation 1131 Programming (Advanced)
- SIL Verification and Calculation Methods
- Proof Testing Procedures and Management
- Management of Change for Safety Systems
- Independent project assignments with review

**Level 3 → 4:**
- Functional Safety Engineer certification (TÜV or equivalent)
- LOPA practitioner training
- SRS Development workshop
- Cybersecurity for Safety Systems (IEC 62443)
- Advanced SIL verification tools (exSILentia, RiskSpectrum)
- Mentorship program (mentor Level 1-2 staff)
- Lead role on SIS projects

**Level 4 → 5:**
- Certified Functional Safety Expert (CFSE) - Exida or TÜV
- HAZOP Leader certification
- Leadership and project management training
- External conferences (CCPS, Mary Kay O'Connor Symposium)
- Publishing/presenting opportunities
- Multi-site assignments
- Corporate functional safety management role

### Hands-On Development Opportunities
- **Plant turnarounds** - Proof testing and SIS maintenance activities
- **New unit startups** - Complete SIS design through commissioning
- **SIS modernization projects** - Legacy system replacements
- **Incident investigations** - Root cause analysis for safety system failures
- **HAZOP/LOPA participation** - Safety requirements development
- **Functional safety assessments** - IEC 61511 compliance reviews
- **Pre-startup safety reviews** - Commissioning and validation activities
- **Vendor training** - Schneider Electric factory training

### Self-Study Resources
- **Standards:**
  - IEC 61511 (Process Industry SIS Lifecycle)
  - IEC 61508 (Functional Safety of E/E/PE Systems)
  - ISA-TR84.00.02 (Simplified SIL Calculations)
  - API RP 554 (Process Instrumentation and Control)
- **Books:**
  - "Safety Instrumented Systems Handbook" by Guy Brassard
  - "Process Safety: Key Concepts and Practical Approaches" by CCPS
  - "Functional Safety for Machinery" by Paul Gruhn
  - "Guidelines for Safe Automation of Chemical Processes" by CCPS
- **Online communities:**
  - ISA LinkedIn groups
  - Eng-Tips Control Systems forum
  - CCPS online resources
- **Journals:**
  - Journal of Loss Prevention in the Process Industries
  - Process Safety Progress (AIChE)

---

## Triconex Product Family Knowledge

Understanding the Triconex product evolution helps assess breadth of experience:

### Legacy Systems (Historical Understanding - Level 2-3)
- **TRICON** - Original TMR architecture, still in widespread use
- **TRICON Version 9 and earlier** - Older hardware platforms

### Current Platforms (Level 2-4)
- **TRICON Version 10/11** - Most common deployed systems
- **Tricon CX** - Compact safety controller for smaller applications
- **Trident** - Latest generation, enhanced performance and cybersecurity

### Advanced Capabilities (Level 3-5)
- **TriStation 1131** - Programming environment (FBD, LD, ST)
- **Triconex Communication Modules (TCMs)** - Modbus, TSAA, OPC
- **External Termination Modules (EXTMs)** - Distributed I/O
- **TRICON Simulator** - Offline testing and validation
- **Safety Manager** - Safety lifecycle management software
- **Triconex-Ready Smart Instruments** - HART and FOUNDATION Fieldbus integration

---

## Functional Safety Competency Overlay

For employees working with any SIS, additional functional safety assessment criteria:

### Functional Safety Competency Levels
- **Basic (Level 1-2):** Understands SIL concepts, follows procedures, awareness of IEC 61511
- **Intermediate (Level 3):** Applies functional safety principles, executes safety lifecycle phases, understands SIL verification
- **Advanced (Level 4):** Designs safety systems per IEC 61511, performs SIL calculations, leads FSA activities, facilitates LOPA
- **Expert (Level 5):** Defines functional safety management systems, establishes corporate risk tolerance, influences industry standards

### Additional Functional Safety Knowledge
- **Safety lifecycle phases** (IEC 61511):
  - Analysis (HAZOP, LOPA, SIL determination)
  - Design and engineering (SRS, SIL verification)
  - Installation and commissioning (FAT, SAT, PSSR)
  - Operation and maintenance (proof testing, MOC)
  - Decommissioning
- **Risk assessment techniques:**
  - Risk matrices (frequency vs. consequence)
  - LOPA (Independent Protection Layers)
  - RRF (Risk Reduction Factor) calculations
  - ALARP principles (As Low As Reasonably Practicable)
- **SIL verification methods:**
  - PFDavg calculations (Probability of Failure on Demand)
  - Fault Tree Analysis (FTA)
  - Markov modeling for complex systems
  - Common cause failures (Beta factor)
- **Proof testing:**
  - Full proof test vs. partial proof test
  - Proof test coverage
  - Dangerous detected vs. undetected failures
  - Proof test interval optimization

---

## Safety Documentation Standards

Understanding what documentation is required at each level:

### Level 2 Documentation
- Equipment status reports
- Proof test result forms
- Change log entries
- Incident reports

### Level 3 Documentation
- Cause & Effect diagrams
- SIF (Safety Instrumented Function) test procedures
- Logic narratives
- Commissioning reports
- MOC documentation

### Level 4 Documentation
- Safety Requirements Specification (SRS)
- SIL verification reports
- Functional Safety Assessment (FSA)
- PSSR (Pre-Startup Safety Review) signoffs
- Safety validation reports
- Proof test optimization studies

### Level 5 Documentation
- Functional Safety Management System (FSMS)
- Corporate SIS design standards
- Safety performance metrics and benchmarking
- Functional safety competency framework
- Corporate risk tolerance criteria
- Safety lifecycle procedures

---

## Common SIS Design Patterns to Learn

### Voting Architectures (Level 2-3)
- **1oo1** - Single sensor, no redundancy (non-SIL or SIL1)
- **1oo2** - Two sensors, one must trip (low spurious trips)
- **2oo2** - Two sensors, both must trip (higher reliability)
- **2oo3** - Three sensors, two must agree (most common for critical SIFs)
- **2oo2D** - Two sensors, diagnostic detection of failures

### Safety Function Types (Level 3-4)
- **ESD (Emergency Shutdown)** - Process shutdown on demand
- **Partial Stroke Testing** - Automated valve testing without process shutdown
- **HIPPS** - High-Integrity Pressure Protection
- **BMS** - Burner Management (flame monitoring, purge sequences)
- **F&G Integration** - Fire and gas detection interface

### Bypass Strategies (Level 3-4)
- **Maintenance bypass** - Temporary sensor/final element bypass for maintenance
- **Forced values** - Override of sensor inputs (highly controlled)
- **Bypass timers** - Automatic timeout on bypasses
- **Bypass alarming** - Notification of active bypasses

---

## Industry Application Focus

Triconex SIS is commonly used in these industries (breadth indicates Level 4-5):

### Oil & Gas
- Offshore platforms (topsides, FPSO)
- Refineries and petrochemical
- Pipeline and midstream facilities
- LNG liquefaction and regasification

### Chemical
- Chemical manufacturing
- Specialty chemicals
- Pharmaceutical manufacturing (batch control integration)

### Power Generation
- Gas turbine protection
- Boiler control and safety
- Combined cycle power plants

### Other Process Industries
- Pulp and paper
- Food and beverage (when safety-rated control required)
- Mining and metals

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-01-19 | Initial Triconex SIS step-up card created | Process Controls Team |

---

**Questions or feedback on this step-up card?**  
Contact: Functional Safety Engineering Leadership

**Important Note:** Safety Instrumented Systems work requires specialized training and formal competency assessment. Always verify that personnel have appropriate functional safety training before assigning SIS responsibilities. Errors in safety systems can result in catastrophic incidents.
