import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

# The two starter tests are retained.
def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0


def test_clean_record():
    assert license_action(2, False, False) == "none"


def test_speed_limit_boundary():
    assert speeding_fine(59, 60, "city") == 0
    assert speeding_fine(60, 60, "city") == 0
    assert speeding_fine(61, 60, "city") == 500


def test_zone_selection():
    assert speeding_fine(61, 60, "school") == 2000
    assert speeding_fine(61, 60, "highway") == 1000
    assert speeding_fine(61, 60, "city") == 500
    assert speeding_fine(61, 60, "unknown") == 500


def test_excess_speed_tier_boundaries():
    # The doubled tier begins above 20; the tripled tier begins above 40.
    assert speeding_fine(80, 60, "city") == 500  # excess 20
    assert speeding_fine(81, 60, "city") == 1000  # excess 21
    assert speeding_fine(100, 60, "city") == 1000  # excess 40
    assert speeding_fine(101, 60, "city") == 1500  # excess 41


def test_school_and_highway_tiers():
    assert speeding_fine(81, 60, "school") == 4000
    assert speeding_fine(101, 60, "school") == 6000
    assert speeding_fine(81, 60, "highway") == 2000
    assert speeding_fine(101, 60, "highway") == 3000


def test_license_twelve_point_boundary_and_commercial_action():
    assert license_action(11, True, False) == "warning"
    assert license_action(12, True, False) == "revoke"
    assert license_action(13, True, True) == "revoke"
    assert license_action(12, False, False) == "suspend"


def test_license_eight_point_boundary_and_repeat_action():
    assert license_action(7, False, False) == "notice"
    assert license_action(8, False, True) == "suspend"
    assert license_action(9, False, True) == "suspend"
    assert license_action(8, False, False) == "warning"


def test_license_four_point_boundary():
    assert license_action(3, False, False) == "none"
    assert license_action(4, False, False) == "notice"
    assert license_action(5, False, True) == "notice"


def test_totals_under_at_and_over_cap():
    assert total_penalty([100, 250, 50]) == 400
    assert total_penalty([10000]) == 10000
    assert total_penalty([6000, 5000]) == 10000


def test_empty_total():
    assert total_penalty([]) == 0


def test_negative_fine_is_rejected():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([100, -1])
