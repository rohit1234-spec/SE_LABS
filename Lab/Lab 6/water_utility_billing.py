"""Water Utility Billing & Tamper Detection Module."""

def calculate_water_bill(accounts, base_fee):
    """Calculate total billed amount and operational status across customer accounts."""
    if not isinstance(accounts, list) or base_fee < 0:
        raise ValueError("Invalid accounts list or base fee")

    total_billed = 0.0
    flagged_accounts = 0

    for account in accounts:
        if not account.get('is_active', False):
            continue

        acct_total = base_fee
        usage_blocks = account.get('usage_blocks', [])

        for usage in usage_blocks:
            if usage <= 0:
                flagged_accounts += 1
                continue

            if usage > 100:
                if not account.get('is_commercial', False):
                    acct_total += usage * 4.5
                    break
                else:
                    acct_total += usage * 3.5
            elif usage > 50:
                acct_total += usage * 2.5
            else:
                acct_total += usage * 1.5

        if account.get('has_leak_waiver', False) and acct_total > 200.0:
            acct_total -= 50.0

        total_billed += acct_total

    if flagged_accounts > 5:
        status = "EXCESSIVE_FLAGS"
    elif total_billed == 0.0:
        status = "NO_ACTIVITY"
    else:
        status = "NORMAL"

    return {"total_billed": total_billed, "status": status}


def check_meter_tampering(readings_matrix):
    """Analyze meter reading delta matrix to detect potential reverse-flow tampering."""
    if not readings_matrix:
        return "NO_DATA"

    for meter in readings_matrix:
        backward_flow_count = 0
        for delta in meter:
            if delta < 0:
                backward_flow_count += 1
                if backward_flow_count >= 2:
                    return "TAMPER_SUSPECTED"
            else:
                backward_flow_count = 0

    return "CLEAR"
