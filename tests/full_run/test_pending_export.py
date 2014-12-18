import grail.settings
from unittest import TestCase
from grail import step
from grail.base_test import BaseTest
from tests.utils import validate_method_output


class TestPendingExport(TestCase):

    class TestObjectPendingExport(BaseTest):
        def test_pending_export(self):
            self.pending_step()

        @step(pending=True)
        def pending_step(self):
            pass

    def setUp(self):
        grail.settings.export_mode = True

    def tearDown(self):
        grail.settings.export_mode = False

    def test_pending_export(self):
        validate_method_output(self.TestObjectPendingExport('test_pending_export').test_pending_export, 'pending step')
