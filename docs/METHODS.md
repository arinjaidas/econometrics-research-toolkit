# Methods

## Estimation sample and search

All candidate variables are converted to numeric values. Infinite values become missing, then one common complete-case sample is constructed across the outcome, required predictors and candidate controls. This makes fit comparisons use the same observations. It may discard more observations than a model-specific sample and does not address selection into missingness.

For p candidate controls and a maximum of k controls, the search contains `sum(combinations(p, j), j=0..k)` specifications. This count is checked against the model budget **before** combinations are allocated. The default demonstration compares 15 models: one base predictor plus subsets of four controls of size zero through three.

## Inference and diagnostics

Each full-rank design is estimated by OLS. HC3 uses leverage-adjusted residual contributions, `e_i² / (1-h_ii)²`, in the sandwich covariance. Robust covariance changes reported uncertainty; it does not repair endogeneity, omitted-variable bias or model-selection uncertainty.

Adjusted R-squared, AIC and BIC describe the estimated models. The output order prioritises adjusted R-squared and then BIC. VIF describes linear dependence among regressors. It is a diagnostic, not an automatic rule for deleting substantively necessary variables. Rank-deficient designs are skipped with an explicit reason.
