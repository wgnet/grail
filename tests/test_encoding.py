# coding=utf-8
from unittest import TestCase
from nose.tools import eq_
from grail import step, BaseTest
from tests.utils import validate_method_output

korean_string = '올'
russian_string = 'д'


class TestEncoding(TestCase):
    def test_localization_exception(self):
        validate_method_output(self.verify_step, u'PASSED verify step (\ufffd\ufffd\ufffd, \ufffd\ufffd)\n'
                                                 u'  \ufffd\ufffd\ufffd\ufffd\ufffd',
                               args=(korean_string, russian_string))

    @step
    def verify_step(self, korean_text, russian_text):
        print korean_text, russian_text

    class TestObjectFailed(BaseTest):
        to_raise = Exception(korean_string)

        def test_failed(self):
            self.failed_step()

        @step
        def failed_step(self):
            raise self.to_raise

    def test_raising(self):
        try:
            self.TestObjectFailed('test_failed').test_failed()
        except Exception as inst:
            eq_(inst, self.TestObjectFailed.to_raise)

    @step
    def eq_dict(self, a, b):
        eq_(a, b)

    def test_dict_params(self):
        validate_method_output(self.eq_dict, u'PASSED eq dict ({}, {})', args=({}, {}))
