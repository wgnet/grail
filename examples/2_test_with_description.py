from grail import BaseTest, step


class MyTestWithDescription(BaseTest):
    def test_some_feature(self):
        self.login_to_application()
        self.complex_step()

    @step
    def login_to_application(self):
        pass

    @step(description='Some tricky actions with the application which I can\'t put to method name')
    def complex_step(self):
        pass
