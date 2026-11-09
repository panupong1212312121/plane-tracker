---
name: data-designer
description: Generate high-fidelity synthetic datasets and enterprise corpora using NVIDIA NeMo DataDesigner. Produces multi-column tabular data with complex statistical distributions, intra-column correlations, deterministic schemas, and custom validator rules. Complements /mock-data when realistic domain distributions, cross-attribute constraints, edge-case traps, or bilingual (Thai/English) enterprise business records are needed for benchmarking or model training. Use when generating complex corpus datasets, multi-field correlated tables, or benchmark distributions.
metadata:
  version: "1.0"
  author: local
---

# DataDesigner (Synthetic Datasets & Enterprise Corpora)

NVIDIA NeMo DataDesigner is an advanced synthetic data generation engine designed for high-fidelity data generation with complex statistical distributions, multi-attribute correlations, and domain constraints. While `/mock-data` handles straightforward deterministic fixtures and basic test seeds, `/data-designer` handles multi-variate statistical distributions, realistic edge-case distributions, and bilingual enterprise corpora (such as Thai tax IDs, mixed Thai-English inventory records, and financial transaction series).

## Boundary: DataDesigner vs Mock-Data

| Dimension | `/mock-data` | `/data-designer` |
| --- | --- | --- |
| **Complexity** | 1–5 simple columns, independent values | Highly correlated multi-attribute distributions |
| **Generation Engine** | Deterministic faker/generators | Statistical sampler + constraint solvers + LLM synthesizers |
| **Target Use Case** | Unit test fixtures, quick component mocks | Benchmark corpora, model fine-tuning sets, stress datasets |
| **Telemetry** | None | Must set `NEMO_TELEMETRY_ENABLED=false` |

## Core Workflow

### 1. Schema & Distribution Specification

Define the target schema with statistical attributes, distributions (Gaussian, Zipfian, categorical distributions), and value ranges in a configuration file (e.g. `corpus_config.yaml`):

```yaml
fields:
  customer_id:
    type: string
    pattern: "CUST-[0-9]{6}"
  company_name_th:
    type: string
    distribution: "thai_enterprise_names"
  tax_id:
    type: string
    pattern: "[0-9]{13}"
    validator: "thai_tax_checksum"
  annual_revenue_thb:
    type: float
    distribution: "log_normal"
    params: { mean: 15.2, sigma: 1.1 }
  risk_tier:
    type: categorical
    correlate_with: "annual_revenue_thb"
    distribution:
      low: 0.6
      medium: 0.3
      high: 0.1
```

### 2. Constraint & Validator Definition

Implement custom Python validation checks to enforce domain invariants (e.g., Thai Tax ID mod-11 checksums, valid VAT registered status, or start/end timestamp ordering):

```python
def validate_record(record: dict) -> bool:
    if record["annual_revenue_thb"] > 100_000_000 and record["risk_tier"] == "high":
        return False
    return True
```

### 3. Execution & Seeded Sampling

Run generation with mandatory telemetry suppression and fixed random seed for reproducibility:

```bash
# Disable outbound telemetry
export NEMO_TELEMETRY_ENABLED=false

# Run generation via CLI or python script
uv run datadesigner generate \
  --config .scratch/data-designer/corpus_config.yaml \
  --rows 500 \
  --seed 42 \
  --output .scratch/data-designer/enterprise_corpus.parquet
```

### 4. Quality Audit & PII Verification

- Verify that output records satisfy all schema constraints.
- Inspect correlation matrices to confirm relationships match intended statistical profiles.
- Run automated PII scanners to ensure zero real names, actual phone numbers, or genuine national identification numbers are produced.

## Thai/English Enterprise Corpus Patterns

When designing Thai business corpora:
- **Mixed Scripts:** Realistic datasets include Thai strings with English brand names, transliterations, and abbreviations.
- **Trap Values:** Include intentional noisy rows (e.g. zero-padded numbers stripped of leading zeros, trailing whitespace, varied date formats such as Buddhist Era vs Christian Era years `2567` vs `2024`).

## Guardrails

- **Telemetry Guard:** Always verify `NEMO_TELEMETRY_ENABLED=false` before executing any DataDesigner command.
- **Quota Awareness:** When using LLM-assisted distribution modes, obtain explicit user confirmation before consuming external API quotas.
- **Zero Real Data Exfiltration:** Never seed DataDesigner with actual production user data or unmasked PII.

