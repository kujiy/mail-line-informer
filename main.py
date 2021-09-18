import datetime
import os
import sys
import re
import traceback
from importlib import import_module
from typing import List
from my_rules import my_rules
from pydantic import BaseModel

from env import env
from models import RuleModel
from plugins.line import LINE
from utils.easyimap import MailObj
from utils.mailer import Mailer
from utils.logger import logger

# TODO: plugin式にする
# class Plugins:
#     pass
# plugins = Plugins()
#
# # dynamic import plug-ins
# files = os.listdir("./plugins")
# for file in files:
#     mod_name = file[:-3]  # strip .py at the end
#     if not re.match(r'^__', file):
#         plugin = getattr(import_module(f'.{mod_name}'), mod_name.upper())
#         setattr(plugins, mod_name, plugin)
#
# def call_plugins(*arg, **kwargs):
#     members = [attr for attr in dir(plugins) if not callable(getattr(plugins, attr)) and not attr.startswith("__")]
#     for member in members:
#         member.main(*arg, **kwargs)


LINE_fallback = LINE(token=env.LINE_BASE_TOKEN)


class MailConverter:
    def __init__(self):
        self.mailer = Mailer(
            host=env.MAIL_HOST,
            user=env.MAIL_USER,
            pw=env.MAIL_PASSWORD,
            mailbox=env.MAIL_BOX,
        )


def notify_new_emails(mail: MailObj, LINE_TOKEN: str) -> None:
    line = LINE(token=LINE_TOKEN)
    body = bytes(mail.body, "utf-8").decode('unicode-escape')
    res = line.post(message=f"{mail.title}\n\n{body}")
    logger.info(res)
    if len(mail.attachments) > 0:
        for attachment in mail.attachments:
            res = line.post_raw_image(
                message=attachment[0], raw_image=attachment[1])
            logger.info(res)


def notify_fail(e: Exception):
    LINE_fallback.post(message=f"failed: [{type(e)}] {str(e)} {sys.exc_info()} {traceback.extract_stack()}")


def start(rules: List[RuleModel] = None):
    try:
        c = MailConverter()

        if rules is None:
            rules = my_rules

        for rule in rules:
            mailbox = rule.mailbox
            c.mailer.change_mailbox(mailbox)
            # retrieve emails
            mails: List[MailObj] = c.mailer.get(10)
            logger.info(f"[{mailbox}] received {len(mails)} mails  --------------- {datetime.datetime.now()}")

            for mail in mails:
                logger.info(mail.title)
                try:
                    notify_new_emails(mail, rule.LINE_TOKEN)
                except Exception as e:
                    logger.error(
                        f"new email notify failure: {sys.exc_info()}\n{traceback.print_exc()}")

    except Exception as e:
        notify_fail(e)
        raise


if __name__ == "__main__":
    start()
