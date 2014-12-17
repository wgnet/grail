from unittest import TestCase
from grail import step
from grail.base_test import BaseTest
from tests.utils import validate_method_output


class TestPassed(TestCase):

    class TestObjectPassed(BaseTest):
        def test_passed(self):
            self.passed_step()

        @step
        def passed_step(self):
            pass

    def test_passed(self):
        validate_method_output(self.TestObjectPassed('test_passed').test_passed, 'PASSED passed step')