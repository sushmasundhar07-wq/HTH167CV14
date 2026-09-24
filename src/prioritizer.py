from dataclasses import dataclass


@dataclass
class Field:
    name: str
    severity: str
    financial_loss: float
    treatment_cost: float
    spread_risk: float


SEVERITY_SCORE = {
    "Mild": 1,
    "Moderate": 2,
    "Severe": 3,
}


def calculate_priority_score(field):
    """
    Calculate a treatment priority score.

    Higher score means the field deserves earlier attention.

    Factors:
    - Severity
    - Potential financial loss
    - Spread risk
    """

    severity_score = SEVERITY_SCORE.get(
        field.severity,
        0
    )

    loss_score = min(
        field.financial_loss / 10000,
        10
    )

    spread_score = min(
        field.spread_risk,
        100
    ) / 10

    priority_score = (
        severity_score * 4
        + loss_score * 3
        + spread_score * 3
    )

    return round(
        priority_score,
        2
    )


def prioritize_fields(fields, budget):
    """
    Prioritize fields under a treatment budget.

    Returns:
        List of dictionaries containing:
        - field name
        - priority score
        - treatment decision
    """

    if budget < 0:
        raise ValueError(
            "Budget cannot be negative."
        )

    results = []

    for field in fields:

        score = calculate_priority_score(
            field
        )

        results.append({
            "field": field.name,
            "severity": field.severity,
            "financial_loss": field.financial_loss,
            "treatment_cost": field.treatment_cost,
            "spread_risk": field.spread_risk,
            "priority_score": score,
        })

    # Highest priority first
    results.sort(
        key=lambda x: x["priority_score"],
        reverse=True
    )

    remaining_budget = budget

    for result in results:

        treatment_cost = result[
            "treatment_cost"
        ]

        if treatment_cost <= remaining_budget:

            result["decision"] = (
                "Treat Now"
            )

            remaining_budget -= (
                treatment_cost
            )

        else:

            result["decision"] = (
                "Monitor / Defer"
            )

    return results, remaining_budget