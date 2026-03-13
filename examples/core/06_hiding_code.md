
# Hiding Code Blocks

Sometimes you need to run setup code without showing it in the output.
## Data Statistics (hidden setup)

## Results

The analysis results are shown below, but the setup code is hidden.
```python
doc @ f"### Summary Statistics"
doc.print(f"Mean: {mean:.4f}")
doc.print(f"Std:  {std:.4f}")
```
### Summary Statistics
```
Mean: -0.0317
Std:  0.9817
```

## Use Cases for `doc.hide`

1. **Data loading**: Don't show file I/O code
2. **Environment setup**: Hide initialization details
3. **Expensive computations**: Show results but not the computation
4. **Helper functions**: Define utilities without cluttering docs
```python
doc @ "## Using Hidden Results"
doc.print("We can still use results from hidden code blocks!")
```
## Using Hidden Results
```
We can still use results from hidden code blocks!
```
