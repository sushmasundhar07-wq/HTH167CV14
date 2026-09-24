import cv2
import numpy as np


def estimate_severity(image):
    """
    Estimate visible disease severity from a leaf image.

    Returns:
        severity_label: Mild / Moderate / Severe
        affected_area: estimated percentage of affected pixels
    """

    if image is None:
        return "Unknown", 0.0

    # Convert RGB image to OpenCV format
    image = np.array(image)

    if len(image.shape) == 2:
        image = cv2.cvtColor(
            image,
            cv2.COLOR_GRAY2RGB
        )

    # Convert RGB to HSV
    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2HSV
    )

    # Detect darker / brownish / yellowish diseased regions
    lower_disease = np.array([
        10,
        40,
        20
    ])

    upper_disease = np.array([
        45,
        255,
        220
    ])

    mask = cv2.inRange(
        hsv,
        lower_disease,
        upper_disease
    )

    # Remove small noise
    kernel = np.ones(
        (5, 5),
        np.uint8
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    affected_pixels = np.sum(
        mask > 0
    )

    total_pixels = mask.shape[0] * mask.shape[1]

    affected_area = (
        affected_pixels
        / total_pixels
        * 100
    )

    # Severity thresholds for MVP
    if affected_area < 10:
        severity = "Mild"

    elif affected_area < 30:
        severity = "Moderate"

    else:
        severity = "Severe"

    return severity, round(
        float(affected_area),
        2
    )