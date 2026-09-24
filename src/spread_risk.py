def estimate_spread_risk(
    severity,
    affected_area_percent,
    humidity_percent=70,
    nearby_infected_fields=0,
):
    """
    Estimate disease spread risk for an MVP.

    Returns:
        risk_score: 0-100
        risk_level: Low / Medium / High
    """

    severity_scores = {
        "Mild": 20,
        "Moderate": 50,
        "Severe": 80,
    }

    severity_score = severity_scores.get(
        severity,
        0
    )

    # More affected area increases spread risk.
    area_score = min(
        affected_area_percent,
        100
    )

    # Humidity can favor the spread of many
    # plant diseases, but this is a generic MVP assumption.
    humidity_score = min(
        max(humidity_percent, 0),
        100
    )

    # Nearby infected fields increase risk.
    nearby_score = min(
        nearby_infected_fields * 10,
        100
    )

    risk_score = (
        severity_score * 0.40
        + area_score * 0.30
        + humidity_score * 0.15
        + nearby_score * 0.15
    )

    risk_score = round(
        min(max(risk_score, 0), 100),
        2
    )

    if risk_score < 35:
        risk_level = "Low"

    elif risk_score < 65:
        risk_level = "Medium"

    else:
        risk_level = "High"

    return risk_score, risk_level