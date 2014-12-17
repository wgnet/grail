from grail import BaseTest, step


class SomeClassWithSteps(object):
    @step
    def step_from_another_class(self):
        pass


@step
def some_simple_action_one():
    pass


class MyTestWithGroup(BaseTest):
    external_steps = SomeClassWithSteps()

    def test_some_feature(self):
        self.complex_step_based_on_other_steps()

    @step(step_group=True)
    def complex_step_based_on_other_steps(self):
        self.external_steps.step_from_another_class()
        some_simple_action_one()
        self.external_steps.step_from_another_class()
