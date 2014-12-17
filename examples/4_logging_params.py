from grail import BaseTest, step
from nose.tools import eq_


class MyLoggingParametersAndOutputTest(BaseTest):
    def test_some_feature(self):
        result = self.do_some_calculation(2, second_param=3)
        self.verify_result(result)

    @step
    def do_some_calculation(self, first_param, second_param):
        return first_param + second_param

    @step
    def verify_result(self, actual_data):
        eq_(actual_data, 5)
