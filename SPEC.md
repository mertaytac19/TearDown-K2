# SPEC.md

## Acceptance Criteria (Gherkin)

```gherkin
Feature: K2 t-test (matched pairs) power analysis
  As a researcher, I want to compute sample size (N) a priori and power post hoc using GPower.

  Scenario Outline: A priori sample size calculation
    Given the inputs tails, dz, alpha, and desired power
    When the analysis runs in A priori mode
    Then the output should include n_total, actual_power, critical, df, ncp
    And n_total is calculated as the ceiling of the required sample size
    And df equals n_total - 1
    And ncp equals dz * sqrt(n_total)
    And critical value corresponds to the t-distribution threshold

  Scenario Outline: Post hoc power calculation
    Given the inputs tails, dz, alpha, and actual sample size n_total
    When the analysis runs in Post hoc mode
    Then the output should include n_total, actual_power, critical, df, ncp
    And actual_power is computed based on the provided n_total

  # Boundary scenario: small effect size or insufficient power
  Scenario: Boundary values
    Given dz is very small and desired power <= alpha
    When the analysis runs
    Then the tool should warn that the required N may be infinite or undefined
    And suggest increasing effect size or relaxing alpha
```
