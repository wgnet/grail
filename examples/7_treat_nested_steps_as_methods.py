from grail import BaseTest, step


class DoItInVerySpecialCases(BaseTest):
    def test_its_not_recommended_to_do_this(self):
        self.external_step()

    @step(treat_nested_steps_as_methods=True)
    def external_step(self):
        self.this_is_not_a_step_anymore()

    @step
    def this_is_not_a_step_anymore(self):
        pass
