"""
Comprehensive Example

This example combines multiple CMX features in a realistic workflow.
"""

from cmx import doc
import pandas as pd
import numpy as np
import os

os.makedirs("examples/core/figures", exist_ok=True)

doc.config(filename="examples/core/08_comprehensive.md")

doc @ """
# Machine Learning Experiment Report

**Date**: 2024-01-15
**Experiment**: Image Classification Baseline

## Overview

This report documents the baseline experiment for image classification
using different neural network architectures.
"""

# Setup (hidden)
with doc.hide:
    np.random.seed(42)

    # Simulate training results
    models = ["ResNet50", "VGG16", "MobileNetV2", "EfficientNet-B0"]
    accuracies = [0.945, 0.872, 0.918, 0.956]
    training_times = [145, 203, 98, 167]  # minutes
    params = ["25.6M", "138M", "3.5M", "5.3M"]

doc @ """
## Experiment Configuration
"""

with doc:
    config = {
        "dataset": "ImageNet-1k",
        "batch_size": 64,
        "learning_rate": 0.001,
        "optimizer": "Adam",
        "epochs": 100,
        "augmentation": True,
    }

    doc.yaml(config)

doc @ """
## Results

### Model Comparison
"""

with doc:
    results = pd.DataFrame(
        {
            "Model": models,
            "Accuracy": [f"{a:.1%}" for a in accuracies],
            "Training Time (min)": training_times,
            "Parameters": params,
        }
    )

    doc.table(results, show_index=False)

doc @ """
### Performance Analysis
"""

with doc:
    best_model = models[np.argmax(accuracies)]
    best_acc = max(accuracies)
    fastest_model = models[np.argmin(training_times)]

    doc.print(f"Best performing model: {best_model} ({best_acc:.1%})")
    doc.print(f"Fastest training: {fastest_model} ({min(training_times)} min)")

doc @ """
### Visualization

Training curves for the best model:
"""

with doc:
    # Generate sample training curve
    epochs = np.arange(1, 101)
    train_acc = 1 - np.exp(-epochs / 30) * 0.7 + np.random.randn(100) * 0.01
    train_acc = np.clip(train_acc, 0, 1)

    # Create a simple visualization (would use matplotlib in real scenario)
    vis_data = np.zeros((100, 200, 3), dtype=np.uint8)
    for i, acc in enumerate(train_acc):
        y = int((1 - acc) * 99)
        x = int(i * 2)
        if x < 200:
            vis_data[max(0, y - 1) : min(100, y + 2), x : x + 2] = [0, 150, 255]

    doc.image(vis_data, src="examples/core/figures/training_curve.png")

doc @ """
## Conclusions

1. EfficientNet-B0 achieved the best accuracy with reasonable parameters
2. MobileNetV2 offers the best speed/accuracy tradeoff
3. VGG16 is outdated for this task (high params, low accuracy)

## Next Steps

- [ ] Fine-tune EfficientNet-B0 with larger batch size
- [ ] Test MobileNetV2 for deployment
- [ ] Implement knowledge distillation
"""

doc.flush()

print("\n✓ Comprehensive example complete! Check examples/core/08_comprehensive.md")
