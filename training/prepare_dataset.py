from pathlib import Path
import random
import shutil


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

SOURCE_DIR = PROJECT_DIR / "data" / "raw" / "PlantVillage"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

RANDOM_SEED = 42

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".ppm",
    ".pgm",
    ".tif",
    ".tiff",
    ".webp",
}


# ============================================================
# SET RANDOM SEED
# ============================================================

random.seed(RANDOM_SEED)


# ============================================================
# CHECK SOURCE DATASET
# ============================================================

print("=" * 60)
print("PLANTVILLAGE DATASET PREPARATION")
print("=" * 60)

print("\nProject directory:")
print(PROJECT_DIR)

print("\nDataset directory:")
print(SOURCE_DIR)


if not SOURCE_DIR.exists():

    raise FileNotFoundError(
        f"\nPlantVillage dataset was not found at:\n"
        f"{SOURCE_DIR}\n\n"
        f"Please make sure your dataset is located at:\n"
        f"data/raw/PlantVillage"
    )


# ============================================================
# FIND ALL IMAGES
# ============================================================

print("\nSearching for images...")

all_images = []

for file in SOURCE_DIR.rglob("*"):

    if file.is_file():

        if file.suffix.lower() in {
            ext.lower() for ext in IMAGE_EXTENSIONS
        }:

            all_images.append(file)


if len(all_images) == 0:

    raise RuntimeError(
        "\nNo images were found inside PlantVillage.\n"
        "Please check the dataset extraction."
    )


print(f"Total images found: {len(all_images)}")


# ============================================================
# GROUP IMAGES BY CLASS
# ============================================================

class_images = {}

for image_path in all_images:

    # The immediate parent directory is treated as the class
    class_name = image_path.parent.name

    if class_name not in class_images:

        class_images[class_name] = []

    class_images[class_name].append(image_path)


classes = sorted(class_images.keys())


print(f"Number of classes found: {len(classes)}")


# ============================================================
# DISPLAY CLASSES
# ============================================================

print("\nClasses:")

for class_name in classes:

    print(
        f"  {class_name}: "
        f"{len(class_images[class_name])} images"
    )


# ============================================================
# REMOVE OLD PROCESSED DATASET
# ============================================================

if OUTPUT_DIR.exists():

    print("\nRemoving old processed dataset...")

    shutil.rmtree(OUTPUT_DIR)


# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

TRAIN_DIR = OUTPUT_DIR / "train"
VAL_DIR = OUTPUT_DIR / "val"
TEST_DIR = OUTPUT_DIR / "test"

TRAIN_DIR.mkdir(
    parents=True,
    exist_ok=True
)

VAL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

TEST_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# SPLIT DATA
# ============================================================

total_train = 0
total_val = 0
total_test = 0

usable_classes = 0

print("\n" + "=" * 60)
print("CREATING TRAIN / VALIDATION / TEST DATA")
print("=" * 60)


for class_name in classes:

    images = class_images[class_name].copy()

    random.shuffle(images)

    total = len(images)


    # --------------------------------------------------------
    # A class needs at least 3 images
    # --------------------------------------------------------

    if total < 3:

        print(
            f"\nSkipping {class_name}: "
            f"only {total} image(s)"
        )

        continue


    # --------------------------------------------------------
    # Calculate split sizes
    # --------------------------------------------------------

    train_count = int(total * TRAIN_RATIO)

    val_count = int(total * VAL_RATIO)

    test_count = total - train_count - val_count


    # Guarantee at least one image per split
    if train_count < 1:
        train_count = 1

    if val_count < 1:
        val_count = 1

    if test_count < 1:
        test_count = 1


    # --------------------------------------------------------
    # Adjust if total is too small
    # --------------------------------------------------------

    while train_count + val_count + test_count > total:

        if train_count > 1:
            train_count -= 1

        elif val_count > 1:
            val_count -= 1

        elif test_count > 1:
            test_count -= 1

        else:
            break


    # --------------------------------------------------------
    # Create splits
    # --------------------------------------------------------

    train_images = images[:train_count]

    val_images = images[
        train_count:
        train_count + val_count
    ]

    test_images = images[
        train_count + val_count:
        train_count + val_count + test_count
    ]


    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    if (
        len(train_images) == 0
        or len(val_images) == 0
        or len(test_images) == 0
    ):

        print(
            f"\nSkipping {class_name}: "
            f"unable to create all three splits."
        )

        continue


    # --------------------------------------------------------
    # Create class folders
    # --------------------------------------------------------

    train_class_dir = TRAIN_DIR / class_name
    val_class_dir = VAL_DIR / class_name
    test_class_dir = TEST_DIR / class_name

    train_class_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    val_class_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    test_class_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    # --------------------------------------------------------
    # Copy images
    # --------------------------------------------------------

    for image in train_images:

        destination = train_class_dir / image.name

        shutil.copy2(
            image,
            destination
        )


    for image in val_images:

        destination = val_class_dir / image.name

        shutil.copy2(
            image,
            destination
        )


    for image in test_images:

        destination = test_class_dir / image.name

        shutil.copy2(
            image,
            destination
        )


    # --------------------------------------------------------
    # Counters
    # --------------------------------------------------------

    total_train += len(train_images)
    total_val += len(val_images)
    total_test += len(test_images)

    usable_classes += 1


    print(
        f"\n{class_name}"
    )

    print(
        f"  Total: {total}"
    )

    print(
        f"  Train: {len(train_images)}"
    )

    print(
        f"  Val:   {len(val_images)}"
    )

    print(
        f"  Test:  {len(test_images)}"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DATASET PREPARATION COMPLETE")
print("=" * 60)

print(
    f"\nUsable classes:      {usable_classes}"
)

print(
    f"Total source images: {len(all_images)}"
)

print(
    f"Training images:     {total_train}"
)

print(
    f"Validation images:   {total_val}"
)

print(
    f"Testing images:      {total_test}"
)

print(
    f"\nProcessed dataset:"
)

print(
    OUTPUT_DIR
)

if usable_classes == 0:

    raise RuntimeError(
        "\nNo usable classes were created."
    )

print(
    "\nDataset is ready for training."
)