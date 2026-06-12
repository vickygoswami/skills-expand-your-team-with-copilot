"""Fraud alert scoring utilities for payment transactions."""

from typing import Optional


HIGH_VALUE_WIRE_TRANSFER_THRESHOLD = 10_000


def _is_wire_transfer(transfer_type: Optional[str]) -> bool:
    normalized = (transfer_type or "").strip().lower().replace("_", " ").replace("-", " ")
    return "wire" in normalized


def calculate_fraud_alert_score(amount: float, transfer_type: Optional[str], is_new_device: bool) -> int:
    """
    Calculate a fraud alert score from 0 to 100.

    High-value wire transfers from a new device should receive the strongest
    alert score.
    """
    if amount < 0:
        raise ValueError("amount must be non-negative")

    score = 0
    wire_transfer = _is_wire_transfer(transfer_type)
    high_value_wire_transfer = wire_transfer and amount >= HIGH_VALUE_WIRE_TRANSFER_THRESHOLD

    if wire_transfer:
        score += 30

    if high_value_wire_transfer:
        score += 35

    if is_new_device:
        score += 25

    if high_value_wire_transfer and is_new_device:
        score += 20

    return min(score, 100)


def score_fraud_alert(amount: float, transfer_type: Optional[str], is_new_device: bool) -> int:
    """Backward-compatible alias for fraud alert scoring."""
    return calculate_fraud_alert_score(amount=amount, transfer_type=transfer_type, is_new_device=is_new_device)
