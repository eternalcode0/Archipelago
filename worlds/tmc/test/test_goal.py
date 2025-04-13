from . import MinishCapTestBase


class TestVaati(MinishCapTestBase):
    options = {
        "goal_vaati": True,
    }

    def test_goal(self) -> None:
        """Test some different states to verify goal requires the correct items"""
        self.collect_all_but(["Big Key (DHC)", "Victory"])
        self.assertEqual(self.can_reach_location("DHC B1 Big Chest"), True)
        self.assertBeatable(False)
        self.collect_by_name(["Big Key (DHC)"])
        self.assertBeatable(True)

class TestPedestal(MinishCapTestBase):
    options = {
        "goal_vaati": False,
        "shuffle_elements": True,
    }

    def test_goal(self) -> None:
        """Test whether Pedestal is only accessible once all elements are obtained"""
        self.collect_by_name(["Earth Element", "Fire Element", "Water Element"])
        self.assertBeatable(False)
        self.collect_by_name("Wind Element")
        self.assertBeatable(True)
