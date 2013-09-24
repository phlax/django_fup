import os
import sys

sys.path.append(
    os.path.normpath(
        os.path.join(
            os.getcwd(), os.path.dirname(__file__), '../..')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'file_uploads.testing.settings'
from django.test.simple import DjangoTestSuiteRunner

tr = DjangoTestSuiteRunner(verbosity=1)
failures = tr.run_tests(['file_uploads'])
if failures:
    sys.exit(failures)
