
# Experiment Analysis Report

This is a typical experiment analysis workflow.

## Performance Comparison

Comparing different model checkpoints:

| Checkpoint | Success Rate | Num Trials |
| ---------- | ------------ | ---------- |
| baseline | 45.0% | 100 |
| v1-optimized | 68.0% | 100 |
| v2-final | 89.0% | 100 |

## Analysis

The results show significant improvement over the baseline:

```python
baseline = experiments[0]["success_rate"]
final = experiments[2]["success_rate"]
improvement = (final - baseline) / baseline

doc.print(f"Baseline success rate: {baseline:.1%}")
doc.print(f"Final success rate: {final:.1%}")
doc.print(f"Relative improvement: {improvement:.1%}")
```

```
Baseline success rate: 45.0%
Final success rate: 89.0%
Relative improvement: 97.8%
```

## Detailed Metrics

Here's a more detailed breakdown using pandas:

```python
df = pd.DataFrame(experiments)
df["Success Rate"] = df["success_rate"].apply(lambda x: f"{x:.1%}")
df = df[["checkpoint", "Success Rate", "num_trials"]]
df.columns = ["Checkpoint", "Success Rate", "Num Trials"]

doc.table(df, show_index=False)
```

| Checkpoint   | Success Rate   |   Num Trials |
|--------------|----------------|--------------|
| baseline     | 45.0%          |          100 |
| v1-optimized | 68.0%          |          100 |
| v2-final     | 89.0%          |          100 |
