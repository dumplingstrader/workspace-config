# V2.0 Folder Structure and V1 Archive Organization

## ✅ Completed Structure

```
Experion_License_Aggregator/
│
├── v2/                                    # NEW - V2.0 Complete Rewrite
│   ├── models/                           # Data models with validation
│   │   ├── __init__.py                   # (Agent: Task 1.1)
│   │   ├── license.py                    # LicenseData
│   │   ├── usage.py                      # UsageData
│   │   ├── enriched_license.py           # EnrichedLicense
│   │   ├── cost.py                       # CostCalculation
│   │   └── transfer.py                   # TransferCandidate
│   │
│   ├── pipeline/                         # Processing stages
│   │   ├── __init__.py
│   │   ├── extractors/                   # (Agent: Tasks 2.1-2.3)
│   │   │   ├── __init__.py
│   │   │   ├── base_extractor.py
│   │   │   ├── xml_extractor.py
│   │   │   ├── csv_extractor.py
│   │   │   └── config_loader.py
│   │   │
│   │   ├── validators/                   # (Agent: Tasks 3.1-3.3)
│   │   │   ├── __init__.py
│   │   │   ├── base_validator.py
│   │   │   ├── schema_validator.py
│   │   │   ├── business_validator.py
│   │   │   └── match_validator.py
│   │   │
│   │   ├── transformers/                 # (Agent: Tasks 4.1-4.5)
│   │   │   ├── __init__.py
│   │   │   ├── deduplicator.py
│   │   │   ├── field_mapper.py
│   │   │   ├── usage_matcher.py
│   │   │   ├── cost_calculator.py
│   │   │   └── transfer_detector.py
│   │   │
│   │   └── exporters/                    # (Agent: Tasks 5.1-5.3)
│   │       ├── __init__.py
│   │       ├── json_exporter.py
│   │       ├── excel_exporter.py
│   │       └── report_generator.py
│   │
│   ├── core/                             # Infrastructure (Agent: Task 1.2)
│   │   ├── __init__.py
│   │   ├── orchestrator.py               # (Agent: Task 6.1)
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── constants.py
│   │
│   ├── config/                           # ✅ Configuration files created
│   │   ├── field_mappings.yaml           # ✅ COMPLETE
│   │   ├── cost_rules.yaml               # ✅ COMPLETE
│   │   ├── validation_rules.yaml         # ✅ COMPLETE
│   │   ├── transfer_rules.yaml           # ✅ COMPLETE
│   │   ├── cost_catalog.json             # (Copy from ../config/)
│   │   ├── cost_catalog_mpc_2026.json    # (Copy from ../config/)
│   │   └── system_names.json             # (Copy from ../config/)
│   │
│   ├── tests/                            # Test suite (Agent: Task 7.1-7.2)
│   │   ├── __init__.py
│   │   ├── conftest.py                   # Shared fixtures
│   │   ├── test_models.py
│   │   ├── test_extractors.py
│   │   ├── test_validators.py
│   │   ├── test_transformers.py
│   │   ├── test_exporters.py
│   │   ├── test_integration.py
│   │   └── test_v1_v2_comparison.py      # (Agent: Task 8.1)
│   │
│   ├── docs/                             # Documentation (Agent: Task 7.3)
│   │   ├── ARCHITECTURE.md
│   │   ├── API.md
│   │   └── MIGRATION_FROM_V1.md
│   │
│   ├── AGENT_EXECUTION_PLAN.md           # ✅ COMPLETE - Agent task queue
│   ├── MODELS_SPEC.md                    # ✅ COMPLETE - Data model specs
│   ├── BUILD_ORCHESTRATION.md            # ✅ COMPLETE - Execution guide
│   ├── README.md                         # ✅ COMPLETE - V2 overview
│   ├── main.py                           # CLI entry (Agent: Task 6.2)
│   └── requirements.txt                  # Python dependencies
│
├── v1_archive/                           # ✅ V1.0 Code Archived
│   ├── scripts/                          # ✅ MOVED from root scripts/
│   │   ├── xml_parser.py
│   │   ├── cost_calculator.py
│   │   ├── excel_generator.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── parse_utilization_csvs.py
│   │   ├── debug_duplicates.py
│   │   ├── debug_excel.py
│   │   ├── debug_fields.py
│   │   ├── debug_merge.py
│   │   └── license_history.db
│   │
│   ├── V1_REFERENCE.md                   # (Create: V1 behavior documentation)
│   └── V1_MIGRATION_NOTES.md             # (Create: Known issues and fixes)
│
├── config/                               # Existing config (shared)
│   ├── settings.json
│   ├── cost_catalog.json
│   ├── cost_catalog_mpc_2026.json
│   └── system_names.json
│
├── data/                                 # Data directories
│   ├── raw/                              # Original XML/CSV files
│   │   ├── Carson/
│   │   ├── Wilmington/
│   │   └── Usage/
│   │
│   ├── validated/                        # NEW - After validation gate
│   │   ├── licenses.json
│   │   ├── usage.json
│   │   └── errors.json
│   │
│   ├── enriched/                         # NEW - After transformation
│   │   ├── merged.json
│   │   ├── costs.json
│   │   └── transfers.json
│   │
│   ├── output/                           # Final reports
│   │   └── Experion_License_Report_*.xlsx
│   │
│   └── checkpoints/                      # NEW - Agent progress tracking
│       ├── task_1_1_complete.json
│       ├── task_1_2_complete.json
│       └── current_phase.json
│
├── templates/                            # Existing templates
├── DATA_PROCESSING_GUIDE.md              # ✅ Existing V1 documentation
├── README.md                             # Root README (update to reference V2)
├── QUICK_START.txt                       # Existing quick start
├── requirements.txt                      # Root requirements
└── migrate_to_v2.py                      # (Agent: Task 8.2)
```

---

## 📂 V1 Archive Organization (v1_archive/)

**Purpose**: Preserve V1.0 code for reference and comparison

### **What Was Moved**
- ✅ `scripts/` → `v1_archive/scripts/`
  - All Python modules (xml_parser.py, cost_calculator.py, etc.)
  - All debug scripts (debug_*.py)
  - SQLite database (license_history.db)

### **What Stays in Root**
- `config/` - Configuration files (shared between V1 and V2)
- `data/` - Data directories (shared)
- `templates/` - Excel templates
- Documentation files (README.md, DATA_PROCESSING_GUIDE.md, etc.)

---

## 🎯 Agent Tasks - File Creation Checklist

### **Phase 1: Foundation**
- [ ] `v2/models/__init__.py`
- [ ] `v2/models/license.py`
- [ ] `v2/models/usage.py`
- [ ] `v2/models/enriched_license.py`
- [ ] `v2/models/cost.py`
- [ ] `v2/models/transfer.py`
- [ ] `v2/core/__init__.py`
- [ ] `v2/core/exceptions.py`
- [ ] `v2/core/config.py`
- [ ] `v2/core/constants.py`
- [✅] `v2/config/field_mappings.yaml`
- [✅] `v2/config/cost_rules.yaml`
- [✅] `v2/config/validation_rules.yaml`
- [✅] `v2/config/transfer_rules.yaml`
- [ ] Copy `config/*.json` to `v2/config/`

### **Phase 2: Extraction**
- [ ] `v2/pipeline/extractors/__init__.py`
- [ ] `v2/pipeline/extractors/base_extractor.py`
- [ ] `v2/pipeline/extractors/xml_extractor.py`
- [ ] `v2/pipeline/extractors/csv_extractor.py`
- [ ] `v2/pipeline/extractors/config_loader.py`

### **Phase 3: Validation**
- [ ] `v2/pipeline/validators/__init__.py`
- [ ] `v2/pipeline/validators/base_validator.py`
- [ ] `v2/pipeline/validators/schema_validator.py`
- [ ] `v2/pipeline/validators/business_validator.py`
- [ ] `v2/pipeline/validators/match_validator.py`

### **Phase 4: Transformation**
- [ ] `v2/pipeline/transformers/__init__.py`
- [ ] `v2/pipeline/transformers/deduplicator.py`
- [ ] `v2/pipeline/transformers/field_mapper.py`
- [ ] `v2/pipeline/transformers/usage_matcher.py`
- [ ] `v2/pipeline/transformers/cost_calculator.py`
- [ ] `v2/pipeline/transformers/transfer_detector.py`

### **Phase 5: Export**
- [ ] `v2/pipeline/exporters/__init__.py`
- [ ] `v2/pipeline/exporters/json_exporter.py`
- [ ] `v2/pipeline/exporters/excel_exporter.py`
- [ ] `v2/pipeline/exporters/report_generator.py`

### **Phase 6: Orchestration**
- [ ] `v2/core/orchestrator.py`
- [ ] `v2/main.py`
- [ ] `v2/requirements.txt`

### **Phase 7: Testing**
- [ ] `v2/tests/__init__.py`
- [ ] `v2/tests/conftest.py`
- [ ] `v2/tests/test_models.py`
- [ ] `v2/tests/test_extractors.py`
- [ ] `v2/tests/test_validators.py`
- [ ] `v2/tests/test_transformers.py`
- [ ] `v2/tests/test_exporters.py`
- [ ] `v2/tests/test_integration.py`
- [ ] `v2/docs/ARCHITECTURE.md`
- [ ] `v2/docs/API.md`
- [ ] `v2/docs/MIGRATION_FROM_V1.md`

### **Phase 8: Validation**
- [ ] `v2/tests/test_v1_v2_comparison.py`
- [ ] `migrate_to_v2.py` (root level)
- [ ] `v1_archive/V1_REFERENCE.md`
- [ ] `v1_archive/V1_MIGRATION_NOTES.md`

### **Supporting Documentation** (✅ Already Created)
- [✅] `v2/AGENT_EXECUTION_PLAN.md`
- [✅] `v2/MODELS_SPEC.md`
- [✅] `v2/BUILD_ORCHESTRATION.md`
- [✅] `v2/README.md`
- [✅] This file: `v2/FOLDER_STRUCTURE.md`

---

## 🚀 Quick Start for Agents

### **Step 1: Verify Structure**
```bash
cd C:\Users\GF99\Documentation\Experion_License_Aggregator
tree v2 /F  # Windows
```

### **Step 2: Copy Existing Config**
```bash
Copy-Item config\cost_catalog.json v2\config\
Copy-Item config\cost_catalog_mpc_2026.json v2\config\
Copy-Item config\system_names.json v2\config\
Copy-Item config\settings.json v2\config\
```

### **Step 3: Start Agent Execution**
```bash
# Read execution plan
cat v2\AGENT_EXECUTION_PLAN.md

# Begin Phase 1
agent execute --plan v2\AGENT_EXECUTION_PLAN.md --phase 1
```

---

## 📊 File Count Summary

| Category | V1 (Archived) | V2 (To Build) | Shared |
|----------|--------------|---------------|--------|
| Python Modules | 9 | ~35 | 0 |
| Config Files | 0 | 4 YAML | 4 JSON |
| Test Files | 0 | ~10 | 0 |
| Documentation | 1 | 7 | 5 |
| Debug Scripts | 5 | 0 | 0 |
| **Total** | **15** | **~56** | **9** |

---

## ✅ Completion Status

### **Infrastructure Setup**
- [✅] V2 directory structure created
- [✅] V1 scripts moved to v1_archive/
- [✅] Configuration YAML files created
- [✅] Documentation framework established
- [✅] Agent execution plan written

### **Ready for Agent Build**
- [✅] Folder structure complete
- [✅] Specifications written
- [✅] Config files created
- [✅] V1 code archived for reference
- [ ] Agent execution (pending)

---

**Status**: Ready for autonomous agent execution  
**Next Step**: Begin Phase 1 (Foundation) - Task 1.1  
**Last Updated**: January 28, 2026
