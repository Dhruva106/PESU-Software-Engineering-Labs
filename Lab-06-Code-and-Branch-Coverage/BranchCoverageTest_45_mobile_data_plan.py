
import pytest

from mobile_data_plan import (
    overage_charge,
    recharge_allowed,
    validity_status
)


# ==========================================
# OVERAGE CHARGE — BRANCH COVERAGE
# ==========================================

def test_unknown_plan_branch():
    with pytest.raises(ValueError):
        overage_charge("gold", 5, False, False)


def test_valid_plan_branch():
    assert overage_charge("basic", 2, False, False) == 0


def test_negative_data_branch():
    with pytest.raises(ValueError):
        overage_charge("basic", -1, False, False)


def test_non_negative_data_branch():
    assert overage_charge("basic", 2, False, False) == 0


def test_loyal_non_premium_branch():
    assert overage_charge("standard", 7, False, True) == 15


def test_non_loyal_branch():
    assert overage_charge("standard", 6, False, False) == 15


def test_loyal_premium_branch():
    assert overage_charge("premium", 11, False, True) == 15


def test_extra_data_zero_branch():
    assert overage_charge("standard", 5, False, False) == 0


def test_extra_data_positive_branch():
    assert overage_charge("basic", 3, False, False) == 15


def test_roaming_rate_branch():
    assert overage_charge("basic", 3, True, False) == 40


def test_non_roaming_rate_branch():
    assert overage_charge("basic", 3, False, False) == 15


def test_extra_above_ten_branch():
    assert overage_charge("standard", 16, False, False) == 275


def test_extra_not_above_ten_branch():
    assert overage_charge("standard", 10, False, False) == 75


def test_large_roaming_overage_branch():
    assert overage_charge("basic", 13, True, False) == 605


def test_large_non_roaming_overage_branch():
   assert overage_charge("basic", 13, False, False) == 275


# ==========================================
# RECHARGE ALLOWED — BRANCH COVERAGE
# ==========================================

def test_kyc_pending_true_branch():
    assert recharge_allowed(200, 5, True) is True


def test_kyc_pending_false_amount_branch():
    assert recharge_allowed(201, 1, True) is False


def test_kyc_not_pending_branch():
    assert recharge_allowed(500, 1, False) is True


def test_amount_above_2000_branch():
    assert recharge_allowed(2001, 1, False) is False


def test_amount_not_above_2000_branch():
    assert recharge_allowed(2000, 1, False) is True


def test_pending_recharges_within_limit_branch():
    assert recharge_allowed(500, 2, False) is True


def test_pending_recharges_exceed_limit_branch():
    assert recharge_allowed(500, 3, False) is False


# ==========================================
# VALIDITY STATUS — BRANCH COVERAGE
# ==========================================

def test_prepaid_branch():
    assert validity_status(0, True, False) == "active"


def test_postpaid_branch():
    assert validity_status(3, False, False) == "active"


def test_addon_enabled_branch():
    assert validity_status(2, True, True) == "active"


def test_addon_disabled_branch():
    assert validity_status(0, True, False) == "active"


def test_active_status_branch():
    assert validity_status(3, False, False) == "active"


def test_grace_status_branch():
    assert validity_status(2, False, False) == "grace"


def test_expired_status_branch():
    assert validity_status(-13, False, False) == "expired"


def test_prepaid_grace_boundary_branch():
    assert validity_status(-15, True, False) == "grace"


def test_prepaid_expired_branch():
    assert validity_status(-16, True, False) == "expired"
