# Experion License Aggregator V2.0

**Complete Rewrite**: Data-first ETL architecture with validation-driven design  
**Status**: Under Development - Agent-Executable Build Plan  
**Target**: Zero debug scripts, 100% data quality visibility

---

## 🎯 What's New in V2.0

### **Core Architecture Changes**

| V1.0 (Legacy) | V2.0 (Current) |
|---------------|----------------|
| Dict-based data passing | **Typed data models** with validation |
| Late error detection | **Validation gates** at each stage |
| Hardcoded logic | **Config-driven** business rules |
| Single-pass processing | **Staged pipeline** with checkpoints |
| Manual debugging | **Self-healing** with quality reports |
| 5+ debug scripts | **Zero scripts** needed |

### **Key Improvements**

1. **Data Models with Validation**
   - `LicenseData`, `UsageData`, `EnrichedLicense` dataclasses
   - Validation at construction time catches errors early
   - Type safety prevents runtime errors

2. **Validation Pipeline**
   - Schema validation (required fields)
   - Business validation (age, customer name, ranges)
   - Match validation (XML↔CSV confidence scoring)
   - Data quality dashboard in Excel output

3. **Configuration-Driven**
   - `field_mappings.yaml` - XML↔CSV field mappings
   - `cost_rules.yaml` - Pricing cascade configuration
   - `validation_rules.yaml` - Business rules
   - `transfer_rules.yaml` - Transfer candidate criteria
   - **Change behavior without editing code**

4. **Staged Processing with Checkpoints**
   ```
   data/
   ├── raw/          # Original XML/CSV
   ├── validated/    # After validation gate
   ├── enriched/     # After merging + cost calc
   └── output/       # Final reports
   ```
   - Debug faster: Load `validated/licenses.json` to skip re-parsing
   - Test independently: Load `enriched/merged.json` for Excel development
   - Resume on failure: Pick up from last checkpoint

5. **Fuzzy Matching**
   - Exact match: `(cluster, msid, system_number)`
   - Fuzzy MSID matching for variants (M0922 vs M0922-01)
   - Confidence scoring (0.0 to 1.0) with audit trail

6. **Data Quality Dashboard**
   - New Excel sheet showing all validation issues
   - Group by error type (Missing MSID, No Usage Data, etc.)
   - Severity levels (ERROR, WARNING, INFO)
   - Match confidence for each system

---

## 📁 Directory Structure

```
v2/
├── models/                    # Data models (100% test coverage required)
│   ├── license.py            # LicenseData with validation
│   ├── usage.py              # UsageData from CSV
│   ├── enriched_license.py   # License + usage + cost
│   ├── cost.py               # CostCalculation with audit trail
│   └── transfer.py           # TransferCandidate detection
│
├── pipeline/                  # Processing stages
│   ├── extractors/           # Data extraction
│   │   ├── xml_extractor.py  # Parse XML to LicenseData
│   │   ├── csv_extractor.py  # Parse CSV to UsageData
│   │   └── config_loader.py  # Load YAML/JSON configs
│   │
│   ├── validators/           # Validation gates
│   │   ├── schema_validator.py      # Required fields
│   │   ├── business_validator.py    # Business rules
│   │   └── match_validator.py       # Fuzzy matching
│   │
│   ├── transformers/         # Data transformation
│   │   ├── deduplicator.py   # Version-based deduplication
│   │   ├── field_mapper.py   # Apply field_mappings.yaml
│   │   ├── usage_matcher.py  # XML↔CSV matching
│   │   ├── cost_calculator.py # Pricing cascade
│   │   └── transfer_detector.py # Transfer candidates
│   │
│   └── exporters/            # Output generation
│       ├── json_exporter.py  # For BI tools
│       ├── excel_exporter.py # Main Excel report
│       └── report_generator.py # Validation dashboard
│
├── core/                     # Infrastructure
│   ├── orchestrator.py       # Pipeline coordinator
│   ├── config.py             # Config management
│   ├── exceptions.py         # Custom exceptions
│   └── constants.py          # Enums (LicenseType, etc.)
│
├── config/                   # Configuration files
│   ├── field_mappings.yaml   # XML↔CSV mappings
│   ├── cost_rules.yaml       # Pricing cascade
│   ├── validation_rules.yaml # Business rules
│   ├── transfer_rules.yaml   # Transfer criteria
│   ├── cost_catalog.json     # Honeywell pricing
│   ├── cost_catalog_mpc_2026.json # MPC 2026 overrides
│   └── system_names.json     # Friendly names
│
├── tests/                    # Test suite (>80% coverage target)
│   ├── test_models.py
│   ├── test_extractors.py
│   ├── test_validators.py
│   ├── test_transformers.py
│   ├── test_integration.py
│   └── conftest.py           # Shared fixtures
│
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md       # System design
│   ├── API.md                # Public API reference
│   └── MIGRATION_FROM_V1.md  # Upgrade guide
│
├── AGENT_EXECUTION_PLAN.md   # Agent build instructions
├── MODELS_SPEC.md            # Data model specifications
├── CONFIG_SPEC.md            # Configuration guide
├── README.md                 # This file
└── main.py                   # CLI entry point
```

---

## 🚀 Quick Start

### **Prerequisites**

```bash
# Python 3.10+
python --version

# Virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### **Run V2 Pipeline**

```bash
# Standard run
python v2/main.py

# Verbose output
python v2/main.py --verbose

# Resume from checkpoint
python v2/main.py --stage transformation

# Export JSON for BI tools
python v2/main.py --export-json
```

### **Configuration**

All behavior controlled by YAML files in `v2/config/`:

1. **Edit field mappings**: `field_mappings.yaml`
2. **Adjust validation rules**: `validation_rules.yaml`
3. **Change transfer criteria**: `transfer_rules.yaml`
4. **Update pricing**: Edit JSON catalogs

No code changes needed for business rule adjustments!

---

## 📊 Output Files

### **Excel Report** (`data/output/Experion_License_Report_*.xlsx`)

| Sheet | Description |
|-------|-------------|
| **PKS** | All PKS systems (pivot table format) |
| **Transfer Candidates** | Systems with excess capacity |
| **Data Quality** | **NEW** Validation issues dashboard |
| **Summary** | Totals by cluster with costs |
| **Changes** | Differences from previous run |

### **JSON Exports** (optional with `--export-json`)

- `data/validated/licenses.json` - All parsed licenses
- `data/enriched/merged.json` - Licenses + usage + costs
- `data/output/transfer_candidates.json` - Transfer analysis

### **Intermediate Checkpoints**

- `data/validated/` - After validation gate
- `data/enriched/` - After transformation
- **Use for debugging without re-parsing XML**

---

## 🧪 Testing

```bash
# Run all tests
pytest v2/tests/

# With coverage report
pytest v2/tests/ --cov=v2 --cov-report=html

# Specific module
pytest v2/tests/test_models.py -v

# Integration tests only
pytest v2/tests/test_integration.py
```

**Coverage Target**: >80% overall, 100% for data models

---

## 🛠️ Development Workflow

### **Agent-Driven Development**

See [`AGENT_EXECUTION_PLAN.md`](AGENT_EXECUTION_PLAN.md) for complete autonomous build plan.

**Quick Summary**:
1. Phase 1: Foundation (models + core)
2. Phase 2: Extraction (XML/CSV parsers)
3. Phase 3: Validation (quality gates)
4. Phase 4: Transformation (matching + costs)
5. Phase 5: Export (Excel + JSON)
6. Phase 6: Orchestration (pipeline coordinator)
7. Phase 7: Testing (>80% coverage)
8. Phase 8: Migration (V1 comparison)

### **Manual Development**

```bash
# Create new module
touch v2/pipeline/transformers/new_module.py

# Write tests first (TDD)
touch v2/tests/test_new_module.py
pytest v2/tests/test_new_module.py  # Should fail

# Implement module
# ... write code ...

# Run tests
pytest v2/tests/test_new_module.py  # Should pass

# Check coverage
pytest --cov=v2/pipeline/transformers/new_module
```

---

## 🔧 Configuration Examples

### **Add New Field Mapping**

```yaml
# v2/config/field_mappings.yaml
license_to_usage:
  NEW_LICENSE_FIELD: CSV_USAGE_FIELD
```

### **Adjust Transfer Criteria**

```yaml
# v2/config/transfer_rules.yaml
criteria:
  PROCESSPOINTS:
    - name: "Absolute Excess"
      threshold: 1000  # Changed from 500
```

### **Update Pricing**

```json
// v2/config/cost_catalog_mpc_2026.json
{
  "NEW_LICENSE_TYPE": {
    "unit_cost": 25.00,
    "per": 10,
    "category": "Features"
  }
}
```

---

## 📚 Documentation

- **[AGENT_EXECUTION_PLAN.md](AGENT_EXECUTION_PLAN.md)** - Complete agent build instructions
- **[MODELS_SPEC.md](MODELS_SPEC.md)** - Data model specifications
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design (TBD)
- **[docs/API.md](docs/API.md)** - Public API reference (TBD)
- **[docs/MIGRATION_FROM_V1.md](docs/MIGRATION_FROM_V1.md)** - V1 → V2 upgrade guide (TBD)

---

## 🔄 Migration from V1.0

**V1.0 Code Location**: See `../v1_archive/` directory

### **Key Differences**

| Aspect | V1.0 | V2.0 |
|--------|------|------|
| **Data structures** | Dicts | Typed dataclasses |
| **Validation** | Ad-hoc | Staged pipeline |
| **Configuration** | JSON only | YAML + JSON |
| **Error handling** | Print statements | Structured exceptions |
| **Testing** | Manual | pytest (>80%) |
| **Debugging** | Multiple scripts | Checkpoints + quality dashboard |
| **Field mapping** | Hardcoded | Config file |
| **Cost calculation** | Embedded logic | Config-driven cascade |

### **Migration Steps**

1. Keep V1.0 running (moved to `v1_archive/`)
2. Build V2.0 using agent execution plan
3. Run both in parallel for 2-3 cycles
4. Compare outputs: `pytest tests/test_v1_v2_comparison.py`
5. Switch to V2.0 after validation
6. Archive V1.0 permanently

---

## ⚠️ Known Limitations (TBD - To Be Implemented)

- [ ] **HS/EAS Sheets**: Separate sheets for High Security and EAS systems
- [ ] **Historical Comparison**: Change detection vs previous run
- [ ] **Database Integration**: SQLite history tracking
- [ ] **Web UI**: Browser-based report viewing

---

## 🤝 Contributing

### **For Agents**

Follow [`AGENT_EXECUTION_PLAN.md`](AGENT_EXECUTION_PLAN.md) task queue.

### **For Humans**

1. Read specification files in `v2/`
2. Write tests first (TDD)
3. Follow type hints and docstrings
4. Run `pytest` before committing
5. Update documentation

---

## 📈 Success Metrics

| Metric | V1.0 | V2.0 Target |
|--------|------|-------------|
| Debug Scripts Needed | 5+ | 0 |
| Data Quality Visibility | Manual inspection | Automated dashboard |
| Configuration Changes | Edit Python code | Edit YAML files |
| Test Coverage | <20% | >80% |
| Onboarding Time | 1-2 days | 2-4 hours |
| Error Recovery | Re-run entire pipeline | Resume from checkpoint |

---

## 📞 Support

- **V2 Architecture Questions**: See `docs/ARCHITECTURE.md`
- **Agent Execution**: See `AGENT_EXECUTION_PLAN.md`
- **V1 Reference**: See `../v1_archive/`
- **Current Data**: See `../data/raw/`

---

## 📄 License

Internal tool for Marathon Petroleum Corporation. Not for external distribution.

---

**Version**: 2.0.0-dev  
**Last Updated**: January 28, 2026  
**Status**: Under Active Development
