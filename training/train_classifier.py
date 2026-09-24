from pathlib import Path
import json
import random

import torch
from torch import nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms, models


# ============================================================
# CONFIG
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

TRAIN_DIR = PROJECT_DIR / "data" / "processed" / "train"
VAL_DIR = PROJECT_DIR / "data" / "processed" / "val"
TEST_DIR = PROJECT_DIR / "data" / "processed" / "test"

MODEL_DIR = PROJECT_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "crop_disease_mobilenetv3.pth"
CLASS_NAMES_PATH = MODEL_DIR / "class_names.json"

IMAGE_SIZE = 224

MAX_TRAIN_IMAGES = 3000
MAX_VAL_IMAGES = 600
MAX_TEST_IMAGES = 600

BATCH_SIZE = 32
NUM_EPOCHS = 3
LEARNING_RATE = 0.001

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


print("=" * 60)
print("CROP DISEASE CLASSIFIER - MOBILE NET V3 SMALL")
print("=" * 60)

print()
print("Project directory:")
print(PROJECT_DIR)

print()
print("Device:", DEVICE)


# ============================================================
# TRANSFORMS
# ============================================================

train_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

val_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])


# ============================================================
# LOAD DATASETS
# ============================================================

print()
print("Loading datasets...")

train_dataset_full = datasets.ImageFolder(
    TRAIN_DIR,
    transform=train_transform
)

val_dataset_full = datasets.ImageFolder(
    VAL_DIR,
    transform=val_transform
)

test_dataset_full = datasets.ImageFolder(
    TEST_DIR,
    transform=val_transform
)

class_names = train_dataset_full.classes
num_classes = len(class_names)

print()
print("Total training images:", len(train_dataset_full))
print("Total validation images:", len(val_dataset_full))
print("Total test images:", len(test_dataset_full))
print("Number of classes:", num_classes)


# ============================================================
# BALANCED SUBSET
# ============================================================

def create_balanced_subset(dataset, max_images):
    """
    Select approximately the same number of images
    from each class.
    """

    class_to_indices = {}

    for index, (_, class_id) in enumerate(dataset.samples):
        if class_id not in class_to_indices:
            class_to_indices[class_id] = []

        class_to_indices[class_id].append(index)

    selected_indices = []

    num_classes = len(class_to_indices)

    images_per_class = max_images // num_classes

    for class_id in sorted(class_to_indices.keys()):

        indices = class_to_indices[class_id]

        random.shuffle(indices)

        selected = indices[:images_per_class]

        selected_indices.extend(selected)

    random.shuffle(selected_indices)

    return Subset(dataset, selected_indices)


train_dataset = create_balanced_subset(
    train_dataset_full,
    MAX_TRAIN_IMAGES
)

val_dataset = create_balanced_subset(
    val_dataset_full,
    MAX_VAL_IMAGES
)

test_dataset = create_balanced_subset(
    test_dataset_full,
    MAX_TEST_IMAGES
)


print()
print("MobileNetV3 training images:", len(train_dataset))
print("MobileNetV3 validation images:", len(val_dataset))
print("MobileNetV3 test images:", len(test_dataset))


# ============================================================
# DATA LOADERS
# ============================================================

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)


# ============================================================
# MODEL
# ============================================================

print()
print("Loading MobileNetV3-Small...")

weights = models.MobileNet_V3_Small_Weights.DEFAULT

model = models.mobilenet_v3_small(
    weights=weights
)

print("Pretrained MobileNetV3-Small loaded.")


# Freeze feature extractor
for parameter in model.features.parameters():
    parameter.requires_grad = False


# Replace classifier
in_features = model.classifier[-1].in_features

model.classifier[-1] = nn.Linear(
    in_features,
    num_classes
)

model = model.to(DEVICE)


# ============================================================
# LOSS + OPTIMIZER
# ============================================================

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.classifier.parameters(),
    lr=LEARNING_RATE
)


# ============================================================
# TRAINING FUNCTION
# ============================================================

def train_one_epoch():

    model.train()

    total_loss = 0
    correct = 0
    total = 0

    for images, labels in train_loader:

        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        total_loss += loss.item() * images.size(0)

        predictions = outputs.argmax(dim=1)

        correct += (predictions == labels).sum().item()

        total += labels.size(0)

    average_loss = total_loss / total

    accuracy = correct / total * 100

    return average_loss, accuracy


# ============================================================
# VALIDATION FUNCTION
# ============================================================

def evaluate(loader):

    model.eval()

    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():

        for images, labels in loader:

            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(images)

            loss = criterion(outputs, labels)

            total_loss += loss.item() * images.size(0)

            predictions = outputs.argmax(dim=1)

            correct += (predictions == labels).sum().item()

            total += labels.size(0)

    average_loss = total_loss / total

    accuracy = correct / total * 100

    return average_loss, accuracy


# ============================================================
# TRAIN
# ============================================================

print()
print("=" * 60)
print("STARTING MOBILENETV3 TRAINING")
print("=" * 60)

best_val_accuracy = 0.0

for epoch in range(NUM_EPOCHS):

    print()
    print(f"Epoch {epoch + 1}/{NUM_EPOCHS}")

    train_loss, train_accuracy = train_one_epoch()

    val_loss, val_accuracy = evaluate(val_loader)

    print(
        f"Train Loss: {train_loss:.4f} | "
        f"Train Accuracy: {train_accuracy:.2f}%"
    )

    print(
        f"Validation Loss: {val_loss:.4f} | "
        f"Validation Accuracy: {val_accuracy:.2f}%"
    )

    if val_accuracy > best_val_accuracy:

        best_val_accuracy = val_accuracy

        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "num_classes": num_classes,
                "model_name": "mobilenet_v3_small",
            },
            MODEL_PATH
        )

        print("✓ Best model saved.")


# ============================================================
# TEST
# ============================================================

print()
print("=" * 60)
print("FINAL TEST")
print("=" * 60)

checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

test_loss, test_accuracy = evaluate(test_loader)

print()
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.2f}%")


# ============================================================
# SAVE CLASS NAMES
# ============================================================

with open(
    CLASS_NAMES_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        class_names,
        file,
        indent=2
    )


# ============================================================
# DONE
# ============================================================

print()
print("=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print()
print("Model saved to:")
print(MODEL_PATH)

print()
print("Class names saved to:")
print(CLASS_NAMES_PATH)

print()
print("Best validation accuracy:")
print(f"{best_val_accuracy:.2f}%")

print()
print("Test accuracy:")
print(f"{test_accuracy:.2f}%")