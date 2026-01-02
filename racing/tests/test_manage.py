import os
import sys
import pytest
from unittest import mock
 
import manage
 
 
def test_main_sets_django_settings_module(monkeypatch):
    monkeypatch.delenv("DJANGO_SETTINGS_MODULE", raising=False)
 
    with mock.patch("django.core.management.execute_from_command_line"):
        manage.main()
 
    assert os.environ["DJANGO_SETTINGS_MODULE"] == "backend.settings"
 
 
def test_main_calls_execute_from_command_line():
    with mock.patch(
        "django.core.management.execute_from_command_line"
    ) as mock_execute:
        manage.main()
        mock_execute.assert_called_once_with(sys.argv)
 
 
def test_import_error_raises_proper_exception(monkeypatch):
    # Simulate ImportError when importing django
    monkeypatch.setitem(sys.modules, "django.core.management", None)
 
    with pytest.raises(ImportError):
        manage.main()
 