from common_resources.graph.io.state_var import StateVar
from common_resources_test.base_tests.base_test import BaseTest


class TestCondition(BaseTest):
    STATE_VAR = StateVar("var")

    def test_and(self):
        condition1 = self.STATE_VAR > 1
        condition2 = self.STATE_VAR < 3
        condition = condition1 & condition2
        state = dict(var=2)
        self.assertTrue(condition.check(state))
        state = dict(var=1)
        self.assertFalse(condition.check(state))
        state = dict(var=3)
        self.assertFalse(condition.check(state))

    def test_or(self):
        condition1 = self.STATE_VAR > 1
        condition2 = self.STATE_VAR == 4
        condition = condition1 | condition2
        state = dict(var=2)
        self.assertTrue(condition.check(state))
        state = dict(var=4)
        self.assertTrue(condition.check(state))
        state = dict(var=1)
        self.assertFalse(condition.check(state))

    def test_not(self):
        condition = ~ (self.STATE_VAR == "hello")
        state = dict(var="bye")
        self.assertTrue(condition.check(state))
        state = dict(var="hello")
        self.assertFalse(condition.check(state))
