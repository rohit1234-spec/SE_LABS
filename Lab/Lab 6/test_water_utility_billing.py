"""Unified test suite runner for Water Utility Billing."""
from BranchCoverageTest_water_utility_billing import *
from CodeCoverageTest_water_utility_billing import *

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", __file__])
