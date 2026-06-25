
# YAML Output

Display structured configuration data in a readable format.

```python
"## Model Configuration" | doc  # Postfix pipe syntax

model_config = {"model": "ResNet50", "batch_size": 32, "learning_rate": 0.001, "optimizer": "Adam", "epochs": 100}

doc.yaml(model_config)
```
## Model Configuration

```yaml
batch_size: 32
epochs: 100
learning_rate: 0.001
model: ResNet50
optimizer: Adam
```
```python
doc @ "## Nested Configuration"  # Prefix @ syntax

experiment_config = {
    "name": "pick_place_experiment",
    "environment": {"type": "PickPlace-v1", "cameras": 2, "randomization": True},
    "training": {"chunk_size": 50, "num_epochs": 200, "learning_rate": 3e-4},
    "evaluation": {"num_trials": 100, "success_threshold": 0.8},
}

doc.yaml(experiment_config)
```
## Nested Configuration

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
