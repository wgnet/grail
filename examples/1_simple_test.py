from grail import BaseTest, step


class MyFirstGrailTest(BaseTest):
    def test_some_feature(self):
        self.login_to_application()

    @step
    def login_to_application(self):
        pass
