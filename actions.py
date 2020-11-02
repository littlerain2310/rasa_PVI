from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet,Form,ReminderScheduled,ActionReverted,UserUtteranceReverted,FollowupAction,AllSlotsReset
from rasa.core.slots import Slot
from rasa.core.policies.memoization import MemoizationPolicy
import datetime
import time
from threading import Timer
import re
import random

age =0
class DenyForm(FormAction):
    def name(self):
        return "deny_form"
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return["contact"]
    def slot_mappings(self):
        return {
            "contact": [
                self.from_text()
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if slot_to_fill !="contact":
            print("'''")
            return [SlotSet(slot_to_fill,None)]
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        dispatcher.utter_message("Cảm ơn thời gian của A/C ạ. A/C vui lòng liên hệ số Hotline: 18006152 để được tư vấn chi tiết ạ. ")
        return []

class ActionDangerForm(FormAction):
    def name(self):
        return "action_danger_form"
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return["danger"]
    def slot_mappings(self):
        return {
            "danger": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if slot_to_fill !="danger":
            print("'''")
            return [SlotSet(slot_to_fill,None)]
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        if tracker.get_slot("danger") == False:
            dispatcher.utter_message("Một tiếng sau em gọi lại ạ.")
            return[]
        else:
            return [SlotSet('danger',True),FollowupAction("step2_form")]

class EmailForm(FormAction):
    def name(self):
        return "email_form"
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return["email_confirm"]
    def slot_mappings(self):
        return {
            "email_confirm": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='email_yes',value= False),
                self.from_intent(intent='deny',value= False)
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if slot_to_fill !="email_confirm":
            print("'''")
            return [SlotSet(slot_to_fill,None)]
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        if tracker.get_slot("email_confirm") == False:
            # dispatcher.utter_message(".")
            return[SlotSet('email_confirm',True),FollowupAction("health_form")]
        else:
            dispatcher.utter_message('Mong A/c thông cảm hiện tại hệ thống bên em vẫn chưa hoàn thiện')
            return [SlotSet('email_confirm',False)]

class ActionBusyForm(FormAction):
    def name(self):
        return "action_busy_form"
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return["busy"]
    def slot_mappings(self):
        return {
            "busy": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        
        
        if slot_to_fill !="busy":
            print("'''")
            return [SlotSet(slot_to_fill,None)]
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        if tracker.get_slot("busy") == False:
            return[]
        else:
            return [SlotSet("busy",True),FollowupAction("step2_form")]
class ActionNoNeed(Action):
    def name(self):
        return "action_no_need"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ vâng em hiểu ạ, chỉ ngày hôm nay A/C là KH may mắn được bên em lựa chọn để mang đến lời đề nghị đặc biệt từ PVI, công ty bảo hiểm uy tín số một trên thị trường')
        
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]
class BHYTSimilar(FormAction):
    def name(self):
        return "insurance_smilarity_actions"
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return["BHYT"]
    def slot_mappings(self):
        return {
            "BHYT": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if slot_to_fill !="BHYT":
            print("'''")
            return [SlotSet(slot_to_fill,None)]
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        if tracker.get_slot("BHYT") == False:
            # dispatcher.utter_message("Một tiếng sau em gọi lại ạ.")
            return[FollowupAction("deny_form")]
        else:
            return [SlotSet('BHYT',True),FollowupAction("health_form")]

class ThinkMore(FormAction):
    def name(self):
        return "action_think_more"
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return ["think_more"]
    def slot_mappings(self):
        return {
            "think_more": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if slot_to_fill !="think_more":
            print("'''")
            return [SlotSet(slot_to_fill,None)]
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        if tracker.get_slot("think_more") == False:
            # dispatcher.utter_message("Một tiếng sau em gọi lại ạ.")
            return[FollowupAction("deny_form")]
        else:
            return [SlotSet('think_more',True),FollowupAction("health_form")]
class BuyMore(FormAction):
    def name(self):
        return "buy_more_form"
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return["buy_more"]
    def slot_mappings(self):
        return {
            "buy_more": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if slot_to_fill !="buy_more":
            print("'''")
            return [SlotSet(slot_to_fill,None)]
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        if tracker.get_slot("buy_more") == False:
            # dispatcher.utter_message("Một tiếng sau em gọi lại ạ.")
            return[FollowupAction("deny_form")]
        else:
            return [SlotSet('buy_more',True),FollowupAction("step2_form")]
class ActionGoodHealth(Action):
    def name(self):
        return "action_good_health"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Chúc mừng A/C đang có sức khoẻ tốt ')
        
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]
class ActionFamilyDeny(Action):
    def name(self):
        return "action_family_deny"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Phí sản phầm này rất thấp, nó cũng phù hợp cho gia đình của mình luôn ')
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]
class ActionFastVoice(Action):
    def name(self):
        return "action_fast_voice"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Em xin lỗi ạ. Để em nói chậm lại ạ (giảm tốc độ nói lại)')
        
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]
class ActionQuestion(Action):
    def name(self):
        return "action_question"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Để em giải thích cho A/C ạ.')
        
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]
class ActionAlreadyMedical(Action):
    def name(self):
        return "action_already_medical01"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Chúc mừng A/C đã có gói bảo hiểm cho mình. Cao cấp hơn bảo hiểm y tế nhà nuớc, bảo hiểm bên em không bị giới hạn về tuyến bệnh viện, sử dụng được ở bất kì bệnh viện nào trên toàn quốc và quy trình rất nhanh và dễ dàng.   Nên có rất nhiều người mua thêm sản phẩm này bên cạnh gói BHYTNN để gia tăng quyền lợi. Bên cạnh đó,')
        
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]
class ActionKnowMore03(Action):
    def name(self):
        return "action_know_more03"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ vâng, hôm nay A/C là KH may mắn được bên em lựa chọn để mang đến lời đề nghị đặc biệt từ PVI, công ty bảo hiểm uy tín số một trên thị trường.')
        
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]    
class Unbelieve(Action):
    def name(self):
        return "action_unbelieve00"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ em hiểu. Nhưng đây là lời đề nghị đặc biệt từ PVI có trên 55 năm kinh nghiệm về bảo hiểm. Bên cạnh đó ')      
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]   
class LostMoney(Action):
    def name(self):
        return "action_unbelieve01"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ, em hiểu. 1 năm mình không dùng BH thì đó là điều tốt rồi ạ! Mà thật sự là phí bên em rất thấp mà quyền lợi lại cao. Ví dụ, một ngày nằm viện là 1-2 triệu rồi, mà phí 1 năm bên em chỉ có tầm hơn 1 triệu. Bên cạnh đó')
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]   
class Complicated(Action):
    def name(self):
        return "action_unbelieve02"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ em hiểu, nhưng thủ tục bồi thường của PVI rất đơn giản. Nếu A/C đi đến bệnh viện có liên kết, A/C chỉ cần đưa thẻ BH và CMND, PVI sẽ thanh toán phí trực tiếp cho A/C theo quyền lợi mình nhận được ạ')
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]  
class PhoneCallUnbelieve(Action):
    def name(self):
        return "action_unbelieve03"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ, em hiểu. Em là (Tên TSR) gọi từ Hoa Sao là đại lý chính thức của PVI, địa chỉ công ty em là 8A Huỳnh Lan Khanh Phường 2 Quận Tân Bình. Với lại')
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]  
class NoContrast(Action):
    def name(self):
        return "action_unbelieve04"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ em hiểu. Nếu A/C đồng ý mua thì sau cuộc gọi này, nhân viên bên em sẽ mang đơn đăng kí tham gia đến cho A/C kí trực tiếp ạ, nên A/C cứ yên tâm. Nhân tiện đây ')
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]  
class ActionOverAge(Action):
    def name(self):
        return "action_overage"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Rất tiếc cô chú không thể tham gia được sản phẩm đặc biệt này của PVI. Tuy nhiên, cô chú có thể tham gia cho gia đình hoặc nhân viên công ty nếu cố chú là chủ doanh nghiệp ạ. ')
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]    
class ActionLowVoice(FormAction):    
    def name(self):
        return "action_low_voice_form"
    @staticmethod
    def requested_slot(tracker)-> List[Text]:
        return["low_voice"]
    def slot_mappings(self):
        return {
            "low_voice": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if slot_to_fill !="low_voice":
            print("'''")
            return [SlotSet(slot_to_fill,None)]
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        if tracker.get_slot("low_voice") == False:
            dispatcher.utter_message("Chỉ hôm nay thôi em mang đến cho A/C lời đề nghị đặc biệt từ PVI. Khoảng 1 tiếng sau em gọi lại ạ.")
            return[]
        else:
            return [SlotSet('low_voice',True),FollowupAction("step2_form")]
class SetReminder(Action):
    def name(self):
        return "action_set_reminder"
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        #dispatcher.utter_message("I will remind you in 30 seconds.")

        date = datetime.datetime.now() + datetime.timedelta(seconds=30)
        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            name="my_reminder",
            kill_on_user_message=True,
        )

        return [reminder]
class AlreadyHad01(FormAction):
    def name(self):
        return 'already_had01_form'
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        if tracker.get_slot("already_had01") == True :
            return["already_had01"]
        else:
            if tracker.get_slot("health_insurance") == True :
                return ["already_had01","health_insurance"]
            else:
                return ["already_had01","health_insurance","boss2"]
    def slot_mappings(self):
        return {
            "already_had01": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ],
            "health_insurance": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ],
            "boss2": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ],
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        # if slot_to_fill !="already_had01" or slot_to_fill !="health_insurance" or slot_to_fill !="boss2" :
        #     print("bug already")
        #     return [SlotSet(slot_to_fill,None)]
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        result = []
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if tracker.get_slot("already_had01") == True:
            return[FollowupAction("step2_form")]
        elif tracker.get_slot("health_insurance") == True:
            return[FollowupAction("action_already_medical01")]
        elif tracker.get_slot("boss2") == True:
            return[FollowupAction("already_had02_form")]
        else:
            return[FollowupAction("action_family_deny")]
class AlreadyHad02(FormAction):
    def name(self):
        return 'already_had02_form'
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return["boss"]
    def slot_mappings(self):
        return {
            "boss": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if slot_to_fill !="boss":
            print("'''")
            return [SlotSet(slot_to_fill,None)]
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        if tracker.get_slot("boss") == False:
            dispatcher.utter_message("Mình có thể mua cho gia đình của mình ạ.")
            return[SlotSet('boss',False),FollowupAction("step2_form")]
        else:
            dispatcher.utter_message(" A/C có thể mua cho gia đình hoặc nhân viên của mình ạ")
            return [SlotSet('boss',True),FollowupAction("step2_form")]
class AdviseMore(FormAction):
    def name(self):
        return 'advise_more_form'
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return["advise_more"]
    def slot_mappings(self):
        return {
            "advise_more": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if slot_to_fill !="advise_more":
            print("'''")
            return [SlotSet(slot_to_fill,None)]
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        if tracker.get_slot("advise_more") == False:
            dispatcher.utter_message("nên đổi sang cho TL xử lý tiếp")
            return[]
        else:
            return [SlotSet('advise_more',True),FollowupAction("step2_form")]
class OptionInsuranceRight(Action):
    def name(self):
        return "action_FAQ01"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ,quyền lợi BH lựa chọn nghĩa là chỉ với 285,000 VND, sẽ nhận được 125 triệu đồng tiền mặt cho một chẩn đoán ung thư')
        slot_to_fill = tracker.get_slot("requested_slot")
        dispatcher.utter_message(template='utter_ask_{}'.format(slot_to_fill))
        return [FollowupAction("additional_form")]
class Sale(Action):
    def name(self):
        return "action_FAQ02"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Chỉ ngày hôm nay Anh Chị là KH may mắn được bên em lựa chọn để mang đến lời đề nghị đặc biệt từ PVI, công ty bảo hiểm uy tín trên thị trường. Mặc dù giá thị trường là 5 triệu đồng, nhưng hôm nay anh chị có thể sở hữu gói bảo hiểm này khoảng 1 triệu đồng thôi ạ.')
        # slot_to_fill = tracker.get_slot("requested_slot")
        
        # dispatcher.utter_message(template='utter_ask_{}'.format(slot_to_fill))
        return [FollowupAction("additional_form")]
class WhyIHaveToMore(Action):
    def name(self):
        return "action_FAQ03"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Với gói lựa chọn, Anh Chị sẽ có thêm quyền lợi là nhận được 125 triệu đồng tiền mặt cho một chẩn đoán ung thư')
        slot_to_fill = tracker.get_slot("requested_slot")
        dispatcher.utter_message(template='utter_ask_{}'.format(slot_to_fill))
        return [FollowupAction("additional_form")]
class FAQ04(Action):
    def name(self):
        return "action_FAQ04"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Nó cũng đơn giản như thủ tục của Anh Chị vậy, chỉ cần trả lời 4 câu hỏi sức khỏe của người thân gia đình mình và nhân viên bên em sẽ đến nhà anh chỉ để thu phí cùng lúc cho cả gia đình luôn ạ!')
        # slot_to_fill = tracker.get_slot("requested_slot")
        # dispatcher.utter_message(template='utter_ask_{}'.format(slot_to_fill))
        return [FollowupAction("additional_form")]
class GoldDiaMond(Action):
    def name(self):
        return "action_FAQ05"
    def run(self, dispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Các hạn mức gói cao hơn thì sẽ được hưởng mức quyền lợi cao hơn, ví dụ như gói Kim Cương tổng quyền lợi bảo hiểm là 500 triệu đồng cho nội trú và phẫu thuật')
        # slot_to_fill = tracker.get_slot("requested_slot")
        # print("bug cua diamond")
        # temp="utter_ask_{}".format(slot_to_fill)
        # dispatcher.utter_message("bug ne")
        # dispatcher.utter_message(template=temp)
        # print("bug cua diamond")
        return [FollowupAction("additional_form")]        
class MyReminder(Action):
    def name(self):
        return 'my_reminder'
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message(template='utter_remind')
        return [Form(None),SlotSet('requested_slot',None),FollowupAction('step2_form')]   

class BeginForm(FormAction):
    def name(self):
        return 'begin_form'
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return ["people"]
    def slot_mappings(self):
        return{
            # "number_insurance": [
            #     #self.from_entity(entity="number_insurance",not_intent="chichat"),
            #     self.from_text()
            # ],
            "people":[
                self.from_entity(entity="people",not_intent="chichat"),
                self.from_text()
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="my_reminder",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
            value = tracker.latest_message["entities"] 
            # if not value:
            #     print("''''")
            #     # text = tracker.latest_message.get("text")
            #     result.append(SlotSet(slot_to_fill,None))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        intent = tracker.latest_message.get("intent", {}).get("name")
        # if slot_to_fill == "number_insurance" :
        #     if intent != "give_number":
        #         print('bug')
        #         result.append(SlotSet(slot_to_fill,None))
        if slot_to_fill == "people" :
            if intent != "give_people":
                print('bug2')
                result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        #dispatcher.utter_message(template="utter_ask_end_step1")
        return [FollowupAction("step2_form")]

class Step2Form(FormAction):
    def name(self):
        return 'step2_form'
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        if tracker.get_slot("start02") == True:
            return ["start02"]
        else:
            return ["start02","contact"]
    def slot_mappings(self):
        return{
            "start02": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ],
            "contact": [
                self.from_text()
            ]
        }
    def validate_start02(self,value, dispatcher, tracker, domain):
        # result = []
        # # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        # #                                 trigger_date_time=datetime.datetime.now()
        # #                                 + datetime.timedelta(seconds=30),
        # #                                 name="my_reminder",
        # #                                 kill_on_user_message=True))
        # slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        # value = tracker.latest_message.get("text")
        # slot_to_fill = tracker.get_slot("requested_slot")
        # if slot_to_fill: 
        #     slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        #     value = tracker.latest_message["entities"] 
        #     # if not value:
        #     #     text = tracker.latest_message.get("text")
        #     #     result.append(SlotSet(slot_to_fill,text))
        # for slot, value in slot_values.items():
        #     result.append(SlotSet(slot, value))
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            return {"start02":None}
        elif intent == "deny":
            return {"start02":False}
        elif intent == "affirm":
            return {"start02":True}
        # else :
        #     return {"start02":None}
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        result = []
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        # dispatcher.utter_message(template='utter_start05')
        # if tracker.get_slot('start02') == True:
        #     return [result,FollowupAction('health_form')]
        # else:
        #     dispatcher.utter_message("Vâng em xin chào anh/chị")
        #     return []
        if tracker.get_slot("start02")==True :
            # dispatcher.utter_message('A/C vui lòng trả lời 4 câu hỏi sức khỏe, sau đó bên e sẽ có nhân viên xuống tận nơi làm hồ sơ và thu phí hoặc mình sẽ thanh toán trực tiếp trên website PVI.')
            # result.append(FollowupAction('health_form'))
            return [FollowupAction('health_form')]
        elif tracker.get_slot("start02")==False :
            dispatcher.utter_message("Cảm ơn thời gian của A/C ạ. A/C vui lòng liên hệ số Hotline: 18006152 để được tư vấn chi tiết ạ. ")
            # return [result,FollowupAction('')]
            return []

class HealthForm(FormAction):
    def name(self):
        return 'health_form'
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        if tracker.get_slot("buy_confirm") == False:
            return ["buy_confirm","contact"]
        if tracker.get_slot("start_healthform") == False:
            return["buy_confirm","start_healthform","contact"]
        else:
            return["buy_confirm","start_healthform","health01","health02","health03","health04"]
    def slot_mappings(self):
        return {
            "start_healthform": [
                self.from_intent(intent="affirm",value= True),
                self.from_intent(intent="deny",value= False),
                self.from_text()
            ],
            "buy_confirm" : [
                self.from_intent(intent="affirm",value= True),
                self.from_intent(intent="deny",value= False),
                self.from_text()
            ],
            "contact": [
                self.from_text()
            ],
            "health01": [
                self.from_intent(intent="affirm",value= True),
                self.from_intent(intent="deny",value= False),
                self.from_text()
            ],
            "health02": [
                self.from_intent(intent="affirm",value= True),
                self.from_intent(intent="deny",value= False),
                self.from_text()
            ],
            "health03": [
                self.from_intent(intent="affirm",value= True),
                self.from_intent(intent="deny",value= False),
                self.from_text()
            ],
            "health04": [
                self.from_intent(intent="affirm",value= True),
                self.from_intent(intent="deny",value= False),
                self.from_text()
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="my_reminder",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
            value = tracker.latest_message["entities"] 
            # if not value:
            #     text = tracker.latest_message.get("text")
            #     result.append(SlotSet(slot_to_fill,text))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "affirm":
            result.append(SlotSet(slot_to_fill,True))
        elif intent == "deny":
            result.append(SlotSet(slot_to_fill,False))
        else :
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        ran = random.randrange(0,2)
        result = []
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if tracker.get_slot("buy_confirm") == False:
            dispatcher.utter_message("Cảm ơn thời gian của A/C ạ. A/C vui lòng liên hệ số Hotline: 18006152 để được tư vấn chi tiết ạ. ")
            return []
        if tracker.get_slot("start_healthform") == False:
            dispatcher.utter_message("Cảm ơn thời gian của A/C ạ. A/C vui lòng liên hệ số Hotline: 18006152 để được tư vấn chi tiết ạ. ")
            return []
        elif tracker.get_slot('health01') == True or tracker.get_slot('health02') == True or tracker.get_slot('health03') == True or tracker.get_slot('health04') == True:
            return [FollowupAction('sub_health_form')]      
        else :
            dispatcher.utter_message(template= 'utter_step06')
            # dispatcher.utter_message("Dạ e xin chúc mừng tình hình sức khỏe mình rất tốt đủ điều kiện tham gia chương trình bên em. \nVà đây là các đặc điểm nổi trội của gói bảo hiểm chính:\nViện phí trong thời gian điều trị nội trú: (Tối đa 60 ngày/năm) 1,250,000 VND/ngày, tối đa 62,500,000 VND/năm \n- Tiền giường điều trị\n- Xét nghiệm, chẩn đoán hình ảnh\n- Thuốc điều trị\n- Các chi phí y tế khác\n2. Chi phí phẫu thuật (không bao gồm chi phí khám tiền phẫu thuật) : tối đa 62,500,000 VND/năm \n3. Chi phí y tế cho phương pháp điều trị ung thư tiên tiến (giới hạn cho từng bệnh) lên đến 125,000,000 VND/năm  \n\nTiếp theo, em xin giới thiệu đến A/C những gói lựa chọn và gói nâng cấp có thể thêm vào gói chính của A/C như sau: " )
            # if ran == 0 :
            #     dispatcher.utter_message('Cảm ơn Anh/Chị đã trả lời các câu hỏi. Em xin xác nhận ở thời điểm hiện tại, tình hình sức khoẻ Anh/Chị là rất tốt.Bên em sẽ tiến hành các văn bản khai báo sức khỏe chính thức sau. Trước tiên, em xin phép giới thiệu chi tiết gói sản phẩm.')
            #     dispatcher.utter_message(template='utter_step06')
            #     return [FollowupAction('additional_form')]
            # else :
            #     dispatcher.utter_message('Cám ơn Anh/Chị đã trả lời câu hỏi, vì em chưa biết rõ về tình trạng sức khoẻ của Anh/Chị nên em xin phép được tiếp tục các bước tiếp theo')
            #     dispatcher.utter_message('Các câu hỏi trên đây chỉ dùng để tham khảo về tình hình sức khoẻ hiện tại của Anh/Chị, chưa phải là văn bản chính thức.\nEm nhận thấy Anh/Chị đang rất quan tâm về sản phẩm này, nhân viên bên em sẽ đến tận nơi của anh chị để hỗ trợ hoàn tất bảng câu hỏi sức khoẻ. Anh/Chị vui lòng điền đầy đủ thông tin và kí tên xác nhận.\nNhưng trước tiên, em xin phép giới thiệu chi tiết gói sản phẩm.')
            return [FollowupAction('additional_form')]
class SubHealthForm(FormAction):
    def name(self):
        return 'sub_health_form'
    @staticmethod
    def required_slots(tracker) -> List[Text]:
        # if day > 7 or week > 1:
        #     return ['sick','time','surgery','bad_sick']
        return ['sick','time','surgery']
    def slot_mappings(self):
        return {
           "sick": [
                self.from_entity(entity="sick",not_intent="chichat"),
                self.from_text()
            ],
            "time": [
                self.from_entity(entity="day",not_intent="chichat"),
                self.from_entity(entity="week",not_intent="chichat"),
                self.from_text()
            ],
            "surgery": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ],
            "day":[
                self.from_entity(entity="day"),
            ],
            "week":[
                self.from_entity(entity="week")
            ]  
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if slot_to_fill == "time":
            value = tracker.latest_message["entities"] 
            value_=[]
            for x in value:
                value_.append(x['entity'])
            if 'day' in value_ or 'week' in value_:
                for x in value:
                    if x['entity'] == 'day':
                        print('alo')
                        result.append(SlotSet('day',x['value']))
                    if x['entity'] == 'week':
                        result.append(SlotSet('week',x['value']))
        # if slot_to_fill == 'time':
        #     time = tracker.latest_message['entities']['entity']
        #     if time == "day":
        #         day = int(time["value"])
        #     if time == "week":
        #         week = int(time["value"])
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        # bad_sick = tracker.get_slot('bad_sick')
        # if bad_sick == False:
        #     dispatcher.utter_message('Em cám ơn Anh/Chị đã dành thời gian trao đổi với em. Đồng thời em cũng rất tiếc vì thời điểm này cty vẫn chưa thể cung cấp được gói bảo hiểm phù hợp với Anh/Chị. Em rất hy vọng được phục vụ Anh/Chị với những sản phẩm khác trong tương lai.') 
        result = []
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if tracker.get_slot('day'):
            print('bug')
            day = int(tracker.get_slot('day'))
            if day > 7:
                print('bug')
                return [result,FollowupAction('bad_health_form')]
        if tracker. get_slot('week'):
            week = int(tracker.get_slot('week'))
            if week > 1:
                return [result,FollowupAction('bad_health_form')]  
        dispatcher.utter_message('Cảm ơn Anh/Chị đã trả lời các câu hỏi. Em xin xác nhận ở thời điểm hiện tại, tình hình sức khoẻ Anh/Chị là rất tốt.\n\nBên em sẽ tiến hành các văn bản khai báo sức khỏe chính thức sau. Trước tiên, em xin phép giới thiệu chi tiết gói sản phẩm.') 
        dispatcher.utter_message(template='utter_step06')  
        return [FollowupAction('additional_form')]
class BadHealthForm(FormAction):
    def name(self):
        return "bad_health_form"
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return["bad_sick"]
    def slot_mappings(self):
        return {
            "bad_sick": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "affirm":
            result.append(SlotSet(slot_to_fill,True))
        elif intent == "deny":
            result.append(SlotSet(slot_to_fill,False))
        else :
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        if tracker.get_slot("bad_sick") == False:
            dispatcher.utter_message("Em cám ơn Anh/Chị đã dành thời gian trao đổi với em. Đồng thời em cũng rất tiếc vì thời điểm này cty vẫn chưa thể cung cấp được gói bảo hiểm phù hợp với Anh/Chị. Em rất hy vọng được phục vụ Anh/Chị với những sản phẩm khác trong tương lai")
            return[]
        else:
            dispatcher.utter_message("Các câu hỏi trên đây chỉ dùng để tham khảo về tình hình sức khoẻ hiện tại của Anh/Chị, chưa phải là văn bản chính thức.\nEm nhận thấy Anh/Chị đang rất quan tâm về sản phẩm này, nhân viên bên em sẽ đến tận nơi của anh chị để hỗ trợ hoàn tất bảng câu hỏi sức khoẻ. Anh/Chị vui lòng điền đầy đủ thông tin và kí tên xác nhận.\nNhưng trước tiên, em xin phép giới thiệu chi tiết gói sản phẩm.")
            dispatcher.utter_message(template='utter_step06')  
            return [SlotSet('bad_sick',True),FollowupAction("additional_form")]

class AdditionalForm(FormAction):
    def name(self):
        return 'additional_form'
    
    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['addition01','addition02','addition03']
    def slot_mappings(self):
        return {
           "addition01": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False),
                self.from_text()
            ],
            "addition02": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False),
                self.from_text()
            ],
            "addition03": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False),
                self.from_text()
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "affirm":
            result.append(SlotSet(slot_to_fill,True))
        elif intent == "deny":
            result.append(SlotSet(slot_to_fill,False))
        else :
            print('bug')
            result.append(SlotSet(slot_to_fill,None))
        return result
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        result = []
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        dispatcher.utter_message('Em xin lưu ý, kể từ khi bắt đầu ký tên và đóng phí thì bảo hiểm này sẽ có hiệu lực sau 30 ngày cho ốm bệnh thông thường, sau 90 ngày cho bệnh liên quan đến ung thư và sau 1 năm cho bệnh có sẵn và mãn tính.')
        return [FollowupAction("info_form")]
class InforForm(FormAction):
    def name(self):
        return "info_form"
    @staticmethod
    def is_id(string: Text) -> bool:
        """Check if a string is an integer."""
        try:
            value = int(string)
            regex = "\w{10}"
            if re.search(regex,string):
                return True
        except :
            return False
    @staticmethod
    def required_slots(tracker):
        print("toi vao day roi")
        return ["name","id","id_time","id_location","payment"]
    @staticmethod
    def convert_tail(s):
        s=s.lower()
        if "h" in s:
            s=s.replace("h","")
            print("1")
            return s
        elif "pm" in s:
            s=s.replace("pm","")
            s= int(s)+12
            return s
        elif "am" in s:
            s=s.replace("am","")
            return s
        else:
            print("2")
            return s
    def slot_mappings(self):
        return {
            "name":[
                self.from_entity(entity="name"),
                self.from_text()
            ],
            "id":[
                self.from_entity(entity="id"),
                self.from_text()
            ],
            "id_time":[
                self.from_entity(entity="id_time"),
                self.from_text()
            ],
            "id_location":[
                # self.from_entity(entity="address")
                self.from_text()
            ],
            "payment":[
                self.from_entity(entity="payment"),
                self.from_intent(intent="online_payment",value="Online"),
                self.from_intent(intent="offline_payment",value="Offline"),
                self.from_text()
            ],
        }
    def validate_id(self,value, dispatcher, tracker, domain):
        if self.is_id(value):
            if len(value) >= 10 and len(value) <= 12 :
                return {"id": value}
            else:
                return {"id": None}
        else:
            return {"id": None}
    def validate_id_time(self,value, dispatcher, tracker, domain):
        value = tracker.latest_message["entities"] 
        value_=[]
        for x in value:
            value_.append(x['entity'])
        if "day" in value_ and "month" in value_ and "year" in value_ and "hour" in value_:
            for x in value:
                if x['entity'] == 'day':
                    day = x['value']
                if x['entity'] == 'month':
                    month = x['value']
                if x['entity'] == 'year':
                    year = x['value']
                if x['entity'] == 'hour':
                    hour = x['value']
                    hour = self.convert_tail(hour)
            time = datetime.datetime(int(year),int(month),int(day),int(hour))
            time=time.strftime("%m/%d/%Y, %H:%M:%S")
        elif "day" in value_ and "month" in value_ and "year" in value_ :
            for x in value:
                if x['entity'] == 'day':
                    day = x['value']
                if x['entity'] == 'month':
                    month = x['value']
                if x['entity'] == 'year':
                    year = x['value']
            time = datetime.datetime(int(year),int(month),int(day))
            time=time.strftime("%m/%d/%Y, %H:%M:%S")     
        elif "day2" in value_ and "hour" in value_  :
            for x in value:
                if x['entity'] == 'day2':
                    day2 = x['value']
                    if day2 == "nay":
                        time= datetime.datetime.now()
                    elif day2 == "mai":
                        time= datetime.datetime.now() + datetime.timedelta(days=1)
                    elif day2 == "kia":
                        time = datetime.datetime.now() + datetime.timedelta(days=2)
                if x['entity'] == 'hour':
                    hour = x['value']
                    hour = self.convert_tail(hour)
            time = time.replace(hour=int(hour),minute=0,second=0)
            time=time.strftime("%m/%d/%Y, %H:%M:%S")
        elif "hour" in value_ :
            time = datetime.datetime.now()
            for x in value:
                if x['entity'] == 'hour':
                    hour = x['value']
                    hour = self.convert_tail(hour)
                    time = time.replace(hour=int(hour),minute=0,second=0)
                    time=time.strftime("%m/%d/%Y, %H:%M:%S")
        else:
            return {"id_time":None}
        return {"id_time": time}
    def submit(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )->List[Dict]:
        result = []
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        if tracker.get_slot("payment") == "Online":
            dispatcher.utter_message("Chọn thanh toán")
            return []
        else:
            return [SlotSet("money","1.175.000 vnd"),FollowupAction("offline_pay_form")]
class OfflinePay(FormAction):
    def name(self):
        return 'offline_pay_form'
    @staticmethod
    def required_slots(tracker):
        return ["address","pay_time","confirm","last_ask"]
    @staticmethod
    def convert_tail(s):
        s=s.lower()
        if "h" in s:
            s=s.replace("h","")
            print("1")
            return s
        elif "pm" in s:
            s=s.replace("pm","")
            s= int(s)+12
            return s
        elif "am" in s:
            s=s.replace("am","")
            return s
        else:
            print("2")
            return s
    def slot_mappings(self):
        return {
            "address":[
                self.from_entity(entity="address"),
                self.from_text()
            ],
            "pay_time":[
                self.from_entity(entity="pay_time"),
                self.from_text()
            ],
            "confirm":[
                # self.from_entity(entity="pay_time"),
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ],
            "last_ask":[
                # self.from_entity(entity="address"),
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ]
        }
    def validate_confirm(self,value, dispatcher, tracker, domain):
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            return {"confirm":None}
        return {"confirm":value}
    def validate_last_ask(self,value, dispatcher, tracker, domain):
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "deny":
            return {"last_ask":False}
        elif intent == "affirm":
            dispatcher.utter_message("A/c vui lòng thông cảm bên hệ thống bên em vẫn chưa hoàn thiện")
            return {"last_ask":True}
        else :
            return {"last_ask": None}       
    def validate_pay_time(self,value, dispatcher, tracker, domain):
        intent = tracker.latest_message.get("intent", {}).get("name")
        # if intent != "give_day":
        #     return{"pay_time":None}
        value = tracker.latest_message["entities"] 
        value_=[]
        for x in value:
            value_.append(x['entity'])
        if "day" in value_ and "month" in value_ and "year" in value_ and "hour" in value_:
            for x in value:
                if x['entity'] == 'day':
                    day = x['value']
                if x['entity'] == 'month':
                    month = x['value']
                    if int(month) > 12:
                        return {"pay_time":None}
                if x['entity'] == 'year':
                    year = x['value']
                if x['entity'] == 'hour':
                    hour = x['value']
                    hour = self.convert_tail(hour)
            time = datetime.datetime(int(year),int(month),int(day),int(hour))
            time=time.strftime("%m/%d/%Y, %H:%M:%S")
            return {"pay_time": time}
        elif "day" in value_ and "month" in value_ and "year" in value_ :
            for x in value:
                if x['entity'] == 'day':
                    day = x['value']
                if x['entity'] == 'month':
                    month = x['value']
                if x['entity'] == 'year':
                    year = x['value']
            time = datetime.datetime(int(year),int(month),int(day))
            time=time.strftime("%m/%d/%Y, %H:%M:%S")   
            return {"pay_time": time}  
        elif "day2" in value_ and "hour" in value_  :
            for x in value:
                if x['entity'] == 'day2':
                    day2 = x['value']
                    if day2 == "nay":
                        time= datetime.datetime.now()
                    elif day2 == "mai":
                        time= datetime.datetime.now() + datetime.timedelta(days=1)
                    elif day2 == "kia":
                        time = datetime.datetime.now() + datetime.timedelta(days=2)
                if x['entity'] == 'hour':
                    hour = x['value']
                    hour = self.convert_tail(hour)
            time = time.replace(hour=int(hour),minute=0,second=0)
            time=time.strftime("%m/%d/%Y, %H:%M:%S")
            return {"pay_time": time}
        elif "hour" in value_ :
            time = datetime.datetime.now()
            for x in value:
                if x['entity'] == 'hour':
                    hour = x['value']
                    hour = self.convert_tail(hour)
                    time = time.replace(hour=int(hour),minute=0,second=0)
                    time=time.strftime("%m/%d/%Y, %H:%M:%S")
            return {"pay_time": time}
        else:
            return {"pay_time":None}
        
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        ):
        
        dispatcher.utter_message('Dạ em cảm ơn')
        return []
        
class FeeAsk(FormAction):
    def name(self):
        return 'fee_ask_form'
    @staticmethod
    def required_slots(tracker) -> List[Text]:
        global age
        if int(age) < 46 :
            return ['age','join_young']
        elif int(age) >=46 and int(age) <=55:
            return['age','join_mid']
        else:
            if tracker.get_slot('UuViet_joinning') == True :
                return ['age','UuViet_joinning','join_old_yes']
            else:
                return ['age','UuViet_joinning','join_old_no']
    def slot_mappings(self):
        return {
            "age": [
                self.from_text()
            ],
            'UuViet_joinning': [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False),
                self.from_text()
            ],
            'join_young': [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False),
                self.from_text()
            ],
            'join_mid': [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False),
                self.from_text()
            ],
            'join_old_yes': [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False),
                self.from_text()
            ],
            'join_old_no': [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False),
                self.from_text()
            ],
          
        }
    def validate(self, dispatcher, tracker, domain):
        global age
        result = []
        # result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
        #                                 trigger_date_time=datetime.datetime.now()
        #                                 + datetime.timedelta(seconds=30),
        #                                 name="first_remind",
        #                                 kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        # if slot_to_fill !="already_had01" or slot_to_fill !="health_insurance" or slot_to_fill !="boss2" :
        #     print("bug already")
        #     return [SlotSet(slot_to_fill,None)]
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "chitchat":
            result.append(SlotSet(slot_to_fill,None))
        if slot_to_fill == "age":
            intent = tracker.latest_message.get("intent", {}).get("name")
            # if intent != "give_birthday":
            #     return {"age": None}
            value = tracker.latest_message["entities"]
            # if value['entity'] == "age":
            #     age = value['value']
            #     return {"age": value}
            value_=[]
            for x in value:
                value_.append(x['entity'])
            if 'fulldatetime' in value_:
                for x in value:
                    if x['entity'] == 'fulldatetime':
                        year_now = datetime.datetime.now()
                        year_now = int(year_now.year)
                        year = x['value'][-4:]
                        age = year_now - int(year)
                        result.append(SlotSet(slot_to_fill,age))       
            elif "age" in value_:
                for x in value:
                    if x['entity'] == 'age':
                        age = x['value']
                        result.append(SlotSet(slot_to_fill,age))
            elif "day" in value_ and "month" in value_ and "year" in value_ :
                for x in value:
                    if x['entity'] == 'day':
                        day = x['value']
                    if x['entity'] == 'month':
                        month = x['value']
                        if int(month) > 12 :
                            return {"age":None}
                    if x['entity'] == 'year':
                        year = x['value']
                time = datetime.datetime(int(year),int(month),int(day))
                x = datetime.datetime.now()
                year_now = int(x.year)
                print("year")
                age = year_now - int(year)
                print(age)
                result.append(SlotSet(slot_to_fill,age))
            elif "day" in value_:
                for x in value:
                    if x['entity'] == 'day':
                        age = x['value']
                        result.append(SlotSet(slot_to_fill,age))
            elif "month" in value_:
                    for x in value:
                        if x['entity'] == 'month':
                            age = x['value']
                            result.append(SlotSet(slot_to_fill,age))
            elif "year" in value_:
                    for x in value:
                        if x['entity'] == 'year':
                            age = x['value']
                            result.append(SlotSet(slot_to_fill,age))
            else:
                result.append(SlotSet(slot_to_fill,None))
       
        if slot_to_fill == "UuViet_joinning":
            intent = tracker.latest_message.get("intent", {}).get("name")
            if intent == "affirm":
                result.append(SlotSet(slot_to_fill,True))
            elif intent == "deny":
                result.append(SlotSet(slot_to_fill,False))
            else:
                result.append(SlotSet(slot_to_fill,None))
        return result
    # def validate_age(self,value, dispatcher, tracker, domain):
    #     global age
    #     # value = tracker.latest_message.get("text")
    #     slot_to_fill = tracker.get_slot("requested_slot")
    #     if slot_to_fill !="age":
    #         print("'''")
    #         return [SlotSet(slot_to_fill,None)]
        
    #     intent = tracker.latest_message.get("intent", {}).get("name")
    #     # if intent != "give_birthday":
    #     #     return {"age": None}
    #     value = tracker.latest_message["entities"]
    #     # if value['entity'] == "age":
    #     #     age = value['value']
    #     #     return {"age": value}
    #     value_=[]
    #     for x in value:
    #         value_.append(x['entity'])
    #     if "age" in value_:
    #         for x in value:
    #             if x['entity'] == 'age':
    #                 age = x['value']
    #                 return {"age": age}
    #     elif "day" in value_ and "month" in value_ and "year" in value_ :
    #         for x in value:
    #             if x['entity'] == 'day':
    #                 day = x['value']
    #             if x['entity'] == 'month':
    #                 month = x['value']
    #             if x['entity'] == 'year':
    #                 year = x['value']
    #         time = datetime.datetime(int(year),int(month),int(day))
    #         x = datetime.datetime.now()
    #         year_now = int(x.year)
    #         age = year_now - int(year)
    #         return {"age": age}
    #     else:
    #         return {"age": None}
    # def validate_UuViet_joinning(self,value, dispatcher, tracker, domain):
    #     slot_to_fill = tracker.get_slot("requested_slot")
    #     if slot_to_fill !="UuViet_joinning":
    #         print("'''")
    #         return [SlotSet(slot_to_fill,None)]
    #     intent = tracker.latest_message.get("intent", {}).get("name")
    #     if intent == "affirm":
    #         return {"UuViet_joinning":True}
    #     elif intent == "deny":
    #         return {"UuViet_joinning":False}
    #     else:
    #         return {"UuViet_joinning":None}
    def submit(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )->List[Dict]:
        global age
        result = []
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
        # age= tracker.get_slot("age")
        print(age)
        print(type(age))
        if int(age) <= 45 :
            # dispatcher.utter_message("Mức phí là 1.175.000 vnd/năm.  BH PVI hỗ trợ chi phí nội trú, phẫu thuật và chi phí điều trị Ung thư bằng kỹ thuật tiên tiến, mình được sử dụng tại tất cả bệnh viện toàn quốc. Em hỗ trợ mình tham gia trong hôm nay ạ. ")
            result.append(SlotSet("money","1.175.000 vnd"))
        elif int(age) < 55 and int(age) >= 46:
            # dispatcher.utter_message("Mức phí là 1.700.0000 vnd/năm. BH PVI hỗ trợ chi phí nội trú, phẫu thuật và chi phí điều trị Ung thư bằng kỹ thuật tiên tiến, mình được sử dụng tại tất cả bệnh viện toàn quốc. Em hỗ trợ mình tham gia trong hôm nay ạ. ")
            result.append(SlotSet("money","1.700.000 vnd")) 
        else:
            if tracker.get_slot("UuViet_joinning") == True:
                # dispatcher.utter_message("Mức phí là 3.000.0000 vnd/năm. BH PVI hỗ trợ chi phí nội trú, phẫu thuật và chi phí điều trị Ung thư bằng kỹ thuật tiên tiến, mình được sử dụng tại tất cả bệnh viện toàn quốc. Em hỗ trợ mình tham gia trong hôm nay ạ. ")
                result.append(SlotSet("money","3.000.000 vnd")) 
            elif tracker.get_slot("UuViet_joinning") == False:
                # dispatcher.utter_message("Em rất tiếc sản phẩm PVI chỉ hỗ trợ cho KH từ 01-55 tuổi. Tuy nhiên, nhân cơ hội mức phí rất thấp 3000vnd/ngày, được hỗ trợ tất cả bệnh viện toàn quốc. Em hỗ trợ mình đăng ký cho gia đình người thân của mình ạ")
                result.append(SlotSet("money","1.175.000 vnd"))
        return [FollowupAction("health_form")]
