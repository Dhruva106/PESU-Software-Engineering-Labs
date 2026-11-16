
import pytest

from mobile_data_plan import (
    overage_charge,
    recharge_allowed,
    validity_status
)


# ==========================================
# OVERAGE CHARGE TEST CASES
# ==========================================

def test_unknown_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", 5, False, False)


def test_negative_data_usage():
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)


def test_usage_within_included_data():
    assert overage_charge("standard", 5, False, False) == 0


def test_loyal_customer_bonus():
    assert overage_charge("standard", 7, False, True) == 15


def test_premium_plan_does_not_get_loyalty_bonus():
    assert overage_charge("premium", 11, False, True) == 15


def test_non_roaming_regular_overage():
    assert overage_charge("basic", 3, False, False) == 15


def test_roaming_regular_overage():
    assert overage_charge("basic", 3, True, False) == 40


def test_non_roaming_overage_above_10_gb():
    assert overage_charge("standard", 16, False, False) == 275


def test_roaming_overage_above_10_gb():
    assert overage_charge("basic", 13, True, False) == 605


# ==========================================
# RECHARGE ALLOWED TEST CASES
# ==========================================

def test_kyc_pending_allowed_amount():
    assert recharge_allowed(200, 5, True) is True


def test_kyc_pending_rejects_high_amount():
    assert recharge_allowed(201, 1, True) is False


def test_reject_amount_above_2000():
    assert recharge_allowed(2001, 1, False) is False


def test_normal_recharge_with_two_pending():
    assert recharge_allowed(2000, 2, False) is True


def test_reject_more_than_two_pending_recharges():
    assert recharge_allowed(500, 3, False) is False


# ==========================================
# VALIDITY STATUS TEST CASES
# ==========================================

def test_prepaid_active():
    assert validity_status(0, True, False) == "active"


def test_prepaid_grace():
    assert validity_status(-1, True, False) == "grace"


def test_prepaid_grace_boundary():
    assert validity_status(-15, True, False) == "grace"


def test_prepaid_expired():
    assert validity_status(-16, True, False) == "expired"


def test_postpaid_active():
    assert validity_status(3, False, False) == "active"


def test_postpaid_grace():
    assert validity_status(2, False, False) == "grace"


def test_postpaid_expired():
    assert validity_status(-13, False, False) == "expired"


def test_prepaid_with_addon():
    assert validity_status(2, True, True) == "active"


def test_postpaid_with_addon():
    assert validity_status(5, False, True) == "active"
