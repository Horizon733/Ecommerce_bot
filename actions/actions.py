from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from actions.utils import generate_otp


class ActionAskOTP(Action):
    def name(self) -> Text:
        return "action_ask_otp"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        otp = generate_otp()
        dispatcher.utter_message(response="utter_otp")
        return [SlotSet("correct_otp", otp)]
