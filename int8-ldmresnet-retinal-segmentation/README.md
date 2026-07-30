# INT8-Quantized LDMRes-Net for Lightweight Retinal Vessel Segmentation

This repository contains the implementation, experiments, and preprint materials for **INT8-Quantized LDMRes-Net for Efficient Lightweight Medical Image Segmentation on Edge Devices**.

The project investigates whether an already lightweight retinal vessel segmentation architecture, **LDMRes-Net**, can be further optimized using **INT8 quantization** while preserving segmentation quality. We compare a full-precision **FP32 baseline** against two INT8 compression strategies:

- **Post-Training Quantization (PTQ)**
- **Quantization-Aware Training (QAT)**

The experiments are performed on the **DRIVE retinal vessel segmentation dataset** using a PyTorch implementation of an LDMRes-Net-style encoder-decoder network.

---

## Research Motivation

Retinal vessel segmentation is important for ophthalmic and vascular disease screening, but many deep learning segmentation models are too computationally expensive for low-resource clinical environments or edge devices.

This work explores the following research question:

> Can INT8 quantization improve the deployment efficiency of a lightweight retinal vessel segmentation model without severely reducing clinically relevant segmentation performance?

The main focus is the trade-off between:

- segmentation quality,
- model size,
- inference latency,
- and sensitivity to fine vessel structures.

---

## Key Contributions

- Reproduced an LDMRes-Net-style lightweight retinal vessel segmentation pipeline in PyTorch.
- Implemented FP32, INT8-PTQ, and INT8-QAT model variants.
- Evaluated the accuracy-efficiency trade-off using F1 score, sensitivity, specificity, accuracy, inference latency, and model size.
- Demonstrated that QAT provides a better balance than PTQ for preserving vessel sensitivity after INT8 compression.

---

## Dataset

This project uses the **DRIVE dataset** for retinal vessel segmentation.

The dataset contains:

- 40 colour fundus images,
- manually annotated vessel masks,
- field-of-view masks,
- 20 training images,
- 20 test images.

Due to dataset licensing restrictions, the dataset is **not included** in this repository. Download DRIVE from the official source and place it in the following structure:

```text
data/
└── DRIVE/
    ├── training/
    │   ├── images/
    │   ├── 1st_manual/
    │   └── mask/
    └── test/
        ├── images/
        ├── 1st_manual/
        └── mask/
```

Update the dataset path in the notebook or configuration file before running the experiments.

---

## Methodology Overview

The experimental workflow is:

1. Load and preprocess DRIVE retinal fundus images.
2. Resize images and masks to `640 × 640`.
3. Apply z-score normalization to input images.
4. Train the FP32 LDMRes-Net baseline.
5. Evaluate the FP32 baseline using segmentation metrics.
6. Apply INT8 post-training quantization.
7. Apply INT8 quantization-aware training.
8. Compare FP32, PTQ, and QAT models using quality and efficiency metrics.

---

## Model Architecture

The implemented architecture follows the LDMRes-Net design philosophy:

- compact encoder-decoder structure,
- dual multi-scale residual blocks,
- parallel convolutional paths,
- residual connections for stable training,
- lightweight parameter count suitable for edge-oriented deployment.

The implemented model contains approximately:

```text
70,197 trainable parameters
```

---

## Experimental Configuration

| Parameter | Value |
|---|---:|
| Architecture | LDMRes-Net |
| Input resolution | 640 × 640 |
| Framework | PyTorch |
| Optimizer | Adam |
| Initial learning rate | 1e-3 |
| Weight decay | 1e-4 |
| Batch size | 2 |
| Epochs | 200 |
| Loss function | Dice loss |
| Precision modes | FP32, INT8-PTQ, INT8-QAT |

---

## Results

| Metric | FP32 | INT8-PTQ | INT8-QAT |
|---|---:|---:|---:|
| F1 score | 79.10% | 77.48% | 77.66% |
| Sensitivity | 79.30% | 74.41% | 77.88% |
| Specificity | 98.00% | 98.37% | 97.87% |
| Accuracy | 96.33% | 96.25% | 96.10% |
| Inference time | ~400 ms | 267.6 ms | 251.6 ms |
| Model size | ~0.40 MB | 0.289 MB | 0.289 MB |

### Main Finding

Both INT8 approaches reduced model size and inference latency. However, **PTQ caused a larger drop in sensitivity**, while **QAT recovered more vessel sensitivity and achieved the fastest inference time**.

This suggests that QAT is the stronger option for preserving fine retinal vessel structures under INT8 compression.

---

## Repository Structure

A recommended structure for this repository is:

```text
int8-ldmresnet-retinal-segmentation/
│
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── .gitignore
│
├── paper/
│   ├── int8_ldmresnet_research_paper.pdf
│   ├── int8_ldmresnet_research_paper.tex
│   └── references.bib
│
├── notebooks/
│   └── ldmresnet_with_INT8_Final.ipynb
│
├── src/
│   ├── __init__.py
│   ├── dataset.py
│   ├── model.py
│   ├── train.py
│   ├── evaluate.py
│   ├── metrics.py
│   ├── quantization.py
│   └── utils.py
│
├── configs/
│   └── drive_ldmresnet.yaml
│
├── scripts/
│   ├── train_fp32.py
│   ├── run_ptq.py
│   ├── run_qat.py
│   └── evaluate_models.py
│
├── results/
│   ├── tables/
│   ├── figures/
│   └── qualitative_predictions/
│
├── checkpoints/
│   └── .gitkeep
│
└── data/
    └── README.md
```

### Notes

- Keep the **paper PDF and LaTeX files** inside `paper/`.
- Keep the original exploratory notebook inside `notebooks/`.
- Move reusable code from the notebook into `src/`.
- Keep generated plots, tables, and segmentation outputs inside `results/`.
- Do not commit the DRIVE dataset directly.
- Do not commit large trained weights unless they are small enough and intended for release.

---

## Installation

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
torch
torchvision
numpy
pillow
matplotlib
scikit-learn
tqdm
pyyaml
jupyter
```

Depending on your system, install the PyTorch version that matches your CPU/GPU setup from the official PyTorch installation instructions.

---

## Running the Notebook

Place the DRIVE dataset in `data/DRIVE/`, then open:

```text
notebooks/ldmresnet_with_INT8_Final.ipynb
```

Update the dataset path if required, then run the notebook cells in order.

---

## Suggested Script-Based Workflow

After refactoring the notebook into Python files, the project can be run as:

```bash
python scripts/train_fp32.py --config configs/drive_ldmresnet.yaml
python scripts/run_ptq.py --config configs/drive_ldmresnet.yaml
python scripts/run_qat.py --config configs/drive_ldmresnet.yaml
python scripts/evaluate_models.py --config configs/drive_ldmresnet.yaml
```

---

## Preprint and Citation

A preprint version of the paper is available in the `paper/` directory.

If you use this work, please cite:

```bibtex
@misc{desai2026int8ldmresnet,
  title        = {INT8-Quantized LDMRes-Net for Efficient Lightweight Medical Image Segmentation on Edge Devices},
  author       = {Desai, Dhruv Atul and Nair, Ashwin and Bhujbal, Atharva},
  year         = {2026},
  note         = {Preprint},
  institution  = {University of Galway}
}
```

---

## Authors

- **Dhruv Atul Desai**  
  MSc Computer Science/Data Analytics, University of Galway

- **Ashwin Nair**  
  MSc Artificial Intelligence, University of Galway

- **Atharva Bhujbal**  
  MSc Artificial Intelligence, University of Galway

---

## Limitations

- The DRIVE dataset is small, with only 20 training and 20 test images.
- The current implementation was evaluated in a software environment rather than on a dedicated medical edge device.
- Further validation is required on additional datasets such as CHASE DB1 and STARE.
- Hardware-specific inference benchmarking should be performed before making deployment claims.

---

## Future Work

- Evaluate on CHASE DB1 and STARE datasets.
- Deploy and benchmark on real edge hardware.
- Explore pruning, knowledge distillation, and mixed-precision quantization.
- Improve QAT schedules and calibration strategies.
- Package the pipeline as a reproducible training and evaluation framework.

---

## Disclaimer

This repository is intended for research and educational purposes only. It is not a clinically validated medical device or diagnostic system.
