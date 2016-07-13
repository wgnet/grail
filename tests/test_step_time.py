import time
from unittest import TestCase

import grail
from grail import step
from tests.utils import validate_method_output


class TestStepTime(TestCase):
    def setUp(self):
        grail.settings.print_step_time = True

    @step
    def some_step(self):
        time.sleep(0.5)

    def test_step_time(self):
        validate_method_output(self.some_step, '[0.50s] PASSED some step')

    def tearDown(self):
        grail.settings.print_step_time = False
