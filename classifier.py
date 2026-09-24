import torch
from torch import nn
from torchvision import models


class CropDiseaseClassifier:

    def __init__(self, num_classes, device=None):

        self.device = device or torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.model = models.mobilenet_v3_small(
            weights=None
        )

        input_features = self.model.classifier[-1].in_features

        self.model.classifier[-1] = nn.Linear(
            input_features,
            num_classes
        )

        self.model = self.model.to(self.device)


    def load_weights(self, model_path):

        checkpoint = torch.load(
            model_path,
            map_location=self.device
        )

        if (
            isinstance(checkpoint, dict)
            and "model_state_dict" in checkpoint
        ):
            self.model.load_state_dict(
                checkpoint["model_state_dict"]
            )
        else:
            self.model.load_state_dict(checkpoint)

        self.model.eval()


    def predict(self, image_tensor, class_names):

        self.model.eval()

        image_tensor = image_tensor.to(self.device)

        with torch.no_grad():

            outputs = self.model(image_tensor)

            probabilities = torch.softmax(
                outputs,
                dim=1
            )

            confidence, prediction = torch.max(
                probabilities,
                dim=1
            )

        class_index = prediction.item()

        disease = class_names[class_index]

        confidence_percent = (
            confidence.item() * 100
        )

        return (
            disease,
            round(confidence_percent, 2)
        )


    def predict_top_k(
        self,
        image_tensor,
        class_names,
        k=3
    ):

        self.model.eval()

        image_tensor = image_tensor.to(self.device)

        with torch.no_grad():

            outputs = self.model(image_tensor)

            probabilities = torch.softmax(
                outputs,
                dim=1
            )

            values, indices = torch.topk(
                probabilities,
                k
            )

        results = []

        for probability, index in zip(
            values[0],
            indices[0]
        ):

            results.append({
                "disease": class_names[index.item()],
                "confidence": round(
                    probability.item() * 100,
                    2
                )
            })

        return results