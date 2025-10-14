from gen_common.graph.io.state_var import StateVar
from gen_common_test.base.tests.base_test import BaseTest


class TestStateVar(BaseTest):
    STATE_VAR = StateVar("var")

    def test_is(self):
        condition = self.STATE_VAR.is_(None)
        state = dict(var=None)
        self.assertTrue(condition.check(state))
        state = dict(var="hello")
        self.assertFalse(condition.check(state))

        condition = self.STATE_VAR.is_(True)
        state = dict(var=True)
        self.assertTrue(condition.check(state))
        state = dict(var=False)
        self.assertFalse(condition.check(state))

    def test_contains(self):
        condition = self.STATE_VAR.contains(1)
        state = dict(var={1: "test"})
        self.assertTrue(condition.check(state))
        state = dict(var={})
        self.assertFalse(condition.check(state))

    def test_length_and_geq(self):
        condition = self.STATE_VAR.length() >= 1
        state = dict(var=[1])
        self.assertTrue(condition.check(state))
        state = dict(var=[])
        self.assertFalse(condition.check(state))

    def test_length_and_gt(self):
        condition = self.STATE_VAR > 1
        state = dict(var=2)
        self.assertTrue(condition.check(state))
        state = dict(var=1)
        self.assertFalse(condition.check(state))

    def test_length_and_lt(self):
        condition = self.STATE_VAR < 2
        state = dict(var=1)
        self.assertTrue(condition.check(state))
        state = dict(var=2)
        self.assertFalse(condition.check(state))

    def test_length_and_lt2(self):
        condition = self.STATE_VAR <= 2
        state = dict(var=2)
        self.assertTrue(condition.check(state))
        state = dict(var=3)
        self.assertFalse(condition.check(state))

    def test_eq(self):
        condition = self.STATE_VAR == "hello"
        state = dict(var="hello")
        self.assertTrue(condition.check(state))
        state = dict(var="bye")
        self.assertFalse(condition.check(state))

    def test_neq(self):
        condition = self.STATE_VAR != "bye"
        state = dict(var="hello")
        self.assertTrue(condition.check(state))
        state = dict(var="bye")
        self.assertFalse(condition.check(state))

    def test_not(self):
        condition = ~ self.STATE_VAR
        state = dict(var=False)
        self.assertTrue(condition.check(state))
        state = dict(var=True)
        self.assertFalse(condition.check(state))

    def test_is_instance(self):
        condition = self.STATE_VAR.is_instance(str)
        state = dict(var="hello")
        self.assertTrue(condition.check(state))
        state = dict(var=2)
        self.assertFalse(condition.check(state))

    def test_exists(self):
        condition = self.STATE_VAR.exists()
        state = dict(var=["hello"])
        self.assertTrue(condition.check(state))
        state = dict(var=2)
        self.assertTrue(condition.check(state))
        state = dict(var=None)
        self.assertFalse(condition.check(state))
        state = dict(var=[])
        self.assertFalse(condition.check(state))
