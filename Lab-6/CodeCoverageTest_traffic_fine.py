import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

# The two starter tests are retained.
def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0


def test_clean_record():
    assert license_action(2, False, False) == "none"


def test_speeding_zone_base_fines():
    assert speeding_fine(61, 60, "city") == 500
    assert speeding_fine(61, 60, "school") == 2000
    assert speeding_fine(61, 60, "highway") == 1000


def test_speeding_increased_fines():
    assert speeding_fine(81, 60, "city") == 1000
    assert speeding_fine(101, 60, "school") == 6000


def test_license_actions():
    assert license_action(12, True, False) == "revoke"
    assert license_action(12, False, True) == "suspend"
    assert license_action(8, False, True) == "suspend"
    assert license_action(8, False, False) == "warning"
    assert license_action(4, False, False) == "notice"


def test_totals_and_cap():
    assert total_penalty([100, 250, 50]) == 400
    assert total_penalty([6000, 5000]) == 10000


def test_empty_total():
    assert total_penalty([]) == 0


def test_negative_fine_is_rejected():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([100, -1])
