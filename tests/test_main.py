from main import start
from utils.mailer import Mailer
from tests.helpers import *

def test_notify(mocked_object):

    start(my_rules)

    mocked_object.mail_mock.assert_called_once()
    mocked_object.notify_new_emails_mock.assert_called_once()
    mocked_object.notify_new_emails_mock.assert_called_once_with(mail_obj, my_rules[0].LINE_TOKEN)
    mocked_object.line_mock.assert_not_called()
