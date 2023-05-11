from typing import Text, Dict, List

from rasa_sdk import FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import REQUESTED_SLOT
from rasa_sdk.types import DomainDict


class ValidateLoginForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_login_form"

    def validate_email(
            self,
            value: Text,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Dict[str, str]:
        if value is not None:
            return {"email": value}
        else:
            dispatcher.utter_message("The value you provided is invalid.")
            return {REQUESTED_SLOT: "email"}

    def validate_otp(
            self,
            value: Text,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Dict[str, str]:
        if value is not None:
            correct_otp = tracker.get_slot("correct_otp")
            if value == correct_otp:
                return {"otp": value}
            else:
                dispatcher.utter_message("The otp you provided is incorrect.")
                return {REQUESTED_SLOT: "email"}
        else:
            dispatcher.utter_message("The value you provided is invalid.")
            return {REQUESTED_SLOT: "email"}


class ValidateFeedbackForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_feedback_form"

    async def required_slots(
            self,
            domain_slots: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> List[Text]:
        slots = domain_slots.copy()
        ask_feedback = tracker.get_slot("ask_feedback")
        print("here required")
        if ask_feedback == "affirm":
            return slots + ["name", "email", "feedback"]
        return domain_slots

    def validate_ask_feedback(
            self,
            value: Text,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Dict[str, str]:
        intent_name = tracker.latest_message.get("intent").get("name")
        if intent_name in ["affirm", "deny"]:
            return {"ask_feedback": intent_name}
        dispatcher.utter_message("The value you provided is invalid.")
        return {REQUESTED_SLOT: "ask_feedback"}


