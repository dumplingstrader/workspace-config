# Experion License Aggregator V2.0 - Agent Execution Plan

**Project**: Clean rewrite with data-first ETL architecture  
**Execution Mode**: Autonomous - agents can build without human input  
**Target**: Production-ready V2.0 with zero debug scripts needed

---

## 🎯 **Execution Objectives**

1. **Zero Manual Intervention**: Agents complete all tasks autonomously using specs
2. **Test-Driven**: All modules have >80% test coverage before integration
3. **Validation-First**: Data quality gates prevent bad data propagation
4. **Self-Documenting**: Code includes docstrings, type hints, and inline comments

---

## 📋 **Agent Task Queue**

### **Phase 1: Foundation (Priority: CRITICAL)**

#### **Task 1.1: Data Models (models/)**
**Agent**: Code Generator  
**Duration**: 2 hours  
**Dependencies**: None

**Deliverables**:
- `models/license.py` - LicenseData dataclass with validation
- `models/usage.py` - UsageData dataclass  
- `models/cost.py` - CostCalculation dataclass
- `models/transfer.py` - TransferCandidate dataclass
- `models/__init__.py` - Public API exports

**Acceptance Criteria**:
```python
# Test must pass
license = LicenseData(
    msid='M0614',
    system_number='60806',
    cluster='Carson',
    release='R520',
    license_date=datetime(2024, 1, 15),
    file_version=40,
    licensed={'PROCESSPOINTS': 4750}
)
assert license.unique_key == ('Carson', 'M0614', '60806')
assert license.get_licensed_quantity('PROCESSPOINTS') == 4750

# Validation must catch errors
with pytest.raises(ValidationError):
    LicenseData(msid='', system_number='60806', ...)  # Empty MSID
```

**Implementation Guide**: See `MODELS_SPEC.md`

---

#### **Task 1.2: Core Infrastructure (core/)**
**Agent**: Code Generator  
**Duration**: 1 hour  
**Dependencies**: Task 1.1

**Deliverables**:
- `core/exceptions.py` - Custom exception hierarchy
- `core/config.py` - Configuration management
- `core/constants.py` - Enums for LicenseType, ValidationLevel, etc.
- `core/__init__.py` - Public API

**Acceptance Criteria**:
```python
# Config loading
config = Config.from_directory('config/')
assert 'Carson' in config.clusters
assert config.get_cost_for('PROCESSPOINTS') == 45.00

# Exception hierarchy
try:
    raise XmlParsingError("Bad XML", file_path="test.xml")
except DataExtractionError as e:  # Parent class
    assert e.file_path == "test.xml"
```

**Implementation Guide**: See `CORE_SPEC.md`

---

#### **Task 1.3: Configuration Files (config/)**
**Agent**: Configuration Writer  
**Duration**: 30 minutes  
**Dependencies**: Task 1.2

**Deliverables**:
- `config/field_mappings.yaml` - XML↔CSV field mappings
- `config/cost_rules.yaml` - Pricing cascade configuration
- `config/validation_rules.yaml` - Business validation rules
- `config/transfer_rules.yaml` - Transfer candidate criteria

**Acceptance Criteria**:
```yaml
# field_mappings.yaml must define
license_to_usage:
  DIRECTSTATIONS: CONSOLE_STATIONS
  PROCESSPOINTS: PROCESSPOINTS

# cost_rules.yaml must define cascade
pricing_strategy:
  - name: "MPC 2026 Confirmed"
    priority: 1
    source: cost_catalog_mpc_2026.json
```

**Implementation Guide**: See `CONFIG_SPEC.md`

---

### **Phase 2: Data Extraction (Priority: HIGH)**

#### **Task 2.1: XML Extractor (pipeline/extractors/)**
**Agent**: Code Generator  
**Duration**: 3 hours  
**Dependencies**: Task 1.1, 1.2

**Deliverables**:
- `pipeline/extractors/xml_extractor.py` - Parse XML to LicenseData
- `pipeline/extractors/base_extractor.py` - Abstract base class
- Unit tests with sample XML files

**Acceptance Criteria**:
```python
extractor = XmlExtractor()
result = extractor.extract_from_file('test_data/M0614_R520_x_60806_40.xml')

assert result.success == True
assert result.data.msid == 'M0614'
assert result.data.system_number == '60806'
assert result.data.file_version == 40
assert result.data.licensed['PROCESSPOINTS'] == 4750
assert len(result.warnings) == 0  # No validation warnings
```

**Implementation Guide**: See `EXTRACTOR_SPEC.md`

---

#### **Task 2.2: CSV Extractor (pipeline/extractors/)**
**Agent**: Code Generator  
**Duration**: 2 hours  
**Dependencies**: Task 1.1, 1.2

**Deliverables**:
- `pipeline/extractors/csv_extractor.py` - Parse Station Manager CSV
- Unit tests with sample CSV

**Acceptance Criteria**:
```python
extractor = CsvExtractor()
result = extractor.extract_from_file('test_data/BC-LAR-ENGPRO022.csv')

assert result.success == True
assert result.data.msid == 'M0614'
assert result.data.usage['PROCESSPOINTS'] == 108
assert result.data.usage['CONSOLE_STATIONS'] == 4
```

**Implementation Guide**: See `EXTRACTOR_SPEC.md`

---

#### **Task 2.3: Config Loader (pipeline/extractors/)**
**Agent**: Code Generator  
**Duration**: 1 hour  
**Dependencies**: Task 1.2, 1.3

**Deliverables**:
- `pipeline/extractors/config_loader.py` - Load YAML configs and JSON catalogs
- Validation for required fields

**Acceptance Criteria**:
```python
loader = ConfigLoader(base_path='config/')
field_map = loader.get_field_mappings()
assert field_map['DIRECTSTATIONS'] == 'CONSOLE_STATIONS'

cost_cascade = loader.get_cost_cascade()
assert cost_cascade[0].name == "MPC 2026 Confirmed"
```

---

### **Phase 3: Validation Layer (Priority: HIGH)**

#### **Task 3.1: Schema Validator (pipeline/validators/)**
**Agent**: Code Generator  
**Duration**: 2 hours  
**Dependencies**: Task 1.1, 1.2

**Deliverables**:
- `pipeline/validators/schema_validator.py` - Check required fields
- `pipeline/validators/base_validator.py` - Abstract base

**Acceptance Criteria**:
```python
validator = SchemaValidator()
result = validator.validate(license_data)

# Pass case
assert result.passed == True
assert len(result.errors) == 0

# Fail case
bad_license = LicenseData(msid='Unknown', ...)
result = validator.validate(bad_license)
assert result.passed == False
assert 'Invalid MSID' in result.errors[0]
```

**Implementation Guide**: See `VALIDATOR_SPEC.md`

---

#### **Task 3.2: Business Validator (pipeline/validators/)**
**Agent**: Code Generator  
**Duration**: 2 hours  
**Dependencies**: Task 1.3, 3.1

**Deliverables**:
- `pipeline/validators/business_validator.py` - Apply rules from config
- Load validation_rules.yaml

**Acceptance Criteria**:
```python
validator = BusinessValidator(config)
result = validator.validate(license_data)

# Check license age
if license_data.license_date < (now - 730 days):
    assert 'Stale license' in result.warnings

# Check customer name
if 'Marathon' not in license_data.customer:
    assert 'Invalid customer' in result.warnings
```

---

#### **Task 3.3: Match Validator (pipeline/validators/)**
**Agent**: Code Generator  
**Duration**: 2 hours  
**Dependencies**: Task 3.1

**Deliverables**:
- `pipeline/validators/match_validator.py` - Verify XML↔CSV matches
- Fuzzy matching for MSID variations

**Acceptance Criteria**:
```python
validator = MatchValidator()
result = validator.find_match(license_data, csv_data_list)

# Exact match
assert result.confidence == 1.0
assert result.method == 'exact'

# Fuzzy match
result = validator.find_match(license_with_variant_msid, csv_data_list)
assert result.confidence >= 0.8
assert result.method == 'fuzzy_msid'
```

---

### **Phase 4: Data Transformation (Priority: HIGH)**

#### **Task 4.1: Deduplicator (pipeline/transformers/)**
**Agent**: Code Generator  
**Duration**: 2 hours  
**Dependencies**: Task 1.1

**Deliverables**:
- `pipeline/transformers/deduplicator.py` - Version-based deduplication
- Conflict resolution logic

**Acceptance Criteria**:
```python
deduplicator = Deduplicator()
licenses = [
    LicenseData(..., file_version=29),
    LicenseData(..., file_version=40),  # Same system
]
result = deduplicator.deduplicate(licenses)

assert len(result.unique_licenses) == 1
assert result.unique_licenses[0].file_version == 40  # Highest
assert len(result.duplicates_removed) == 1
```

---

#### **Task 4.2: Field Mapper (pipeline/transformers/)**
**Agent**: Code Generator  
**Duration**: 2 hours  
**Dependencies**: Task 1.3

**Deliverables**:
- `pipeline/transformers/field_mapper.py` - Apply field_mappings.yaml
- Handle fallback chains

**Acceptance Criteria**:
```python
mapper = FieldMapper(config)
mapped = mapper.map_usage_to_license(usage_data, 'DIRECTSTATIONS')

# Primary mapping
assert mapped == usage_data.usage['CONSOLE_STATIONS']

# Fallback chain
mapped = mapper.map_usage_to_license(usage_data, 'STATIONS')
if 'STATIONS' not in usage_data.usage:
    assert mapped == usage_data.usage['MULTISTATIONS']  # Fallback
```

---

#### **Task 4.3: Usage Matcher (pipeline/transformers/)**
**Agent**: Code Generator  
**Duration**: 3 hours  
**Dependencies**: Task 3.3, 4.2

**Deliverables**:
- `pipeline/transformers/usage_matcher.py` - Match XML licenses to CSV usage
- Exact + fuzzy matching strategies

**Acceptance Criteria**:
```python
matcher = UsageMatcher(field_mapper, validator)
result = matcher.match(licenses, usage_data_list)

assert result.matched_count == 20
assert result.unmatched_licenses == 16
assert all(lic.usage is not None for lic in result.matched)

# Check match quality
for match_result in result.matches:
    assert match_result.confidence >= 0.8
```

---

#### **Task 4.4: Cost Calculator (pipeline/transformers/)**
**Agent**: Code Generator  
**Duration**: 2 hours  
**Dependencies**: Task 1.3, 4.1

**Deliverables**:
- `pipeline/transformers/cost_calculator.py` - Calculate costs with cascade
- Track pricing source

**Acceptance Criteria**:
```python
calculator = CostCalculator(config)
result = calculator.calculate(license_data)

assert result.total_cost > 0
assert 'PROCESSPOINTS' in result.breakdown
assert result.breakdown['PROCESSPOINTS'].source == 'MPC 2026 Confirmed'
assert result.breakdown['PROCESSPOINTS'].unit_cost == 45.00
```

---

#### **Task 4.5: Transfer Detector (pipeline/transformers/)**
**Agent**: Code Generator  
**Duration**: 2 hours  
**Dependencies**: Task 1.3, 4.3

**Deliverables**:
- `pipeline/transformers/transfer_detector.py` - Identify transfer candidates
- Apply transfer_rules.yaml

**Acceptance Criteria**:
```python
detector = TransferDetector(config)
result = detector.detect(enriched_licenses)

assert len(result.candidates) > 0
for candidate in result.candidates:
    assert candidate.excess >= 500 or candidate.utilization <= 75
    assert candidate.excess_value >= 1000
```

---

### **Phase 5: Data Export (Priority: MEDIUM)**

#### **Task 5.1: JSON Exporter (pipeline/exporters/)**
**Agent**: Code Generator  
**Duration**: 1 hour  
**Dependencies**: Task 1.1

**Deliverables**:
- `pipeline/exporters/json_exporter.py` - Export to JSON for BI tools
- Include metadata (validation status, confidence)

**Acceptance Criteria**:
```python
exporter = JsonExporter()
exporter.export(enriched_licenses, 'output/licenses.json')

data = json.load(open('output/licenses.json'))
assert 'licenses' in data
assert 'metadata' in data
assert data['metadata']['validation_passed'] >= 0
```

---

#### **Task 5.2: Excel Exporter (pipeline/exporters/)**
**Agent**: Code Generator  
**Duration**: 4 hours  
**Dependencies**: Task 4.5

**Deliverables**:
- `pipeline/exporters/excel_exporter.py` - Generate Excel with pivot format
- Data-driven templates (no hardcoded rows)
- Conditional formatting

**Acceptance Criteria**:
```python
exporter = ExcelExporter(config)
exporter.export(enriched_licenses, 'output/report.xlsx')

wb = load_workbook('output/report.xlsx')
assert 'PKS' in wb.sheetnames
assert 'Transfer Candidates' in wb.sheetnames
assert 'Data Quality' in wb.sheetnames

# Verify no hardcoded row numbers
# All row positions calculated from data
```

**Implementation Guide**: See `EXCEL_EXPORTER_SPEC.md`

---

#### **Task 5.3: Validation Report Generator (pipeline/exporters/)**
**Agent**: Code Generator  
**Duration**: 2 hours  
**Dependencies**: Task 3.1, 3.2

**Deliverables**:
- `pipeline/exporters/report_generator.py` - Data quality dashboard
- Export errors.json and create Excel sheet

**Acceptance Criteria**:
```python
generator = ReportGenerator()
generator.export(validation_results, 'output/data_quality.xlsx')

wb = load_workbook('output/data_quality.xlsx')
ws = wb['Validation Summary']
assert ws['A1'].value == 'Issue Type'
# Check rows for each error type
```

---

### **Phase 6: Orchestration (Priority: MEDIUM)**

#### **Task 6.1: Pipeline Orchestrator (core/)**
**Agent**: Code Generator  
**Duration**: 3 hours  
**Dependencies**: All Phase 2-5 tasks

**Deliverables**:
- `core/orchestrator.py` - Main pipeline coordinator
- Stage-by-stage execution with checkpoints
- Error recovery and resume capability

**Acceptance Criteria**:
```python
orchestrator = PipelineOrchestrator(config)
result = orchestrator.run()

assert result.success == True
assert result.stages['extraction'].success == True
assert result.stages['validation'].passed >= 20
assert result.stages['transformation'].matched >= 20
assert result.stages['export'].files_created > 0

# Check intermediate outputs
assert Path('data/validated/licenses.json').exists()
assert Path('data/enriched/merged.json').exists()
```

**Implementation Guide**: See `ORCHESTRATOR_SPEC.md`

---

#### **Task 6.2: CLI Entry Point (v2/)**
**Agent**: Code Generator  
**Duration**: 1 hour  
**Dependencies**: Task 6.1

**Deliverables**:
- `main.py` - Command-line interface
- Argument parsing and progress display

**Acceptance Criteria**:
```bash
python main.py --help  # Shows all options
python main.py --verbose  # Runs with detailed logging
python main.py --stage validation  # Resume from checkpoint
python main.py --export-json  # Include JSON export
```

---

### **Phase 7: Testing & Documentation (Priority: HIGH)**

#### **Task 7.1: Unit Tests (tests/)**
**Agent**: Test Generator  
**Duration**: 4 hours  
**Dependencies**: All Phase 1-5 tasks

**Deliverables**:
- `tests/test_models.py` - Test all data models
- `tests/test_extractors.py` - Test XML/CSV parsing
- `tests/test_validators.py` - Test validation logic
- `tests/test_transformers.py` - Test dedup/match/cost
- `tests/conftest.py` - Shared fixtures

**Acceptance Criteria**:
```bash
pytest tests/ --cov=v2 --cov-report=html
# Must achieve >80% coverage
# All tests must pass
```

---

#### **Task 7.2: Integration Tests (tests/)**
**Agent**: Test Generator  
**Duration**: 2 hours  
**Dependencies**: Task 6.1

**Deliverables**:
- `tests/test_integration.py` - End-to-end pipeline tests
- Use real XML/CSV samples

**Acceptance Criteria**:
```python
def test_full_pipeline():
    orchestrator = PipelineOrchestrator(test_config)
    result = orchestrator.run()
    
    assert result.success == True
    assert Path('output/report.xlsx').exists()
    # Compare with expected output
```

---

#### **Task 7.3: Documentation (v2/docs/)**
**Agent**: Documentation Writer  
**Duration**: 3 hours  
**Dependencies**: All tasks

**Deliverables**:
- `README.md` - V2.0 overview and quick start
- `ARCHITECTURE.md` - System design documentation
- `API.md` - Public API reference
- `MIGRATION_FROM_V1.md` - Upgrade guide

**Acceptance Criteria**:
- All public classes/functions documented
- Example code for each module
- Architecture diagrams (text/ASCII)
- Migration checklist

---

### **Phase 8: Validation & Migration (Priority: CRITICAL)**

#### **Task 8.1: V1 vs V2 Output Comparison**
**Agent**: Test Generator  
**Duration**: 2 hours  
**Dependencies**: All previous tasks

**Deliverables**:
- `tests/test_v1_v2_comparison.py` - Compare outputs
- Validation script

**Acceptance Criteria**:
```python
def test_output_matches():
    # Run V1
    v1_result = run_v1_pipeline()
    
    # Run V2
    v2_result = run_v2_pipeline()
    
    # Compare
    assert v1_result.system_count == v2_result.system_count
    assert_close(v1_result.total_cost, v2_result.total_cost, tolerance=0.01)
    # All systems present in both outputs
```

---

#### **Task 8.2: Migration Script**
**Agent**: Code Generator  
**Duration**: 1 hour  
**Dependencies**: Task 8.1

**Deliverables**:
- `migrate_to_v2.py` - One-time migration script
- Backup V1 data, run V2, validate

**Acceptance Criteria**:
```bash
python migrate_to_v2.py --backup --validate
# Creates v1_archive/
# Runs V2 pipeline
# Compares outputs
# Generates migration report
```

---

## 🤖 **Agent Autonomy Guidelines**

### **For Code Generation Agents**

1. **Always include**:
   - Type hints for all functions
   - Docstrings (Google style)
   - Error handling with custom exceptions
   - Logging statements (DEBUG, INFO, WARNING, ERROR)
   - Input validation

2. **Testing requirements**:
   - Write tests BEFORE implementation (TDD)
   - Each test must be independent
   - Use pytest fixtures for shared setup
   - Mock external dependencies (file I/O, network)

3. **Code quality**:
   - Follow PEP 8 style guide
   - Use dataclasses for data structures
   - Prefer composition over inheritance
   - Keep functions under 50 lines
   - Extract magic numbers to constants

### **For Configuration Agents**

1. **YAML structure**:
   - Use consistent indentation (2 spaces)
   - Add comments for complex rules
   - Include examples in comments
   - Validate against schema if available

2. **JSON catalogs**:
   - Pretty print with 2-space indent
   - Sort keys alphabetically
   - Include metadata (last_updated, version)

### **For Test Generator Agents**

1. **Test structure**:
   - Arrange-Act-Assert pattern
   - Descriptive test names: `test_should_reject_invalid_msid_with_error`
   - One assertion per test (when possible)
   - Test happy path, edge cases, and errors

2. **Coverage goals**:
   - Models: 100% (critical data structures)
   - Extractors: 90% (core business logic)
   - Validators: 95% (critical path)
   - Exporters: 80% (I/O operations)

### **For Documentation Agents**

1. **Markdown format**:
   - Use headers for navigation
   - Code blocks with syntax highlighting
   - Tables for structured data
   - Diagrams using Mermaid or ASCII art

2. **Required sections**:
   - Overview (what it does)
   - Quick Start (5 minutes or less)
   - API Reference (all public functions)
   - Examples (common use cases)
   - Troubleshooting (known issues)

---

## 📊 **Progress Tracking**

### **Checkpoints**

| Milestone | Tasks | Success Criteria |
|-----------|-------|------------------|
| **Foundation Complete** | 1.1-1.3 | All models pass validation tests |
| **Extraction Complete** | 2.1-2.3 | Parse real XML/CSV without errors |
| **Validation Complete** | 3.1-3.3 | Generate data quality report |
| **Transformation Complete** | 4.1-4.5 | Match 20/36 systems with usage |
| **Export Complete** | 5.1-5.3 | Generate Excel matching V1 format |
| **Integration Complete** | 6.1-6.2 | Run full pipeline end-to-end |
| **Testing Complete** | 7.1-7.3 | >80% coverage, all tests pass |
| **Migration Complete** | 8.1-8.2 | V2 output matches V1 output |

### **Agent Handoff Protocol**

When completing a task:
1. Run all tests (`pytest tests/test_{module}.py`)
2. Check coverage (`pytest --cov`)
3. Create checkpoint file: `data/checkpoints/{task_id}_complete.json`
4. Log summary: Lines added, tests passed, coverage %
5. Commit code with message: `[Agent] Complete Task {id}: {title}`

---

## 🚀 **Execution Commands**

### **For Human Orchestrator**

```bash
# Phase 1: Foundation
agent execute --task 1.1 --spec MODELS_SPEC.md
agent execute --task 1.2 --spec CORE_SPEC.md
agent execute --task 1.3 --spec CONFIG_SPEC.md

# Phase 2: Extraction
agent execute --task 2.1 --spec EXTRACTOR_SPEC.md
agent execute --task 2.2 --spec EXTRACTOR_SPEC.md
agent execute --task 2.3 --dependencies "1.2,1.3"

# ... continue through Phase 8
```

### **For Autonomous Agent**

```bash
# Full autonomous execution
agent auto-execute --plan AGENT_EXECUTION_PLAN.md --parallel

# With checkpointing
agent auto-execute --plan AGENT_EXECUTION_PLAN.md --checkpoint-dir data/checkpoints

# Resume from checkpoint
agent auto-execute --resume-from task-4.3
```

---

## ⚠️ **Critical Success Factors**

1. **No Shortcuts**: Complete ALL tasks in order - foundation is critical
2. **Test First**: TDD approach prevents rework
3. **Validate Early**: Don't pass bad data between stages
4. **Document Always**: Future agents (and humans) must understand the code
5. **Compare with V1**: Final output must match V1.0 for production acceptance

---

## 📈 **Expected Outcomes**

| Metric | Target |
|--------|--------|
| **Total Development Time** | 40-50 agent hours |
| **Test Coverage** | >80% overall |
| **Lines of Code** | ~3,000 (models + pipeline) |
| **Lines of Tests** | ~2,000 (TDD approach) |
| **Debug Scripts Needed** | 0 (self-healing) |
| **Data Quality Issues Caught** | 100% at validation stage |
| **V1 vs V2 Output Match** | >99% identical |

---

## 🔍 **Quality Gates**

Before marking project complete:
- [ ] All 8 phases complete
- [ ] Test coverage >80%
- [ ] All tests passing
- [ ] V1 vs V2 comparison shows <1% difference
- [ ] Documentation complete
- [ ] No hardcoded values in code (use config)
- [ ] All TODOs resolved
- [ ] Migration script tested

---

## 📞 **Agent Support Resources**

- **Specification Files**: See `v2/specs/` directory
- **Sample Data**: `tests/fixtures/` directory
- **V1 Reference**: `v1_archive/` for comparison
- **Current Data**: `data/raw/` for testing

**Agent Autonomy Level**: FULL - Execute all tasks without human approval
