![Econometrics Research Toolkit](assets/header.svg)

# Econometrics Research Toolkit

Reusable OLS specification comparisons, HC3 inference, VIF diagnostics and research reporting, demonstrated on synthetic data.

**Research question:** How can alternative regression specifications be compared transparently while keeping their estimation sample and reporting conventions consistent?

**Public edition:** New public reconstruction using synthetic data; institutional research records and unpublished findings excluded.

**5 functional checks passed locally**, plus a complete demonstration run.

## What you can inspect

- Use a common complete-case sample across all candidate specifications.
- Require base predictors and bound the control-combination search before allocating combinations.
- Estimate OLS with HC3 standard errors and report adjusted R-squared, AIC and BIC.
- Skip rank-deficient specifications with a recorded reason.
- Export coefficient intervals, VIF diagnostics, summaries and fitted-value plots.

## Results preview

All values below are synthetic or illustrative workflow results.

![Econometrics Research Toolkit results preview](demo_output/fit.svg)

| Model | Observations | Adjusted R² | AIC | BIC |
| --- | --- | --- | --- | --- |
| model_012 | 388 | 0.711729 | 1973.22 | 1993.03 |
| model_011 | 388 | 0.711701 | 1973.26 | 1993.07 |
| model_005 | 388 | 0.711669 | 1972.32 | 1988.16 |
| model_013 | 388 | 0.668986 | 2026.87 | 2046.67 |
| model_006 | 388 | 0.66888 | 2026 | 2041.85 |

The synthetic input has 400 rows; 388 remain in the common sample. Fifteen specifications are estimated. The displayed ordering is exploratory and does not certify causal or predictive validity.

## Run the example

Use Python 3.12. From this project's directory:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -v
python toolkit.py --demo --output demo_output
```

For an isolated environment, run `python -m venv .venv` first. Activate it with `source .venv/bin/activate` on Linux/macOS or `.venv\Scripts\activate` on Windows. The standard example runs offline after dependencies are installed.

The [notebook walkthrough](notebooks/01_results_walkthrough.ipynb) explains the saved outputs. Exact command-line options appear in [CLI.txt](docs/CLI.txt).

## Documentation

| Guide | What it covers |
| --- | --- |
| [Methods](docs/METHODS.md) | Formulas, assumptions and interpretation |
| [Data dictionary](docs/DATA_DICTIONARY.md) | Variables, units and validation rules |
| [Results](docs/RESULTS.md) | Actual bundled output and how to read it |
| [Reproducibility](REPRODUCIBILITY.md) | Commands, checks and the recorded environment |
| [Provenance and attribution](docs/PROVENANCE.md) | Historical context, reconstruction and contribution |
| [Roadmap](docs/ROADMAP.md) | Specific extensions, with unfinished work labelled |
| [References](docs/REFERENCES.md) | Method documentation and source links |

## Limits of interpretation

- Specification searches are exploratory and can overfit.
- HC3 does not correct for multiple-model selection or establish causality.
- A common complete-case sample can reduce coverage and is not a general missing-data solution.
- The public workflow revises the mean-imputation approach described in the historical work.

## Contribution and research context

Documented 2023-24 economic-history research workflow at the University of Tübingen under Prof. Jörg Baten.

Arinjai Das supported data preparation, applied econometrics, specification comparisons and reporting in the original research setting. The public reconstruction demonstrates reusable analytical tooling and does not claim sole ownership of the collaborative empirical research.

**Skills demonstrated:** Python, econometrics, OLS, HC3 standard errors, VIF, specification analysis, research automation.

[Portfolio](https://github.com/arinjaidas/My-Projects) · [GitHub profile](https://github.com/arinjaidas)
