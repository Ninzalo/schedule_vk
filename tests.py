# -*- coding: utf-8 -*-

import os
import json
import unittest
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from config import token_vk, group_id

from Lib.bot.BotDB_Func import BotDB_Func
from Lib.bot.bot_func import Bot_class
from Lib.bot.sender import Sender
from Lib.bot.stages_names import Stages_names
from Lib.bot.event_hint import Event_hint


vk_session = vk_api.VkApi(token=token_vk)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id)

sender = Sender(vk_session=vk_session)
sn = Stages_names()
db = BotDB_Func()
bot_class = Bot_class(vk=vk)


def _create_request(text: str):
    event = Event_hint(
        msg=text.lower(),
        message=text,
        id=123,
        peer_id=123,
        button_actions=["callback"],
        attachments=None,
    )
    result = bot_class.bot(event=event)
    return result


def unpack_results(text: str):
    results = _create_request(text=text)
    list_of_dicts = []
    request = {"message": text, "returns": []}
    for item in results.returns:
        struct = {
            "user_id": item.user_id,
            "output_text": item.text,
            "buttons": [],
            "i_buttons": [],
            "attachments": [],
            "docs": [],
        }
        try:
            if item.buttons != []:
                for button in item.buttons.buttons:
                    button_struct = {
                        "label": button.text,
                        "color": button.color,
                        "new_line": button.new_line_after,
                    }
                    struct["buttons"].append(button_struct)
        except:
            pass
        try:
            if item.inline_buttons != []:
                for inline_button in item.inline_buttons.buttons:
                    i_button_struct = {
                        "label": inline_button.text,
                        "color": inline_button.color,
                        "new_line": inline_button.new_line_after,
                        "payload": inline_button.payload,
                    }
                    struct["i_buttons"].append(i_button_struct)
        except:
            pass
        if item.attachments is not None:
            for attachment in item.attachments:
                struct["attachments"].append(attachment)
        if item.preuploaded_doc is not None:
            struct["docs"].append(item.preuploaded_doc)

        request["returns"].append(struct)
    list_of_dicts.append(request)
    return list_of_dicts


class TestStringMethods(unittest.TestCase):
    def test_returns(self):
        # texts = all_texts()
        with open(f"{os.getcwd()}/Lib/tests/test_requests.json") as f:
            texts = json.load(f)
        self.maxDiff = None
        for _, text in enumerate(texts):
            # print(_ + 1)
            # print(text)
            self.assertEqual(
                [text["returns"]],
                [
                    item["returns"]
                    for item in unpack_results(text=text["message"])
                ],
            )


if __name__ == "__main__":
    unittest.main(warnings="ignore")
