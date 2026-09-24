from pathlib import Path
import torch

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

TRAIN_DIR = PROCESSED_DATA_DIR / "train"
VAL_DIR = PROCESSED_DATA_DIR / "val"
TEST_DIR = PROCESSED_DATA_DIR / "test"

MODEL_DIR = PROJECT_DIR / "models"

MODEL_PATH = MODEL_DIR / "crop_disease_mobilenetv3.pth"
CLASS_NAMES_PATH = MODEL_DIR / "class_names.json"

IMAGE_SIZE = 224

BATCH_SIZE = 32
LEARNING_RATE = 0.001
NUM_EPOCHS = 3

NUM_CLASSES = 38

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)
