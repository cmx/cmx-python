# YAML Output

**Questions**
- How do I display configuration dictionaries?
- How do I show nested settings?
- When should I use YAML instead of JSON?

**Objectives**
- Display dictionaries as YAML
- Show experiment configurations
- Understand YAML formatting

## Basic YAML Output

Display a configuration dictionary:

```python
from cmx import doc

doc.config(filename="output.md")

with doc:
    doc @ "## Model Configuration"

    config = {
        'model': 'ResNet50',
        'batch_size': 32,
        'learning_rate': 0.001,
        'optimizer': 'Adam'
    }

    doc.yaml(config)

doc.flush()
```

Output in markdown:
```yaml
model: ResNet50
batch_size: 32
learning_rate: 0.001
optimizer: Adam
```

## Nested Configuration

YAML handles nested dictionaries well:

```python
with doc:
    doc @ "## Experiment Config"

    config = {
        'name': 'pick_place_experiment',
        'environment': {
            'type': 'PickPlace-v1',
            'cameras': 2,
            'randomization': True
        },
        'training': {
            'epochs': 100,
            'learning_rate': 0.0003
        }
    }

    doc.yaml(config)
```

## Use Cases

Use YAML for:
- Experiment configurations
- Model hyperparameters
- Environment settings
- Any nested dictionary structure

YAML is more readable than JSON for configuration files.

## Key Points

- Use `doc.yaml(dict)` to display dictionaries
- YAML handles nested structures well
- More readable than JSON for configs
- Common pattern for experiment documentation

## Next Steps

- [Tables](tables.md) - Display data
- [Context Managers](context.md) - Control output
