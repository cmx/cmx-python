"""
YAML Output Example

This example shows how to display configuration and structured data
as YAML, a common pattern for documenting experiments.
"""

from cmx import doc

doc.config(__file__)

doc @ """
# YAML Output

Display structured configuration data in a readable format.
"""

with doc:
    "## Model Configuration" | doc  # Postfix pipe syntax

    model_config = {"model": "ResNet50", "batch_size": 32, "learning_rate": 0.001, "optimizer": "Adam", "epochs": 100}

    doc.yaml(model_config)

with doc:
    doc @ "## Nested Configuration"  # Prefix @ syntax

    experiment_config = {
        "name": "pick_place_experiment",
        "environment": {"type": "PickPlace-v1", "cameras": 2, "randomization": True},
        "training": {"chunk_size": 50, "num_epochs": 200, "learning_rate": 3e-4},
        "evaluation": {"num_trials": 100, "success_threshold": 0.8},
    }

    doc.yaml(experiment_config)

doc.flush()

print("\n✓ YAML output example complete! Check 05_yaml_output.md next to the script.")
