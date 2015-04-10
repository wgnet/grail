from grail import BaseTest, step


class MyDisableLogOutputTest(BaseTest):
    def test_some_feature(self):
        self.log_output()
        self.do_not_log_output()

    @step
    def log_output(self):
        return 'Important output'

    @step(log_output=False)
    def do_not_log_output(self):
        return 'Some invisible in logs data'


class MyDisableLogInputTest(BaseTest):
    def test_some_feature(self):
        self.log_input('input data')
        self.do_not_log_input('input data')

    @step
    def log_input(self, input_data):
        pass

    @step(log_input=False)
    def do_not_log_input(self, input_data):
        pass
