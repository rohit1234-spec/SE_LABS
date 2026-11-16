import pytest
from water_utility_billing import calculate_water_bill, check_meter_tampering


def test_invalid_accounts_type():
    """Test that non-list accounts parameter raises ValueError."""
    with pytest.raises(ValueError, match="Invalid accounts list or base fee"):
        calculate_water_bill("not-a-list", 10.0)


def test_invalid_base_fee():
    """Test that negative base_fee raises ValueError."""
    with pytest.raises(ValueError, match="Invalid accounts list or base fee"):
        calculate_water_bill([], -5.0)


def test_empty_accounts_list():
    """Test empty accounts list with zero base fee results in NO_ACTIVITY."""
    result = calculate_water_bill([], 0.0)
    assert result == {"total_billed": 0.0, "status": "NO_ACTIVITY"}


def test_inactive_account_skipped():
    """Test that inactive accounts are skipped."""
    accounts = [
        {"is_active": False, "usage_blocks": [50]},
        {"is_active": True, "usage_blocks": [20]}
    ]
    result = calculate_water_bill(accounts, 10.0)
    # Only second account billed: 10 + 20*1.5 = 40.0
    assert result["total_billed"] == 40.0
    assert result["status"] == "NORMAL"


def test_usage_zero_and_negative_flagged():
    """Test that zero and negative usage blocks are flagged and skipped."""
    accounts = [
        {"is_active": True, "usage_blocks": [0, -15, 20]}
    ]
    result = calculate_water_bill(accounts, 10.0)
    # 10 + 20 * 1.5 = 40.0
    assert result["total_billed"] == 40.0
    assert result["status"] == "NORMAL"


def test_residential_high_usage_break():
    """Test residential account with usage > 100 applies 4.5 rate and breaks loop."""
    accounts = [
        {"is_active": True, "is_commercial": False, "usage_blocks": [120, 30]}
    ]
    result = calculate_water_bill(accounts, 15.0)
    # 15 + 120 * 4.5 = 555.0 (second block 30 skipped due to break)
    assert result["total_billed"] == 555.0
    assert result["status"] == "NORMAL"


def test_commercial_high_usage_and_medium_usage():
    """Test commercial account with high usage (>100) and medium usage (>50)."""
    accounts = [
        {"is_active": True, "is_commercial": True, "usage_blocks": [110, 60, 20]}
    ]
    result = calculate_water_bill(accounts, 10.0)
    # 10 + 110*3.5 + 60*2.5 + 20*1.5 = 10 + 385 + 150 + 30 = 575.0
    assert result["total_billed"] == 575.0
    assert result["status"] == "NORMAL"


def test_leak_waiver_applied():
    """Test leak waiver deduction when acct_total > 200."""
    accounts = [
        {"is_active": True, "has_leak_waiver": True, "is_commercial": True, "usage_blocks": [100]}
    ]
    result = calculate_water_bill(accounts, 10.0)
    # 10 + 100*2.5 = 260.0. > 200, so discount 50 -> 210.0
    assert result["total_billed"] == 210.0
    assert result["status"] == "NORMAL"


def test_leak_waiver_not_applied_under_threshold():
    """Test leak waiver not applied when acct_total <= 200."""
    accounts = [
        {"is_active": True, "has_leak_waiver": True, "usage_blocks": [30]}
    ]
    result = calculate_water_bill(accounts, 10.0)
    # 10 + 30*1.5 = 55.0 (<= 200, no discount)
    assert result["total_billed"] == 55.0
    assert result["status"] == "NORMAL"


def test_excessive_flags_status():
    """Test status is EXCESSIVE_FLAGS when flagged_accounts > 5."""
    accounts = [
        {"is_active": True, "usage_blocks": [-1, -2, -3, -4, -5, -6, 10]}
    ]
    result = calculate_water_bill(accounts, 5.0)
    assert result["status"] == "EXCESSIVE_FLAGS"


def test_check_meter_tampering_no_data():
    """Test check_meter_tampering with empty or None readings."""
    assert check_meter_tampering([]) == "NO_DATA"
    assert check_meter_tampering(None) == "NO_DATA"


def test_check_meter_tampering_suspected():
    """Test check_meter_tampering detects consecutive negative readings."""
    matrix = [
        [10, 15, -2, -4, 20]
    ]
    assert check_meter_tampering(matrix) == "TAMPER_SUSPECTED"


def test_check_meter_tampering_clear():
    """Test check_meter_tampering returns CLEAR when no consecutive negative readings occur."""
    matrix = [
        [10, -3, 15, -2, 20],
        [5, 10, 12]
    ]
    assert check_meter_tampering(matrix) == "CLEAR"
