from dataclasses import dataclass


@dataclass
class LossEstimate:
    yield_loss_percent: float
    yield_loss_quantity: float
    financial_loss: float


# Approximate severity-to-yield-loss assumptions for MVP.
# These are demo assumptions and should be replaced with
# crop/disease-specific research or field data later.
SEVERITY_LOSS = {
    "Mild": 0.10,
    "Moderate": 0.25,
    "Severe": 0.40,
}


def estimate_loss(
    severity,
    field_area_acres,
    expected_yield_per_acre,
    crop_price_per_kg,
):
    """
    Estimate potential yield and financial loss if untreated.

    Args:
        severity: Mild / Moderate / Severe
        field_area_acres: Field size in acres
        expected_yield_per_acre: Expected crop yield per acre in kg
        crop_price_per_kg: Crop selling price per kg

    Returns:
        LossEstimate
    """

    if severity not in SEVERITY_LOSS:
        raise ValueError(
            f"Unknown severity: {severity}"
        )

    if field_area_acres < 0:
        raise ValueError(
            "Field area cannot be negative."
        )

    if expected_yield_per_acre < 0:
        raise ValueError(
            "Expected yield cannot be negative."
        )

    if crop_price_per_kg < 0:
        raise ValueError(
            "Crop price cannot be negative."
        )

    loss_rate = SEVERITY_LOSS[severity]

    total_expected_yield = (
        field_area_acres
        * expected_yield_per_acre
    )

    yield_loss_quantity = (
        total_expected_yield
        * loss_rate
    )

    financial_loss = (
        yield_loss_quantity
        * crop_price_per_kg
    )

    return LossEstimate(
        yield_loss_percent=loss_rate * 100,
        yield_loss_quantity=round(
            yield_loss_quantity,
            2
        ),
        financial_loss=round(
            financial_loss,
            2
        ),
    )