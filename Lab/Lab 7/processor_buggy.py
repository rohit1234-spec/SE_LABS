"""Buggy / Vulnerable Water Billing Processor (Unvalidated Input)."""

def sanitize_meter_id(meter_id):
    # Buggy: Lacks NoneType and type check; crashes with AttributeError when meter_id is None
    meter_id = meter_id.strip()
    for ch in ['!', '@', '#', '$', '%']:
        meter_id = meter_id.replace(ch, '')
    return meter_id.upper()


def parse_consumption_readings(readings_csv):
    # Buggy: Lacks NoneType / non-numeric handling; crashes on ValueError
    readings = readings_csv.split(',')
    return [int(r.strip()) for r in readings]


def format_billing_summary(account_record):
    # Buggy: Assumes colon-separated string with exactly 3 fields and numeric usage
    parts = account_record.split(':')
    customer_name = parts[0].strip()
    units = int(parts[1].strip())
    zone = parts[2].strip()
    return f"Customer {customer_name} billed {units * 2} USD in {zone}"


if __name__ == "__main__":
    print(sanitize_meter_id("@meter_01!"))
    print(parse_consumption_readings("10, 20, 30"))
    print(format_billing_summary("Alice:50:NorthZone"))
