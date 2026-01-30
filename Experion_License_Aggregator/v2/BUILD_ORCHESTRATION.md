# V2.0 Build Orchestration - Agent Instructions

**Purpose**: Guide for autonomous agent to build complete V2.0 system  
**Execution Mode**: Full autonomy - no human input required  
**Validation**: Output must match V1.0 within 1% tolerance

---

## 🎯 Agent Mission

Build production-ready Experion License Aggregator V2.0 that:
1. Processes all XML/CSV files with validation
2. Generates identical output to V1.0 (within tolerance)
3. Provides data quality dashboard
4. Requires zero manual debug scripts
5. Achieves >80% test coverage

---

## 📋 Complete Task List (38 Tasks)

### **PHASE 1: FOUNDATION** (Priority: CRITICAL)

#### ✅ Task 1.1: Data Models
- **File**: `models/license.py`
- **Time**: 2 hours
- **Tests**: 100% coverage
- **Validation**: 
  ```python
  lic = LicenseData(msid='M0614', system_number='60806', ...)
  assert lic.unique_key == ('Carson', 'M0614', '60806')
  
  # Must reject invalid
  with pytest.raises(ValidationError):
      LicenseData(msid='', ...)
  ```

#### ✅ Task 1.2: Core Infrastructure
- **Files**: `core/exceptions.py`, `core/config.py`, `core/constants.py`
- **Time**: 1 hour
- **Tests**: 90% coverage

#### ✅ Task 1.3: Configuration Files
- **Files**: All YAML configs in `config/`
- **Time**: 30 minutes
- **Validation**: Load and parse without errors

---

### **PHASE 2: EXTRACTION** (Priority: HIGH)

#### ✅ Task 2.1: XML Extractor
- **File**: `pipeline/extractors/xml_extractor.py`
- **Time**: 3 hours
- **Tests**: 95% coverage
- **Validation**:
  ```python
  result = extractor.extract_from_file('test.xml')
  assert result.success == True
  assert result.data.msid == 'M0614'
  assert result.data.licensed['PROCESSPOINTS'] == 4750
  ```

#### ✅ Task 2.2: CSV Extractor
- **File**: `pipeline/extractors/csv_extractor.py`
- **Time**: 2 hours
- **Tests**: 95% coverage

#### ✅ Task 2.3: Config Loader
- **File**: `pipeline/extractors/config_loader.py`
- **Time**: 1 hour
- **Tests**: 90% coverage

---

### **PHASE 3: VALIDATION** (Priority: HIGH)

#### ✅ Task 3.1: Schema Validator
- **File**: `pipeline/validators/schema_validator.py`
- **Time**: 2 hours
- **Tests**: 95% coverage

#### ✅ Task 3.2: Business Validator
- **File**: `pipeline/validators/business_validator.py`
- **Time**: 2 hours
- **Tests**: 95% coverage

#### ✅ Task 3.3: Match Validator
- **File**: `pipeline/validators/match_validator.py`
- **Time**: 2 hours
- **Tests**: 90% coverage
- **Validation**:
  ```python
  result = validator.find_match(license, csv_list)
  assert result.confidence >= 0.8
  assert result.method in ['exact', 'fuzzy_msid']
  ```

---

### **PHASE 4: TRANSFORMATION** (Priority: HIGH)

#### ✅ Task 4.1: Deduplicator
- **File**: `pipeline/transformers/deduplicator.py`
- **Time**: 2 hours
- **Tests**: 90% coverage

#### ✅ Task 4.2: Field Mapper
- **File**: `pipeline/transformers/field_mapper.py`
- **Time**: 2 hours
- **Tests**: 95% coverage

#### ✅ Task 4.3: Usage Matcher
- **File**: `pipeline/transformers/usage_matcher.py`
- **Time**: 3 hours
- **Tests**: 90% coverage
- **Validation**: Must match 20/36 systems like V1.0

#### ✅ Task 4.4: Cost Calculator
- **File**: `pipeline/transformers/cost_calculator.py`
- **Time**: 2 hours
- **Tests**: 90% coverage

#### ✅ Task 4.5: Transfer Detector
- **File**: `pipeline/transformers/transfer_detector.py`
- **Time**: 2 hours
- **Tests**: 85% coverage

---

### **PHASE 5: EXPORT** (Priority: MEDIUM)

#### ✅ Task 5.1: JSON Exporter
- **File**: `pipeline/exporters/json_exporter.py`
- **Time**: 1 hour
- **Tests**: 80% coverage

#### ✅ Task 5.2: Excel Exporter
- **File**: `pipeline/exporters/excel_exporter.py`
- **Time**: 4 hours
- **Tests**: 80% coverage
- **Validation**: PKS sheet format matches V1.0 exactly

#### ✅ Task 5.3: Validation Report Generator
- **File**: `pipeline/exporters/report_generator.py`
- **Time**: 2 hours
- **Tests**: 80% coverage

---

### **PHASE 6: ORCHESTRATION** (Priority: MEDIUM)

#### ✅ Task 6.1: Pipeline Orchestrator
- **File**: `core/orchestrator.py`
- **Time**: 3 hours
- **Tests**: 85% coverage
- **Validation**:
  ```python
  orchestrator = PipelineOrchestrator(config)
  result = orchestrator.run()
  assert result.success == True
  assert Path('data/validated/licenses.json').exists()
  ```

#### ✅ Task 6.2: CLI Entry Point
- **File**: `main.py`
- **Time**: 1 hour
- **Tests**: 70% coverage

---

### **PHASE 7: TESTING** (Priority: HIGH)

#### ✅ Task 7.1: Unit Tests
- **Files**: All test files in `tests/`
- **Time**: 4 hours
- **Validation**: `pytest --cov` shows >80%

#### ✅ Task 7.2: Integration Tests
- **File**: `tests/test_integration.py`
- **Time**: 2 hours
- **Validation**: Full pipeline runs successfully

#### ✅ Task 7.3: Documentation
- **Files**: `docs/*.md`
- **Time**: 3 hours
- **Validation**: All public APIs documented

---

### **PHASE 8: VALIDATION** (Priority: CRITICAL)

#### ✅ Task 8.1: V1 vs V2 Comparison
- **File**: `tests/test_v1_v2_comparison.py`
- **Time**: 2 hours
- **Validation**:
  ```python
  v1_systems = 36
  v2_systems = 36
  assert v1_systems == v2_systems
  
  v1_cost = 17_300_875
  v2_cost = result.total_cost
  assert abs(v1_cost - v2_cost) / v1_cost < 0.01  # <1% diff
  ```

#### ✅ Task 8.2: Migration Script
- **File**: `migrate_to_v2.py`
- **Time**: 1 hour
- **Validation**: Successful migration with report

---

## 🤖 Agent Execution Commands

### **Sequential Execution** (Recommended)

```bash
# Phase 1
agent execute --spec v2/MODELS_SPEC.md --task 1.1
agent execute --spec v2/CORE_SPEC.md --task 1.2
agent execute --spec v2/CONFIG_SPEC.md --task 1.3

# Phase 2
agent execute --spec v2/EXTRACTOR_SPEC.md --task 2.1
agent execute --spec v2/EXTRACTOR_SPEC.md --task 2.2
agent execute --task 2.3 --deps "1.2,1.3"

# Phase 3
agent execute --spec v2/VALIDATOR_SPEC.md --task 3.1
agent execute --spec v2/VALIDATOR_SPEC.md --task 3.2
agent execute --spec v2/VALIDATOR_SPEC.md --task 3.3

# Phase 4
agent execute --spec v2/TRANSFORMER_SPEC.md --tasks 4.1,4.2,4.3,4.4,4.5

# Phase 5
agent execute --spec v2/EXPORTER_SPEC.md --tasks 5.1,5.2,5.3

# Phase 6
agent execute --spec v2/ORCHESTRATOR_SPEC.md --tasks 6.1,6.2

# Phase 7
agent execute --spec v2/TESTING_SPEC.md --tasks 7.1,7.2,7.3

# Phase 8
agent execute --tasks 8.1,8.2 --validate-migration
```

### **Parallel Execution** (Advanced)

```bash
# Run independent tasks in parallel
agent execute --parallel --plan v2/AGENT_EXECUTION_PLAN.md
```

---

## 📊 Progress Tracking

### **Checkpoint Files**

After each task, agent creates:
```json
// data/checkpoints/task_1_1_complete.json
{
  "task_id": "1.1",
  "task_name": "Data Models",
  "status": "complete",
  "timestamp": "2026-01-28T15:30:00Z",
  "duration_minutes": 120,
  "files_created": ["models/license.py", "models/usage.py", ...],
  "tests_passed": 45,
  "coverage_percent": 100.0,
  "validation_results": {
    "license_creation": "passed",
    "validation_rejection": "passed",
    "serialization_roundtrip": "passed"
  }
}
```

### **Phase Completion Gates**

| Phase | Complete When | Validation |
|-------|--------------|------------|
| 1 | All models pass tests | 100% coverage |
| 2 | Parse real XML/CSV | No errors on 36 systems |
| 3 | Generate quality report | 20+ systems validated |
| 4 | Match usage data | 20/36 matched |
| 5 | Excel output created | Matches V1 format |
| 6 | End-to-end pipeline runs | All checkpoints created |
| 7 | Test coverage >80% | All tests pass |
| 8 | V2 output ≈ V1 output | <1% cost difference |

---

## 🔍 Quality Gates

### **Before Moving to Next Phase**

```python
def validate_phase_complete(phase_num: int) -> bool:
    """Check if phase met all requirements"""
    
    if phase_num == 1:  # Foundation
        assert all_models_exist()
        assert all_tests_pass()
        assert coverage >= 100.0  # Models require 100%
    
    elif phase_num == 2:  # Extraction
        assert can_parse_all_xml_files()
        assert can_parse_all_csv_files()
        assert extractors_return_typed_models()
    
    elif phase_num == 3:  # Validation
        assert validation_report_generated()
        assert validation_catches_known_issues()
    
    elif phase_num == 4:  # Transformation
        assert deduplication_reduces_count()
        assert matching_finds_20_systems()
        assert costs_calculated_for_all()
    
    elif phase_num == 5:  # Export
        assert excel_file_created()
        assert excel_has_all_sheets()
        assert pks_sheet_format_correct()
    
    elif phase_num == 6:  # Orchestration
        assert full_pipeline_runs()
        assert all_checkpoints_created()
    
    elif phase_num == 7:  # Testing
        assert overall_coverage >= 80.0
        assert integration_tests_pass()
    
    elif phase_num == 8:  # Validation
        assert v1_v2_outputs_match()
        assert migration_script_works()
    
    return True
```

---

## ⚠️ Critical Success Factors

### **1. Test-Driven Development**

**ALWAYS write tests before implementation:**

```python
# tests/test_license.py
def test_license_rejects_empty_msid():
    """Test BEFORE implementing validation"""
    with pytest.raises(ValidationError):
        LicenseData(msid='', system_number='60806', ...)

# NOW implement in models/license.py
def __post_init__(self):
    if not self.msid:
        raise ValidationError("MSID required")
```

### **2. Type Hints Everywhere**

```python
# ✅ GOOD
def match_usage(license: LicenseData, 
                usage_list: List[UsageData]) -> MatchResult:
    ...

# ❌ BAD
def match_usage(license, usage_list):
    ...
```

### **3. Validation at Boundaries**

```python
# ✅ GOOD - Validate at construction
@dataclass
class LicenseData:
    msid: str
    
    def __post_init__(self):
        if not self.msid:
            raise ValidationError("Invalid MSID")

# ❌ BAD - Validate later
license = {'msid': ''}  # No validation
...
if not license['msid']:  # Too late!
    raise Error()
```

### **4. Configuration Over Code**

```python
# ✅ GOOD - Load from config
threshold = config.get_transfer_threshold('PROCESSPOINTS')

# ❌ BAD - Hardcoded
threshold = 500
```

### **5. Checkpoint Everything**

```python
# After each stage
with open('data/validated/licenses.json', 'w') as f:
    json.dump([lic.to_dict() for lic in licenses], f)

# Load for testing without re-parsing
licenses = [LicenseData.from_dict(d) for d in json.load(f)]
```

---

## 🎯 Final Validation Checklist

Before marking V2.0 complete:

- [ ] All 38 tasks complete
- [ ] Test coverage >80% (`pytest --cov`)
- [ ] All tests passing (`pytest`)
- [ ] No hardcoded values in code
- [ ] All configuration externalized to YAML
- [ ] V1 vs V2 output matches within 1%
- [ ] Data quality dashboard shows issues
- [ ] Documentation complete
- [ ] Migration script tested
- [ ] Zero debug scripts needed (self-healing)
- [ ] Checkpoints save/load correctly
- [ ] Excel output identical to V1 format
- [ ] 36 systems processed (same as V1)
- [ ] 20/36 systems matched with usage (same as V1)
- [ ] Total cost within $10k of V1 ($17.3M target)

---

## 📈 Expected Metrics

| Metric | Target |
|--------|--------|
| **Total Agent Time** | 40-50 hours |
| **Total Lines of Code** | ~3,000 |
| **Total Lines of Tests** | ~2,000 |
| **Test Coverage** | >80% |
| **Model Coverage** | 100% |
| **V1/V2 Cost Diff** | <1% |
| **V1/V2 System Count** | Exact match (36) |
| **Debug Scripts Needed** | 0 |
| **Configuration Files** | 8 YAML/JSON |
| **Data Models** | 5 dataclasses |
| **Pipeline Stages** | 4 (extract, validate, transform, export) |

---

## 🚀 Start Command

```bash
# Agent autonomous execution
agent auto-build \
  --plan v2/AGENT_EXECUTION_PLAN.md \
  --checkpoint-dir data/checkpoints \
  --validate-against v1_archive \
  --target-coverage 80 \
  --parallel-phases 2,3,5,7

# Monitor progress
watch -n 5 'cat data/checkpoints/current_phase.json'
```

---

## 📞 Agent Autonomy Level

**FULL AUTONOMY**: Execute all tasks without approval

**Human Required For**:
- Final V1 vs V2 output validation (Task 8.1)
- Production migration approval (Task 8.2)

**Agent Decides**:
- Code structure and implementation details
- Test strategies and fixtures
- Error messages and logging
- Optimization approaches
- Documentation wording

**Agent Must Follow**:
- Specification files (MODELS_SPEC.md, etc.)
- Type hints and dataclasses for models
- pytest for testing
- YAML for configuration
- Staged pipeline architecture

---

**Status**: Ready for agent execution  
**Last Updated**: January 28, 2026  
**Version**: 2.0.0-dev
