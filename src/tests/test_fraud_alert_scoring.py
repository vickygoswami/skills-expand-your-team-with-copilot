import unittest

from src.backend.fraud_alert_scoring import calculate_fraud_alert_score, score_fraud_alert


class FraudAlertScoringTests(unittest.TestCase):
    def test_high_value_new_device_wire_transfer_gets_max_score(self):
        score = calculate_fraud_alert_score(
            amount=25_000,
            transfer_type="wire transfer",
            is_new_device=True,
        )
        self.assertEqual(score, 100)

    def test_high_value_wire_transfer_is_lower_without_new_device(self):
        score = calculate_fraud_alert_score(
            amount=25_000,
            transfer_type="wire transfer",
            is_new_device=False,
        )
        self.assertEqual(score, 65)

    def test_non_wire_transfer_does_not_get_wire_risk_points(self):
        score = calculate_fraud_alert_score(
            amount=25_000,
            transfer_type="ach",
            is_new_device=True,
        )
        self.assertEqual(score, 25)

    def test_score_fraud_alert_alias_matches_main_function(self):
        score = score_fraud_alert(
            amount=25_000,
            transfer_type="wire transfer",
            is_new_device=True,
        )
        self.assertEqual(score, 100)

    def test_combined_new_device_bonus_changes_high_value_wire_score(self):
        known_device_score = calculate_fraud_alert_score(
            amount=25_000,
            transfer_type="wire transfer",
            is_new_device=False,
        )
        new_device_score = calculate_fraud_alert_score(
            amount=25_000,
            transfer_type="wire transfer",
            is_new_device=True,
        )
        self.assertEqual(new_device_score - known_device_score, 35)


if __name__ == "__main__":
    unittest.main()
