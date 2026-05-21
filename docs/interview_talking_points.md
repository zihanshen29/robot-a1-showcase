# Interview Talking Points

## 30-Second Version

This is a sanitized Unitree A1 showcase repository. I made it to demonstrate how I structure robotics simulation-control work without publishing non-public code or raw logs. It includes deterministic demo data, a validated parser, metrics, plots, tests, and documentation. The numbers and figures are synthetic, so the value is the engineering pipeline and communication, not a claim of real robot performance.

## 2-Minute Version

The repository presents a clean version of a Unitree A1 simulation-control analysis workflow. The code generates 600-step synthetic runs with base motion, velocity tracking, simplified contact indicators, MPC accept/reject states, predicted support-force values, and cost trends. The parser validates the schema, the metrics module calculates interpretable summaries, and the plotting module creates figures that can be used in an interview walkthrough.

I deliberately separated what is shown from what is not shown. This is not the original codebase and it does not include real logs, checkpoints, Isaac integration, ROS messages, or Unitree SDK calls. It is a public-safe artifact that demonstrates how I break down a robotics project into data contracts, diagnostics, reproducible scripts, figures, and tests.

## Technical Q&A

**Why not open the original project directly?**

Because robotics projects often include non-public code, raw logs, environment-specific paths, and collaborator context. A sanitized showcase is a better way to communicate engineering work while respecting confidentiality.

**How do you keep the showcase credible without leaking source details?**

The repository makes its boundary explicit. It provides runnable code, tests, and synthetic data with clear labels. It avoids raw logs and unsupported claims, while still showing parser design, metrics, diagnostics, and plotting quality.

**Why choose 600-step figures?**

Six hundred steps are long enough to show short-horizon tracking, base-height variation, roll/pitch behavior, MPC accept/reject patterns, predicted support-force changes, and cost trends. They are also compact enough for a reviewer to inspect quickly.

**What do MPC accept/reject, predicted support force, and cost trend explain?**

Accept/reject states show whether a candidate controller output would be considered usable by a feasibility gate. Predicted support force gives a leg-level diagnostic for contact phases. Cost trend gives a compact signal for whether the simplified optimization-style objective is improving, flat, or deteriorating in the demo sequence.

**How would this extend to real Unitree A1 or simulator logs?**

I would add an adapter that converts public-approved logs into the same CSV schema, then run the existing validation, metrics, and plots. The adapter would be reviewed separately to avoid publishing raw internal formats or environment details.

**What capabilities does this project demonstrate?**

It demonstrates robotics data-contract design, reproducible analysis, diagnostic plotting, metric selection, boundary-setting, Python packaging, testing, and interview communication.

