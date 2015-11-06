from grail import step
from unittest import TestCase
from utils import validate_method_output


class TestFormatting(TestCase):

    def test_ok_self_in_args(self):
        text_first_index = "This text has index 1 in args"
        validate_method_output(
            self.ok_self_in_args,
            expected_output="PASSED %s" % text_first_index,
            args=(text_first_index,)
        )

    def test_ok_self_not_in_args(self):
        text_zero_index = "This text has index 0 in args"
        validate_method_output(
            self.ok_self_not_in_args,
            expected_output="PASSED ('%s',)" % text_zero_index,
            args=(text_zero_index,)
        )

    def test_error_self_in_args(self):
        text_first_index = "This text has index 1 in args"
        validate_method_output(
            self.error_self_in_args,
            expected_output="PASSED {}",
            args=(text_first_index,)
        )

    def test_error_self_not_in_args(self):
        text_zero_index = "This text has index 0 in args"
        validate_method_output(
            self.error_self_not_in_args,
            expected_output="PASSED test_error_self_not_in_args (test_description_formatting.TestFormatting)",
            args=(text_zero_index,)
        )

    @step(description='{1}', format_description=True, clean_params=False)
    def ok_self_in_args(self, test_text):
        pass

    @step(description='{0}', format_description=True, clean_params=True)
    def ok_self_not_in_args(self, test_text):
        pass

    @step(description='{1}', format_description=True, clean_params=True)
    def error_self_in_args(self, test_text):
        pass

    @step(description='{0}', format_description=True, clean_params=False)
    def error_self_not_in_args(self, test_text):
        pass
