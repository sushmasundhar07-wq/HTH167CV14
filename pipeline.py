from pathlib import Path
import json

import torch
from PIL import Image

from src.config import (
    DEVICE,
    MODEL_PATH,
    CLASS_NAMES_PATH
)

from src.preprocessing import get_validation_transform

from src.classifier import CropDiseaseClassifier

from src.severity import estimate_severity

from src.loss_model import estimate_loss

from src.spread_risk import estimate_spread_risk


class CropDiseasePipeline:

    def __init__(self):

        # -----------------------------------------------
        # Check model
        # -----------------------------------------------

        if not MODEL_PATH.exists():

            raise FileNotFoundError(
                f"Model not found:\n{MODEL_PATH}\n\n"
                "Please train the classifier first."
            )

        # -----------------------------------------------
        # Check class names
        # -----------------------------------------------

        if not CLASS_NAMES_PATH.exists():

            raise FileNotFoundError(
                f"Class names not found:\n"
                f"{CLASS_NAMES_PATH}"
            )

        # -----------------------------------------------
        # Load class names
        # -----------------------------------------------

        with open(
            CLASS_NAMES_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            self.class_names = json.load(file)

        # -----------------------------------------------
        # Create classifier
        # -----------------------------------------------

        self.classifier = CropDiseaseClassifier(

            num_classes=len(
                self.class_names
            ),

            device=DEVICE
        )

        # -----------------------------------------------
        # Load trained MobileNetV3 weights
        # -----------------------------------------------

        self.classifier.load_weights(
            MODEL_PATH
        )

        # -----------------------------------------------
        # Image preprocessing
        # -----------------------------------------------

        self.transform = (
            get_validation_transform()
        )


    # ===================================================
    # DISEASE PREDICTION
    # ===================================================

    def predict_disease(self, image):

        if not isinstance(
            image,
            Image.Image
        ):

            image = Image.fromarray(
                image
            )

        image = image.convert("RGB")

        image_tensor = self.transform(
            image
        ).unsqueeze(0)

        disease, confidence = (
            self.classifier.predict(
                image_tensor,
                self.class_names
            )
        )

        return disease, confidence


    # ===================================================
    # COMPLETE ANALYSIS
    # ===================================================

    def analyze(
        self,
        image,
        field_area_acres=1,
        expected_yield_per_acre=2000,
        crop_price_per_kg=30,
        humidity_percent=70,
        nearby_infected_fields=0
    ):

        # -----------------------------------------------
        # Disease
        # -----------------------------------------------

        disease, confidence = (
            self.predict_disease(image)
        )

        # -----------------------------------------------
        # Severity
        # -----------------------------------------------

        severity, affected_area = (
            estimate_severity(image)
        )

        # -----------------------------------------------
        # Yield / financial loss
        # -----------------------------------------------

        loss = estimate_loss(

            severity=severity,

            field_area_acres=
                field_area_acres,

            expected_yield_per_acre=
                expected_yield_per_acre,

            crop_price_per_kg=
                crop_price_per_kg
        )

        # -----------------------------------------------
        # Spread risk
        # -----------------------------------------------

        spread_score, spread_level = (
            estimate_spread_risk(

                severity=severity,

                affected_area_percent=
                    affected_area,

                humidity_percent=
                    humidity_percent,

                nearby_infected_fields=
                    nearby_infected_fields
            )
        )

        # -----------------------------------------------
        # Final result
        # -----------------------------------------------

        return {

            "disease": disease,

            "confidence": confidence,

            "severity": severity,

            "affected_area_percent":
                affected_area,

            "yield_loss_percent":
                loss.yield_loss_percent,

            "yield_loss_quantity":
                loss.yield_loss_quantity,

            "financial_loss":
                loss.financial_loss,

            "spread_risk_score":
                spread_score,

            "spread_risk_level":
                spread_level
        }