# YAML

Render configuration dictionaries as YAML blocks.

`doc.yaml(data)` takes a Python dict and writes it as a fenced `yaml` block. It needs the `yaml` extra (pyyaml):

```bash
pip install 'cmx[yaml]'
```

## Basic YAML

Pass a dictionary to `doc.yaml`:

```python
from cmx import doc

doc.config(__file__)

with doc:
    config = {
        "model": "ResNet50",
        "batch_size": 32,
        "learning_rate": 0.001,
        "optimizer": "Adam",
        "epochs": 100,
    }

    doc.yaml(config)

doc.flush()
```

This produces:

````markdown
```yaml
batch_size: 32
epochs: 100
learning_rate: 0.001
model: ResNet50
optimizer: Adam
```
````

:::{note}
Keys are sorted alphabetically (the pyyaml default), so the output order does not follow your dict's insertion order. A blank line is inserted before the block automatically.
:::

## Nested config

Nested dictionaries render as indented YAML:

```python
with doc:
    experiment = {
        "name": "pick_place_experiment",
        "environment": {"type": "PickPlace-v1", "cameras": 2, "randomization": True},
        "training": {"chunk_size": 50, "num_epochs": 200, "learning_rate": 3e-4},
        "evaluation": {"num_trials": 100, "success_threshold": 0.8},
    }

    doc.yaml(experiment)
```

This produces:

````markdown
```yaml
environment:
  cameras: 2
  randomization: true
  type: PickPlace-v1
evaluation:
  num_trials: 100
  success_threshold: 0.8
name: pick_place_experiment
training:
  chunk_size: 50
  learning_rate: 0.0003
  num_epochs: 200
```
````

Keys are sorted at every level, and Python values map to their YAML equivalents: `True` becomes `true`, and `3e-4` becomes `0.0003`.

## Use cases

Reach for `doc.yaml` when you want to record structured settings in a readable form:

- Experiment configurations and run metadata
- Model hyperparameters
- Environment and dataset settings
- Any nested dictionary you would otherwise dump as JSON

YAML keeps nested structures legible without the quoting and bracket noise of JSON, which makes it a good fit for documenting experiments.

## Next steps

- [Tables](tables.md) — render DataFrames and CSV data as Markdown tables
- [Printing](printing.md) — add dynamic, computed output with `doc.print()`
