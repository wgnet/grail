from grail import BaseTest, step


class MyVeryFormattedTest(BaseTest):
    def test_some_feature(self):
        self.some_tricky_formatting('value', kwarg_to_format='kw_value', skip_this=100500)

    @step(description='Some info: {0}, another info: {kwarg_to_format}', format_description=True)
    def some_tricky_formatting(self, arg_to_format, kwarg_to_format, skip_this):
        print arg_to_format
        print kwarg_to_format
        print skip_this
