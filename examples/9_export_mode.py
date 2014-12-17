from grail import BaseTest, step
import grail.settings

grail.settings.export_mode = True


class MyTestForExport(BaseTest):
    def test_some_feature(self):
        self.login_to_application()
        self.one_more_step('Step input 1')
        self.pending_step()
        self.step_group()

    @step
    def login_to_application(self):
        pass

    @step
    def one_more_step(self, step_input):
        print 'You will not see next line print'
        print step_input

    @step(description='Some step that will be implemented')
    def pending_step(self):
        pass

    @step(step_group=True)
    def step_group(self):
        self.one_more_step('Step input 2')
        self.one_more_step(None)
