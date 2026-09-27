Crop Disease Prediction

A machine-learning based crop disease prediction project designed to analyze crop/leaf images, identify possible diseases, estimate disease severity, assess potential loss and spread risk, and prioritize cases for further attention.

The project is organized into separate modules for **data preparation, model training, prediction, disease analysis, prioritization, and frontend interaction**.

**Table of Contents**

- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Main Components](#main-components)
- [Machine Learning Workflow](#machine-learning-workflow)
- [Output](#output)
- [Running the Project](#running-the-project)
- [Model Training](#model-training)
- [Model Evaluation](#model-evaluation)
- [Frontend](#frontend)
- [Configuration](#configuration)
- [Technologies](#technologies)
- [Important Notes](#important-notes)
- [Future Improvements](#future-improvements)

## Project Overview

Crop diseases can reduce crop quality and production when they are not detected early. This project provides a structured machine-learning pipeline for crop disease analysis.

The system is designed around the following workflow:

Crop / Leaf Image
        |
        v
   Preprocessing
        |
        v
 Disease Classification
        |
        +------------------+
        |                  |
        v                  v
 Disease Severity      Spread Risk
        |                  |
        +--------+---------+
                 |
                 v
          Potential Loss
                 |
                 v
            Prioritization
                 |
                 v
          Final Prediction

The classification model identifies the disease, while the additional modules provide information that can help determine the seriousness and priority of the detected condition.

> **Note:** The exact prediction method, formulas, model architecture, and output labels depend on the implementation contained in the Python source files.


## Objectives

The main objectives of this project are:

1. Detect crop diseases from input data/images.
2. Preprocess input data into a format suitable for machine learning.
3. Train and evaluate a disease classification model.
4. Estimate the severity of a detected disease.
5. Estimate potential crop loss.
6. Estimate the risk of disease spread.
7. Combine relevant information to prioritize affected cases.
8. Provide a frontend through which users can interact with the system.

---

# Project Architecture

The project is divided into four major areas:

### 1. `training/`

Contains scripts used to prepare the dataset, train the classifier, and evaluate the trained model.

### 2. `src/`

Contains the main application and prediction logic.

### 3. `models/`

Stores trained model files used during prediction.

### 4. `frontend/`

Contains the user interface files.

This separation makes the project easier to understand, test, maintain, and extend.

---

# Directory Structure

```text
CropDiseaseprediction/
│
└── hth-cv-06/
    │
    ├── frontend/
    │   ├── script.js
    │   └── style.css
    │
    ├── models/
    │   └── # Trained model files
    │
    ├── notebooks/
    │   └── # Jupyter notebooks / experiments
    │
    ├── src/
    │   ├── __init__.py
    │   ├── classifier.py
    │   ├── config.py
    │   ├── loss_model.py
    │   ├── pipeline.py
    │   ├── preprocessing.py
    │   ├── prioritizer.py
    │   ├── severity.py
    │   └── spread_risk.py
    │
    ├── training/
    │   ├── evaluate.py
    │   ├── prepare_dataset.py
    │   └── train_classifier.py
    │
    ├── .gitignore
    ├── README.md
    └── venv/
```

---

# How the System Works

## Step 1 — Input

The system receives crop/leaf data, typically an image or a dataset containing crop disease examples.

```text
Input Image
     |
     v
Preprocessing
```

---

## Step 2 — Preprocessing

The input is prepared before it is passed to the machine-learning model.

Typical preprocessing operations can include:

- Loading the image
- Resizing
- Converting image format
- Normalization
- Converting the image into a numerical representation
- Applying the same transformations used during model training

The implementation in `src/preprocessing.py` defines the actual preprocessing operations.

---

## Step 3 — Disease Classification

The processed input is passed to the classifier.

```text
Processed Image
       |
       v
  ML Classifier
       |
       v
Predicted Disease
```

The main classification logic is contained in:

```text
src/classifier.py
```

The classifier is responsible for identifying the disease category represented by the input.

---

## Step 4 — Severity Estimation

After identifying a disease, the system can estimate how severe the condition is.

This functionality is implemented in:

```text
src/severity.py
```

Conceptually:

```text
Disease Detection
       +
Disease Evidence
       |
       v
Severity Estimate
```

Depending on the implementation, severity may be represented as a percentage, category, score, or another value.

---

## Step 5 — Potential Loss Estimation

The project also contains:

```text
src/loss_model.py
```

This module is intended to estimate potential crop loss based on information available to the system.

Conceptually:

```text
Disease
   +
Severity / Other Factors
   |
   v
Potential Loss Estimate
```

The exact loss calculation is defined by the implementation of `loss_model.py`.

---

## Step 6 — Spread Risk

The project contains a separate module:

```text
src/spread_risk.py
```

This component estimates the risk that the detected disease may spread.

Conceptually:

```text
Disease Information
       +
Severity / Relevant Factors
       |
       v
Spread Risk
```

The exact inputs and calculation are defined in the source code.

---

## Step 7 — Prioritization

The final analysis can be used to prioritize cases.

This functionality is contained in:

```text
src/prioritizer.py
```

A conceptual prioritization flow is:

```text
Severity
   +
Potential Loss
   +
Spread Risk
   |
   v
Priority Assessment
```

This allows the system to distinguish cases that may require more immediate attention from cases with lower estimated impact.

---

# Main Components

## `src/classifier.py`

Contains the disease classification logic.

**Purpose:**

- Load/use the trained classifier.
- Process prepared input.
- Generate disease predictions.

---

## `src/preprocessing.py`

Contains input/data preprocessing functionality.

**Purpose:**

- Prepare raw input.
- Apply transformations required by the model.
- Convert input into a model-compatible representation.

---

## `src/pipeline.py`

Connects the different components into a complete prediction workflow.

A typical pipeline is:

```text
Input
  ↓
Preprocessing
  ↓
Classification
  ↓
Severity
  ↓
Loss Estimation
  ↓
Spread Risk
  ↓
Prioritization
  ↓
Result
```

This file acts as the central orchestration layer of the application.

---

## `src/severity.py`

Handles disease severity estimation.

---

## `src/loss_model.py`

Handles potential loss estimation.

---

## `src/spread_risk.py`

Handles disease spread-risk estimation.

---

## `src/prioritizer.py`

Combines relevant outputs and determines the priority of a case according to the project's implemented rules/model.

---

## `src/config.py`

Contains configuration values used by different components of the application.

Keeping configuration in one place makes the project easier to maintain.

---

# Machine Learning Workflow

The training workflow is contained inside the `training/` directory.

## 1. Dataset Preparation

File:

```text
training/prepare_dataset.py
```

This script is responsible for preparing the dataset before model training.

Typical steps may include:

```text
Raw Dataset
    ↓
Data Cleaning
    ↓
Data Organization
    ↓
Preprocessing
    ↓
Train / Validation / Test Data
```

The exact operations depend on the implementation.

---

## 2. Model Training

File:

```text
training/train_classifier.py
```

This script trains the disease classification model.

General workflow:

```text
Prepared Dataset
      ↓
Training Data
      ↓
Machine Learning Model
      ↓
Training
      ↓
Validation
      ↓
Trained Model
      ↓
models/
```

The trained model can then be used by the prediction pipeline.

---

## 3. Model Evaluation

File:

```text
training/evaluate.py
```

This script is used to evaluate the trained classifier.

Depending on the implementation, evaluation can include metrics such as:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

These metrics help determine how the classifier performs on evaluation data.

---

# Models Directory

The `models/` directory is intended to contain trained model artifacts.

For example:

```text
models/
├── trained_classifier.*
└── other_model_files.*
```

The exact filenames and formats depend on the training implementation.

Model files should be generated by the project's training process rather than manually edited.

---

# Notebooks

The `notebooks/` directory is intended for exploratory analysis and experimentation.

Jupyter notebooks can be used for:

- Exploring the dataset
- Visualizing images
- Testing preprocessing methods
- Experimenting with models
- Analyzing training results
- Creating plots and reports

The final reusable application logic should remain in `src/`.

---

# Frontend

The frontend is located in:

```text
frontend/
```

It contains:

```text
frontend/
├── script.js
└── style.css
```

## `script.js`

Handles frontend behavior and user interaction.

Possible responsibilities include:

- Receiving user input
- Sending data to the prediction system
- Handling responses
- Displaying prediction results
- Updating the interface

## `style.css`

Controls the visual presentation of the frontend.

It can define:

- Layout
- Colors
- Fonts
- Buttons
- Cards
- Spacing
- Responsive behavior

---

# Installation

## 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd CropDiseaseprediction
```

Replace `<YOUR_REPOSITORY_URL>` with the actual repository URL.

---

## 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Linux/macOS:

```bash
python3 -m venv venv
```

---

## 3. Activate the virtual environment

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

---

## 4. Install dependencies

If the repository contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If dependencies are managed through another file such as `pyproject.toml` or `environment.yml`, follow the installation instructions defined by that file.

> The repository structure shown for this project does not expose a dependency file, so the exact package list should be taken from the project's Python imports/environment configuration rather than guessed.

---

# Running the Project

The exact command depends on how the backend/application entry point is implemented.

The main application logic is organized around:

```text
src/pipeline.py
```

The frontend files are located at:

```text
frontend/
```

If a dedicated application entry point or server file is added later, document its command here.

For example, if the project uses a Python web framework, the README can be updated with the corresponding server command.

---

# Model Training

To train the classifier, the general workflow is:

### Step 1

Prepare the dataset:

```bash
python training/prepare_dataset.py
```

### Step 2

Train the classifier:

```bash
python training/train_classifier.py
```

### Step 3

Evaluate the model:

```bash
python training/evaluate.py
```

> These commands assume that the corresponding scripts are executable as standalone Python programs. If the scripts require command-line arguments or a different execution method, use the arguments defined inside those files.

---

# Prediction Pipeline

Once a trained model is available, the application can use the prediction pipeline.

Conceptually:

```python
input_data
    ↓
preprocessing
    ↓
classifier
    ↓
severity
    ↓
loss model
    ↓
spread risk
    ↓
prioritizer
    ↓
final result
```

The central coordination logic is located in:

```text
src/pipeline.py
```

---

# Expected Output

A prediction may contain information such as:

```text
Disease:
    <predicted disease>

Severity:
    <severity result>

Potential Loss:
    <loss estimate>

Spread Risk:
    <spread-risk result>

Priority:
    <priority result>
```

The exact output format depends on the implementation.

---

# Configuration

Project-level configuration is stored in:

```text
src/config.py
```

Keeping configuration values separate from application logic makes it easier to modify things such as:

- Model paths
- Dataset paths
- Image dimensions
- Thresholds
- Other project parameters

without changing multiple source files.

---

# Technologies

The project is primarily organized as a **Python machine-learning application with a web frontend**.

The exact Python libraries should be taken from the imports and dependency configuration in the project.

Typical categories used by this type of project include:

| Technology / Category | Purpose |
|---|---|
| Python | Main programming language |
| Machine Learning / Deep Learning framework | Training and running the disease classifier |
| Image processing library | Loading and preprocessing crop images |
| Numerical computing library | Numerical operations and arrays |
| Data processing library | Dataset manipulation |
| ML utility library | Dataset splitting and evaluation metrics |
| JavaScript | Frontend interaction |
| CSS | Frontend styling |
| Jupyter | Data exploration and experimentation |
| Git | Version control |

**Important:** This table describes the technology categories used by the project architecture. The exact package names and versions should be documented from the project's actual dependency files/imports.

---

# Why the Project Is Modular

Instead of putting everything into one Python file, the project separates responsibilities:

```text
classifier.py
    → Disease prediction

preprocessing.py
    → Input preparation

severity.py
    → Severity estimation

loss_model.py
    → Loss estimation

spread_risk.py
    → Spread-risk estimation

prioritizer.py
    → Priority calculation

pipeline.py
    → Connects everything
```

This modular design provides several advantages:

- Easier debugging
- Easier testing
- Easier maintenance
- Components can be modified independently
- New models can be added more easily
- The prediction workflow is easier to understand

---

# Development Workflow

A recommended development workflow is:

```text
1. Collect Dataset
       ↓
2. Prepare Dataset
       ↓
3. Explore Dataset
       ↓
4. Train Classifier
       ↓
5. Evaluate Classifier
       ↓
6. Save Model
       ↓
7. Integrate Model into Pipeline
       ↓
8. Add Severity Analysis
       ↓
9. Add Loss Estimation
       ↓
10. Add Spread-Risk Analysis
       ↓
11. Add Prioritization
       ↓
12. Connect Frontend
       ↓
13. Test Complete System
```

---

# Testing and Evaluation

The project should be tested at multiple levels.

### Data testing

Verify that:

- Images/data can be loaded.
- Labels are correct.
- Invalid inputs are handled.
- Training and testing data are separated appropriately.

### Model testing

Evaluate:

- Classification performance
- Incorrect predictions
- Class-wise performance
- Generalization to unseen data

### Pipeline testing

Verify that:

```text
Input → Prediction → Severity → Loss → Spread Risk → Priority
```

works correctly for valid inputs and handles invalid inputs safely.

### Frontend testing

Verify:

- Image/input selection
- Prediction request
- Result display
- Error handling
- Different screen sizes

---

# Limitations

Machine-learning predictions depend strongly on the quality and diversity of the training data.

Potential limitations include:

- Poor-quality input images
- Lighting differences
- Background differences
- Disease classes not represented in the training dataset
- Dataset imbalance
- Incorrect labels
- Model generalization limitations
- Simplified assumptions in severity, loss, or spread-risk calculations

The system should therefore be treated as a **decision-support and research system**, not as a replacement for expert agricultural diagnosis.

---

# Future Improvements

Possible future improvements include:

- Add more crop and disease classes.
- Increase dataset size and diversity.
- Use data augmentation.
- Improve model accuracy and robustness.
- Add confidence scores to predictions.
- Add explainable-AI visualizations such as heatmaps.
- Improve severity estimation using image segmentation.
- Incorporate environmental information into spread-risk estimation.
- Improve loss estimation using crop-specific economic data.
- Add database storage for previous predictions.
- Add authentication and user management.
- Deploy the application as a web service.
- Add mobile-friendly support.
- Add model monitoring and periodic retraining.

---

# Contributing

Contributions are welcome.

A typical contribution workflow is:

```text
Fork Repository
      ↓
Create Feature Branch
      ↓
Make Changes
      ↓
Test Changes
      ↓
Commit Changes
      ↓
Create Pull Request
```

Before submitting changes, make sure that existing functionality continues to work.

---


# Project Summary

**Crop Disease Prediction** is a modular machine-learning project that combines disease classification with additional analysis such as severity estimation, potential loss estimation, spread-risk assessment, and prioritization.

The project separates:

```text
DATA PREPARATION
       ↓
MODEL TRAINING
       ↓
MODEL EVALUATION
       ↓
PREDICTION
       ↓
DISEASE ANALYSIS
       ↓
PRIORITIZATION
       ↓
FRONTEND
```

This structure makes the system easier to develop, test, explain, and extend.
