import pytest
from water_utility_billing import calculate_water_bill, check_meter_tampering


class TestCalculateWaterBillBranches:
    """Branch coverage tests for calculate_water_bill."""

    def test_branch_invalid_accounts_not_a_list(self):
        """Branch: not isinstance(accounts, list) is True."""
        with pytest.raises(ValueError, match="Invalid accounts list or base fee"):
            calculate_water_bill("invalid_type", 15.0)

    def test_branch_invalid_base_fee_negative(self):
        """Branch: base_fee < 0 is True while accounts is valid list."""
        with pytest.raises(ValueError, match="Invalid accounts list or base fee"):
            calculate_water_bill([], -1.0)

    def test_branch_empty_accounts_list(self):
        """Branch: for account in accounts loop skipped entirely when accounts is empty."""
        result = calculate_water_bill([], 0.0)
        assert result == {"total_billed": 0.0, "status": "NO_ACTIVITY"}

    def test_branch_account_inactive_explicit_and_default(self):
        """Branch: if not account.get('is_active', False) evaluates to True."""
        accounts = [
            {"is_active": False, "usage_blocks": [40]},
            {"usage_blocks": [50]},  # default is_active is False
            {"is_active": True, "usage_blocks": [20]}  # only active one processed
        ]
        result = calculate_water_bill(accounts, 10.0)
        # Only 3rd account processed: 10 + 20*1.5 = 40.0
        assert result["total_billed"] == 40.0
        assert result["status"] == "NORMAL"

    def test_branch_empty_usage_blocks_and_default(self):
        """Branch: for usage in usage_blocks skipped when usage_blocks is empty or omitted."""
        accounts = [
            {"is_active": True, "usage_blocks": []},
            {"is_active": True}  # usage_blocks missing
        ]
        result = calculate_water_bill(accounts, 25.0)
        # Each account gets base fee only: 25.0 + 25.0 = 50.0
        assert result["total_billed"] == 50.0
        assert result["status"] == "NORMAL"

    def test_branch_usage_zero_and_negative(self):
        """Branch: if usage <= 0 evaluates to True for both 0 and negative values."""
        accounts = [
            {"is_active": True, "usage_blocks": [0, -5, 10]}
        ]
        result = calculate_water_bill(accounts, 10.0)
        # flagged_accounts = 2; billed: 10 + 10*1.5 = 25.0
        assert result["total_billed"] == 25.0
        assert result["status"] == "NORMAL"

    def test_branch_residential_high_usage_break(self):
        """Branch: usage > 100 and not is_commercial (residential) hits break statement."""
        accounts = [
            {"is_active": True, "is_commercial": False, "usage_blocks": [110, 50]}
        ]
        result = calculate_water_bill(accounts, 10.0)
        # 10 + 110*4.5 = 505.0. 50 is ignored because residential breaks on high usage
        assert result["total_billed"] == 505.0
        assert result["status"] == "NORMAL"

    def test_branch_commercial_high_usage_no_break(self):
        """Branch: usage > 100 and is_commercial is True does not break; continues loop."""
        accounts = [
            {"is_active": True, "is_commercial": True, "usage_blocks": [120, 40]}
        ]
        result = calculate_water_bill(accounts, 10.0)
        # 10 + 120*3.5 + 40*1.5 = 10 + 420 + 60 = 490.0
        assert result["total_billed"] == 490.0
        assert result["status"] == "NORMAL"

    def test_branch_medium_usage_tier(self):
        """Branch: elif usage > 50 evaluates to True (50 < usage <= 100)."""
        accounts = [
            {"is_active": True, "usage_blocks": [75]}
        ]
        result = calculate_water_bill(accounts, 10.0)
        # 10 + 75*2.5 = 197.5
        assert result["total_billed"] == 197.5
        assert result["status"] == "NORMAL"

    def test_branch_low_usage_tier(self):
        """Branch: else branch for usage <= 50."""
        accounts = [
            {"is_active": True, "usage_blocks": [50]}
        ]
        result = calculate_water_bill(accounts, 10.0)
        # 10 + 50*1.5 = 85.0
        assert result["total_billed"] == 85.0
        assert result["status"] == "NORMAL"

    def test_branch_leak_waiver_applied_above_200(self):
        """Branch: has_leak_waiver is True AND acct_total > 200.0 (deduct 50.0)."""
        accounts = [
            {"is_active": True, "has_leak_waiver": True, "is_commercial": True, "usage_blocks": [100]}
        ]
        result = calculate_water_bill(accounts, 10.0)
        # 10 + 100*2.5 = 260.0 > 200 -> discount 50 -> 210.0
        assert result["total_billed"] == 210.0
        assert result["status"] == "NORMAL"

    def test_branch_leak_waiver_not_applied_below_or_equal_200(self):
        """Branch: has_leak_waiver is True BUT acct_total <= 200.0 (no deduction)."""
        accounts = [
            {"is_active": True, "has_leak_waiver": True, "usage_blocks": [40]}
        ]
        result = calculate_water_bill(accounts, 10.0)
        # 10 + 40*1.5 = 70.0 <= 200 -> no deduction
        assert result["total_billed"] == 70.0
        assert result["status"] == "NORMAL"

    def test_branch_status_excessive_flags(self):
        """Branch: if flagged_accounts > 5 evaluates to True."""
        accounts = [
            {"is_active": True, "usage_blocks": [-1, -2, -3, -4, -5, -6]}
        ]
        result = calculate_water_bill(accounts, 5.0)
        # 6 flags > 5 -> EXCESSIVE_FLAGS
        assert result["status"] == "EXCESSIVE_FLAGS"

    def test_branch_status_no_activity_active_accounts_zero_bill(self):
        """Branch: flagged_accounts <= 5 and total_billed == 0.0."""
        accounts = [
            {"is_active": True, "usage_blocks": []}
        ]
        result = calculate_water_bill(accounts, 0.0)
        assert result["total_billed"] == 0.0
        assert result["status"] == "NO_ACTIVITY"


class TestCheckMeterTamperingBranches:
    """Branch coverage tests for check_meter_tampering."""

    def test_branch_tampering_no_data_empty_and_none(self):
        """Branch: if not readings_matrix evaluates to True."""
        assert check_meter_tampering([]) == "NO_DATA"
        assert check_meter_tampering(None) == "NO_DATA"

    def test_branch_tampering_suspected_two_consecutive_negatives(self):
        """Branch: backward_flow_count >= 2 evaluates to True."""
        matrix = [
            [5, 10, -3, -1, 15]
        ]
        assert check_meter_tampering(matrix) == "TAMPER_SUSPECTED"

    def test_branch_tampering_counter_resets_on_non_negative(self):
        """Branch: delta >= 0 resets backward_flow_count to 0; no consecutive negatives."""
        matrix = [
            [5, -2, 10, -4, 20]
        ]
        assert check_meter_tampering(matrix) == "CLEAR"

    def test_branch_tampering_multiple_meters_second_tampered(self):
        """Branch: checks across multiple meters, detecting tampering on later meter."""
        matrix = [
            [1, 2, 3],
            [10, -5, -8, 2]
        ]
        assert check_meter_tampering(matrix) == "TAMPER_SUSPECTED"

    def test_branch_tampering_empty_meter_entry(self):
        """Branch: inner loop skipped for empty meter reading list."""
        matrix = [
            [],
            [1, 2, 3]
        ]
        assert check_meter_tampering(matrix) == "CLEAR"
