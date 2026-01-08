# Control Systems Functional Location Structure
## SAP Equipment Master Data Organization

---

## Overview
This document defines the functional location hierarchy and equipment categories for Control Systems across all Marathon Petroleum sites. This structure enables logical grouping by system type rather than physical location, supporting distributed control systems that span multiple process areas.

---

## Functional Location Hierarchy

### Site Codes
- **LA-C** - Los Angeles Carson
- **LA-L** - Los Angeles Logistics
- **LA-W** - Los Angeles Wilmington
- **WC** - Watson Cogen

### Top-Level Functional Locations (All Sites)

```
Functional Location        Description
-------------------        -----------
LA-C-16                    A16 Control Systems
LA-L-16                    A16 Control Systems
LA-W-16                    A16 Control Systems
WC-16                      A16 Control Systems
```

### Second-Level Functional Locations (Under Each Site)

```
Parent: LA-C-16 (example - applies to all sites)

Functional Location        Description
-------------------        -----------
LA-C-16-DCS                DCS Distributed Control System
LA-C-16-PLC                PLC Programmable Logic Controllers
LA-C-16-SIS                SIS Safety Instrumented Systems
LA-C-16-VMS                VMS Vibration Monitoring Systems
LA-C-16-TCS                TCS Turbomachinery Control Systems
LA-C-16-NET                NET Network Infrastructure
LA-C-16-AUX                AUX Auxiliary Systems
```

<div style="page-break-after: always;"></div>

---

## Equipment Categories by Functional Location

### LA-C-16-DCS - Distributed Control System

| Equipment Category | Description |
|-------------------|-------------|
| CTRL-DCS-CTL | DCS Controllers (C200, C300, ACE controllers) |
| CTRL-DCS-IOM | I/O Modules (Analog Input/Output, Digital Input/Output) |
| CTRL-DCS-PWR | Power Supplies & Power Distribution |
| CTRL-DCS-COM | Communication Modules (HDAI, FTA, Ethernet) |
| CTRL-DCS-RAK | Racks & Chassis |
| CTRL-DCS-OWS | Operator Workstations |
| CTRL-DCS-SRV | Servers (Application Server, Historian, Domain Controller, etc.) |

**Example Equipment:**
- Honeywell C300 Controller
- Experion ACE Controller
- Analog Input IOTA modules
- FTE modules
- Universal Stations
- History Servers

<div style="page-break-after: always;"></div>

---

### LA-C-16-PLC - Programmable Logic Controllers

| Equipment Category | Description |
|-------------------|-------------|
| CTRL-PLC-CPU | PLC Processors/CPUs |
| CTRL-PLC-IOM | I/O Modules (Analog & Digital) |
| CTRL-PLC-PWR | Power Supplies |
| CTRL-PLC-COM | Communication Modules (Ethernet, serial, fieldbus) |
| CTRL-PLC-RAK | Racks & Chassis |
| CTRL-PLC-HMI | Local HMI Panels & Touch Screens |

**Example Equipment:**
- Allen-Bradley ControlLogix CPUs
- Siemens S7 CPUs
- Remote I/O racks
- Stratix switches (dedicated to PLC networks)
- PanelView displays

<div style="page-break-after: always;"></div>

---

### LA-C-16-SIS - Safety Instrumented Systems

| Equipment Category | Description |
|-------------------|-------------|
| CTRL-SIS-CTL | Safety Controllers (FSC, Tricon, etc.) |
| CTRL-SIS-IOM | Safety I/O Modules (SIL-rated) |
| CTRL-SIS-PWR | Safety-rated Power Supplies |
| CTRL-SIS-COM | Safety Communication Modules |
| CTRL-SIS-RAK | Safety Chassis/Racks |
| CTRL-SIS-OWS | Safety Engineering Workstations |

**Example Equipment:**
- Honeywell Safety Manager (FSC)
- Triconex Safety Controllers
- Safety I/O modules
- Safety Engineering Stations

**Note:** Multiple SIS systems may exist with similar hardware. Use equipment classification characteristics to differentiate:
- System ID (SIS-1, SIS-2, SIS-3)
- Process Unit Assignment
- SIL Level

<div style="page-break-after: always;"></div>

---

### LA-C-16-VMS - Vibration Monitoring Systems

| Equipment Category | Description |
|-------------------|-------------|
| CTRL-VMS-MON | Vibration Monitors & Controllers (Bently Nevada 3500, 1900/65A) |
| CTRL-VMS-SEN | Vibration Sensors & Proximity Probes |
| CTRL-VMS-PWR | Power Supplies for Monitoring Systems |
| CTRL-VMS-RAK | Monitor Racks & Chassis |
| CTRL-VMS-OWS | Vibration Monitoring Workstations |

**Example Equipment:**
- Bently Nevada 3500 rack monitors
- Proximity probes & accelerometers
- System 1 monitoring software stations
- Vibration monitor power supplies

<div style="page-break-after: always;"></div>

---

### LA-C-16-TCS - Turbomachinery Control Systems

| Equipment Category | Description |
|-------------------|-------------|
| CTRL-TCS-CTL | Turbine Controllers (GE Mark VIe, Woodward GAP, MicroNet) |
| CTRL-TCS-IOM | I/O Modules & Termination Panels |
| CTRL-TCS-PWR | Power Supplies |
| CTRL-TCS-COM | Communication Modules |
| CTRL-TCS-HMI | Turbine HMI Panels |
| CTRL-TCS-RAK | Control Racks & Cabinets |

**Example Equipment:**
- GE Mark VIe turbine controllers
- Woodward GAP governor controllers
- Turbine control I/O modules
- Turbomachinery HMI displays

<div style="page-break-after: always;"></div>

---

### LA-C-16-NET - Network Infrastructure

| Equipment Category | Description |
|-------------------|-------------|
| CTRL-NET-SWH | Network Switches (Managed & Unmanaged) |
| CTRL-NET-RTR | Routers |
| CTRL-NET-FWL | Firewalls & Security Appliances |
| CTRL-NET-MDM | Media Converters (Fiber/Copper) |
| CTRL-NET-WAP | Wireless Access Points |

**Example Equipment:**
- Cisco Industrial Ethernet switches
- Hirschmann switches
- Firewall appliances
- Fiber optic media converters

<div style="page-break-after: always;"></div>

---

### LA-C-16-AUX - Auxiliary/Support Systems

| Equipment Category | Description |
|-------------------|-------------|
| CTRL-AUX-UPS | Uninterruptible Power Supplies |
| CTRL-AUX-RAK | Equipment Racks & Cabinets (non-controller) |
| CTRL-AUX-CLM | Climate Control (HVAC, cooling fans, temperature monitors) |
| CTRL-AUX-PDU | Power Distribution Units |
| CTRL-AUX-KVM | KVM Switches |

**Example Equipment:**
- Rack-mounted UPS systems
- Server racks
- Cabinet cooling fans
- Rack PDUs

<div style="page-break-after: always;"></div>

---

## Equipment Master Record Fields

Each individual equipment record will contain:

### Standard SAP Fields
- **Equipment Number** - Auto-generated or manual entry
- **Equipment Description** - Clear identification
- **Functional Location** - Link to functional location hierarchy
- **Equipment Category** - From categories defined above
- **Technical ID Number** - Asset tag or internal ID
- **Manufacturer** - Vendor name
- **Model Number** - Manufacturer part/model number
- **Serial Number** - Unique serial number
- **Installation Date** - Commissioning date
- **Acquisition Value** - Purchase cost
- **ABC Indicator** - Criticality (A=Critical, B=Important, C=Standard)
- **Planning Plant** - Maintenance planning organization
- **Planner Group** - Responsible planner

### Classification Characteristics (Custom)
Additional fields for detailed specifications:
- **System Assignment** - Which specific system (e.g., DCS-1, SIS-A, PLC-Unit3)
- **Process Unit** - Process area served (U-1, U-2, Utilities, Plant-wide)
- **Cabinet/Rack Location** - Physical mounting location
- **IP Address** - For networked devices
- **Firmware Version** - Controller/device firmware
- **Configuration Version** - Software version
- **Redundancy Status** - Primary/Backup/Standalone
- **SIL Level** - For safety equipment
- **Network Zone** - Control network, Safety network, Business network
- **Spare Available** - Yes/No/Partial

<div style="page-break-after: always;"></div>

---

## Implementation Notes

### Benefits of This Structure
- **Logical Grouping** - By system function, not physical location
- **Clear Ownership** - Controls group manages LA-C-16 hierarchy
- **System Flexibility** - Supports cross-area control systems
- **Scalable** - Easy to add new equipment under existing categories
- **Part Number Management** - Multiple identical parts differentiated by characteristics

### Data Entry Strategy
1. Create functional location hierarchy (IL01 - Create Functional Location)
2. Define equipment categories (SPRO configuration)
3. Create classification characteristics (CT04)
4. Create equipment master records (IK01)
5. Assign classifications to equipment
6. Bulk upload using LSMW or batch input

### Maintenance Integration
- Work orders can be created against functional locations or individual equipment
- Preventive maintenance plans link to equipment categories
- Spare parts associate with equipment records via BOM
- Maintenance history tracked by equipment number

<div style="page-break-after: always;"></div>

---

## Complete Example - LA-C-16-DCS

```
Functional Location: LA-C-16-DCS
Description: DCS Distributed Control System

Equipment Records:
  Equipment #: 1000001234
  Description: C300 Controller - Crude Unit
  Category: CTRL-DCS-CTL
  Manufacturer: Honeywell
  Model: HC900-C30-1-1-1
  Serial #: C300-2024-12345
  System Assignment: DCS-PRIMARY
  Process Unit: U-1 Crude
  Cabinet: CR-1-R5-SLOT3
  
  Equipment #: 1000001235
  Description: AI IOTA Module - Tank Farm
  Category: CTRL-DCS-IOM
  Manufacturer: Honeywell
  Model: FTA-T-16
  Serial #: FTA-2023-67890
  System Assignment: DCS-PRIMARY
  Process Unit: Tank Farm
  Cabinet: CR-2-R3-SLOT8
```

---

## Next Steps

1. **Validate Structure** - Review with SAP admin and site stakeholders
2. **Create Functional Locations** - Use IL01 or mass upload
3. **Configure Equipment Categories** - SPRO IMG settings
4. **Build Classification** - Define characteristics in CT04
5. **Create Data Templates** - Excel templates for bulk upload
6. **Begin Equipment Entry** - Start with critical systems (DCS, SIS)
7. **Train Users** - Equipment creation, PM01 planning, work orders

---

**Document Version:** 1.0  
**Date:** January 8, 2026  
**Author:** Tony Chiu  
**Sites:** LA-C, LA-L, LA-W, WC
