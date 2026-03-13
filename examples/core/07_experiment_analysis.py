"""
Experiment Analysis Example

This demonstrates a real-world pattern from vuer-ai repositories:
analyzing and reporting experiment metrics.
"""

from cmx import doc
import pandas as pd
import numpy as np

doc.config(filename="examples/core/07_experiment_analysis.md")

doc @ """
# Experiment Analysis Report

This is a typical experiment analysis workflow.
"""

# Simulate loading experiment data
with doc.hide:
    # In real usage, you'd load this from files or a logging system
    experiments = [
        {"checkpoint": "baseline", "success_rate": 0.45, "num_trials": 100},
        {"checkpoint": "v1-optimized", "success_rate": 0.68, "num_trials": 100},
        {"checkpoint": "v2-final", "success_rate": 0.89, "num_trials": 100},
    ]

doc @ """
## Performance Comparison

Comparing different model checkpoints:
"""

with doc.hide:
    # Prepare the table header
    doc @ """
| Checkpoint | Success Rate | Num Trials |
| ---------- | ------------ | ---------- |"""

    # Add rows for each experiment
    for exp in experiments:
        ckpt = exp["checkpoint"]
        success = exp["success_rate"]
        trials = exp["num_trials"]
        doc @ f"| {ckpt} | {success:.1%} | {trials} |"

doc @ """
## Analysis

The results show significant improvement over the baseline:
"""

with doc:
    baseline = experiments[0]["success_rate"]
    final = experiments[2]["success_rate"]
    improvement = (final - baseline) / baseline

    doc.print(f"Baseline success rate: {baseline:.1%}")
    doc.print(f"Final success rate: {final:.1%}")
    doc.print(f"Relative improvement: {improvement:.1%}")

doc @ """
## Detailed Metrics

Here's a more detailed breakdown using pandas:
"""

with doc:
    df = pd.DataFrame(experiments)
    df["Success Rate"] = df["success_rate"].apply(lambda x: f"{x:.1%}")
    df = df[["checkpoint", "Success Rate", "num_trials"]]
    df.columns = ["Checkpoint", "Success Rate", "Num Trials"]

    doc.table(df, show_index=False)

doc.flush()

print("\n✓ Experiment analysis example complete! Check examples/core/07_experiment_analysis.md")
