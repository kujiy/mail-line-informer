import json
from unittest.mock import Mock
from requests.models import Response

from env import env
from plugins.line import LINE
from utils.mailer import Mailer
import pytest

from env import env
from models import RuleModel

my_rules = [
    RuleModel(mailbox="school-pass", LINE_TOKEN=""),
]


class MockMailObj:
    title = 'test'
    body = 'test'
    attachments = []

class MockWebDriver:
    def __enter__(self):
        return self
    def __exit__(self, exception_type, exception_value, traceback):
        pass

line_response = Mock(spec=Response)
line_response.json.return_value = {'status': 'ok'}
line_response.status_code = 200

mail_obj = MockMailObj()


@pytest.fixture(autouse=True)
def mocked_object(mocker):
    class MockObject(object):
        mail_connect_mock = mocker.patch.object(Mailer, 'connect', return_value=True)
        mail_mock = mocker.patch.object(Mailer, 'get', return_value=[mail_obj])
        mail_change_mailbox_mock = mocker.patch.object(Mailer, 'change_mailbox')
        notify_new_emails_mock = mocker.patch('main.notify_new_emails', return_value=True)
        # send_reply_mock = mocker.patch('main.send_reply', return_value=ReplyModel(text='sent',stamp='stamp'))
        line_mock = mocker.patch('plugins.line.requests.post', return_value=line_response)
        # retrieve_byte_image_mock = mocker.patch.object(Line, 'retrieve_byte_image', return_value=b'abc')
    return MockObject()

