=====
Grail
=====
About
-----
Grail is a library which allows test script creation based on steps.

Library usage brings the following benefits to your tests:

- strict separation test logic from test implementation

- you don't need separate test cases as a documentation for your tests, it will be generated from the code

- separate logging is not required, test execution is automatically logged

- test script creation is easy for people with basic programming skills

- step implementation can be done separately

Basic Usage
-----------
| ``@step`` is a basic concept of Grail library. It's decorator which transforms method or function to step.
| If you want to use steps your test classes should inherit ``BaseTest``.
| When you are doing your tests based on Grail all your test logic should be covered with steps.

The simple test demonstrating basic usage:

.. code:: python

  from grail import BaseTest, step


  class MyFirstGrailTest(BaseTest):
      def test_some_feature(self):
          self.login_to_application()

      @step
      def login_to_application(self):
          pass

Such test output will be:

``PASSED login to application``

Logging parameters and output
-----------------------------
When step method takes some params or return value: all the information will be logged.

Example:

.. code:: python

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

Output will contain all execution details:

| ``PASSED do some calculation (2, second_param=3) -> 5``
| ``PASSED verify result (5)``

@step options
-------------
description
```````````
By default step name is method name split by underscores. In the majority of cases it's enough if you are writing readable code.
But there are situations where step description is not so easy to put into method name.
For such cases there is a ``description`` parameter.

.. code:: python

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

Such test script will generate the following:

| ``PASSED login to application``
| ``PASSED Some tricky actions with the application which I can't put to method name``

pending
```````
If step method is created but not implemented you can specify ``pending`` property. It will fail corresponding test execution but
at the same time you can have full test case description (e.g. for manual execution).

Example:

.. code:: python

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

Test execution output:

| ``PASSED first implemented step``
|   ``Some implemented actions``
| ``PENDING second pending step``
| ``IGNORED some third step``
|
| ``Error``
| ``Traceback (most recent call last):``
|   ``File "/home/i_khrol/PyCharm/grail/grail/base_test.py", line 30, in wrapper``
|     ``raise Exception('Test is failed as there are pending steps')``
| ``Exception: Test is failed as there are pending steps``

step_group
``````````
| If you want to call one step from another you should use ``step_group``. It's special step which is a set of other steps.
| *Important*: Like test itself step group should be based only on steps.

Example below also shows that there is no limitation where you should store your steps.
It could be any class method, function. You can also call the same step multiple times.

.. code:: python

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

The output:

| ``PASSED complex step based on other steps``
|  ``PASSED step from another class``
|  ``PASSED some simple action one``
|  ``PASSED step from another class``

format_description
``````````````````
There are cases when you want to format your step description special way:

- skip some parameters in logging

- put some values in the middle of the message

If you want to do this you should set ``format_description=True``.
In this case ``description.format(*args, **kwargs)`` will be used as step description.

.. code:: python

  from grail import BaseTest, step


  class MyVeryFormattedTest(BaseTest):
      def test_some_feature(self):
          self.some_tricky_formatting('value', kwarg_to_format='kw_value', skip_this=100500)

      @step(description='Some info: {0}, another info: {kwarg_to_format}', format_description=True)
      def some_tricky_formatting(self, arg_to_format, kwarg_to_format, skip_this):
          print arg_to_format
          print kwarg_to_format
          print skip_this

Output will be like this:

| ``PASSED Some info: value, another info: kw_value``
|  ``value``
|  ``kw_value``
|  ``100500``

treat_nested_steps_as_methods
`````````````````````````````
It's forbidden to call steps from each other if it's not step group.
But if you *really* need it you can tell caller to ignore ``@step`` functionality within itself.

.. code:: python

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

Output will not contain description for the internal step:

| ``PASSED external step``

log_output
``````````
There are cases when method output is too huge or it not interested in logging at all. You can switch off output logging for step.

.. code:: python

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

Output:

| ``PASSED log output -> Important output``
| ``PASSED do not log output``

log_input
`````````
You can also switch off input logging for step.

.. code:: python

  from grail import BaseTest, step


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

Output:

| ``PASSED log input (input data)``
| ``PASSED do not log input``

Export Mode
-----------
Regular test automation process assumes some manual test cases that should be automated.
With Grail you can do vise versa - write code and get manual test cases.
In order to generate test description from the code you should set ``grail.settings.export_mode=True``.
With this setting tests will be executed but steps' internal will not be called.
So you can have your test description when your scripts are not implemented yet or
automated test execution is blocked due to any other reasons.

Important things to keep in mind
````````````````````````````````

In ``export_mode`` only ``setUp`` and tests are executed. All the fixtures are skipped.
It's important to have your ``setUp`` and tests be implemented fully with ``@step``-annotated methods and functions.
For other fixtures it's up-to-you to use steps or not.

All ``@step`` features are enabled during export.

Empty params are not included to step description in ``export_mode``.

Example
```````

This test output could be used as manual test case. E.g. you can store it in your favorite test management system.

.. code:: python

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

Output which can be used as manual test case:

| ``login to application``
| ``one more step (Step input 1)``
| ``Some step that will be implemented``
| ``step group``
|   ``one more step (Step input 2)``
|   ``one more step``
