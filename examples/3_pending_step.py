from grail import BaseTest, step


class MyNotFinishedTest(BaseTest):
    def test_some_feature(self):
        self.first_implemented_step()
        self.second_pending_step()
        self.some_third_step()

    @step
    def first_implemented_step(self):
        print 'Some implemented actions'

    @step(pending=True)
    def second_pending_step(self):
        print 'This is not final implementation'

    @step
    def some_third_step(self):
        print 'This step is implemented but will be Ignored and you will not see this message'
