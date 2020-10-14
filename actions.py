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
        result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=30),
                                        name="first_remind",
                                        kill_on_user_message=True))
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
        result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=30),
                                        name="first_remind",
                                        kill_on_user_message=True))
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
        
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]
class ActionGoodHealth(Action):
    def name(self):
        return "action_good_health"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Chúc mừng A/C đang có sức khoẻ tốt ')
        
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]
class ActionFamilyDeny(Action):
    def name(self):
        return "action_family_deny"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Phí sản phầm này rất thấp, nó cũng phù hợp cho gia đình của mình luôn ')
        
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]
class ActionFastVoice(Action):
    def name(self):
        return "action_fast_voice"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Em xin lỗi ạ. Để em nói chậm lại ạ (giảm tốc độ nói lại)')
        
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]
class ActionQuestion(Action):
    def name(self):
        return "action_question"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Để em giải thích cho A/C ạ.')
        
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]
class ActionAlreadyMedical(Action):
    def name(self):
        return "action_already_medical01"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Chúc mừng A/C đã có gói bảo hiểm cho mình. Cao cấp hơn bảo hiểm y tế nhà nuớc, bảo hiểm bên em không bị giới hạn về tuyến bệnh viện, sử dụng được ở bất kì bệnh viện nào trên toàn quốc và quy trình rất nhanh và dễ dàng.   Nên có rất nhiều người mua thêm sản phẩm này bên cạnh gói BHYTNN để gia tăng quyền lợi. Bên cạnh đó,')
        
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]
class ActionKnowMore03(Action):
    def name(self):
        return "action_know_more03"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ vâng, hôm nay A/C là KH may mắn được bên em lựa chọn để mang đến lời đề nghị đặc biệt từ PVI, công ty bảo hiểm uy tín số một trên thị trường.')
        
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]    
class ActionUnbelieve00(Action):
    def name(self):
        return "action_unbelieve00"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ em hiểu. Nhưng đây là lời đề nghị đặc biệt từ PVI có trên 55 năm kinh nghiệm về bảo hiểm. Bên cạnh đó ')      
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]   
class ActionUnbelieve01(Action):
    def name(self):
        return "action_unbelieve01"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ, em hiểu. 1 năm mình không dùng BH thì đó là điều tốt rồi ạ! Mà thật sự là phí bên em rất thấp mà quyền lợi lại cao. Ví dụ, một ngày nằm viện là 1-2 triệu rồi, mà phí 1 năm bên em chỉ có tầm hơn 1 triệu. Bên cạnh đó')
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]   
class ActionUnbelieve02(Action):
    def name(self):
        return "action_unbelieve02"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ em hiểu, nhưng thủ tục bồi thường của PVI rất đơn giản. Nếu A/C đi đến bệnh viện có liên kết, A/C chỉ cần đưa thẻ BH và CMND, PVI sẽ thanh toán phí trực tiếp cho A/C theo quyền lợi mình nhận được ạ')
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]  
class ActionUnbelieve03(Action):
    def name(self):
        return "action_unbelieve03"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ, em hiểu. Em là (Tên TSR) gọi từ Hoa Sao là đại lý chính thức của PVI, địa chỉ công ty em là 8A Huỳnh Lan Khanh Phường 2 Quận Tân Bình. Với lại')
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]  
class ActionUnbelieve04(Action):
    def name(self):
        return "action_unbelieve04"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ em hiểu. Nếu A/C đồng ý mua thì sau cuộc gọi này, nhân viên bên em sẽ mang đơn đăng kí tham gia đến cho A/C kí trực tiếp ạ, nên A/C cứ yên tâm. Nhân tiện đây ')
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]  
class ActionOverAge(Action):
    def name(self):
        return "action_overage"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Rất tiếc cô chú không thể tham gia được sản phẩm đặc biệt này của PVI. Tuy nhiên, cô chú có thể tham gia cho gia đình hoặc nhân viên công ty nếu cố chú là chủ doanh nghiệp ạ. ')
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]    
class ActionLowVoice(FormAction):    
    def name(self):
        return "action_low_voice_form"
    @staticmethod
    def required_slots(tracker)-> List[Text]:
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
        result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=30),
                                        name="first_remind",
                                        kill_on_user_message=True))
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
        result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=30),
                                        name="first_remind",
                                        kill_on_user_message=True))
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
            return[result,FollowupAction("step2_form")]
        elif tracker.get_slot("health_insurance") == True:
            return[result,FollowupAction("action_already_medical01")]
        elif tracker.get_slot("boss2") == True:
            return[result,FollowupAction("already_had02_form")]
        else:
            return[result,FollowupAction("action_family_deny")]
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
        result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=30),
                                        name="first_remind",
                                        kill_on_user_message=True))
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
        result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=30),
                                        name="first_remind",
                                        kill_on_user_message=True))
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
class FAQ01(Action):
    def name(self):
        return "acation_FAQ01"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Dạ em hiểu. Nếu A/C đồng ý mua thì sau cuộc gọi này, nhân viên bên em sẽ mang đơn đăng kí tham gia đến cho A/C kí trực tiếp ạ, nên A/C cứ yên tâm. Nhân tiện đây ')
        return []
class FAQ02(Action):
    def name(self):
        return "acation_FAQ02"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Chỉ ngày hôm nay Anh Chị là KH may mắn được bên em lựa chọn để mang đến lời đề nghị đặc biệt từ PVI, công ty bảo hiểm uy tín trên thị trường. Mặc dù giá thị trường là 5 triệu đồng, nhưng hôm nay anh chị có thể sở hữu gói bảo hiểm này khoảng 1 triệu đồng thôi ạ.')
        return []
class FAQ03(Action):
    def name(self):
        return "acation_FAQ03"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Với gói lựa chọn, Anh Chị sẽ có thêm quyền lợi là nhận được 125 triệu đồng tiền mặt cho một chẩn đoán ung thư')
        return []
class FAQ04(Action):
    def name(self):
        return "acation_FAQ04"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Nó cũng đơn giản như thủ tục của Anh Chị vậy, chỉ cần trả lời 4 câu hỏi sức khỏe của người thân gia đình mình và nhân viên bên em sẽ đến nhà anh chỉ để thu phí cùng lúc cho cả gia đình luôn ạ!')
        return []
class FAQ05(Action):
    def name(self):
        return "acation_FAQ05"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message('Các hạn mức gói cao hơn thì sẽ được hưởng mức quyền lợi cao hơn, ví dụ như gói Kim Cương tổng quyền lợi bảo hiểm là 500 triệu đồng cho nội trú và phẫu thuật')
        return []        
class MyReminder(Action):
    def name(self):
        return 'my_reminder'
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_template('utter_remind',tracker)
        return [Form(None),SlotSet('required_slots',None),FollowupAction('step2_form')]   

class BeginForm(FormAction):
    def name(self):
        return 'begin_form'
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return ["number_insurance","people"]
    def slot_mappings(self):
        return{
            "number_insurance": [
                self.from_entity(entity="number_insurance",not_intent="chichat"),
                self.from_text()
            ],
            "people":[
                self.from_entity(entity="people",not_intent="chichat"),
                self.from_text()
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=30),
                                        name="my_reminder",
                                        kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
            value = tracker.latest_message["entities"] 
            if not value:
                print("''''")
                text = tracker.latest_message.get("text")
                result.append(SlotSet(slot_to_fill,text))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
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
        dispatcher.utter_template("utter_ask_end_step1",tracker)
        return []

class Step2Form(FormAction):
    def name(self):
        return 'step2_form'
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return ["start02","start03","start04"]
    def slot_mappings(self):
        return{
            "start02": [
                self.from_text()
            ],
            "start03": [
                self.from_text()
            ],
            "start04": [
                self.from_intent(intent="affirm",value= True),
                self.from_intent(intent="deny",value= False)
            ],
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=30),
                                        name="my_reminder",
                                        kill_on_user_message=True))
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
        dispatcher.utter_template('utter_start05',tracker)
        if tracker.get_slot('start04') == True:
            return [result,FollowupAction('health_form')]
        else:
            dispatcher.utter_message("Vâng em xin chào anh/chị")
            return []
class HealthForm(FormAction):
    def name(self):
        return 'health_form'
    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return["health01","health02","health03","health04"]
    def slot_mappings(self):
        return {
            "health01": [
                self.from_intent(intent="affirm",value= True),
                self.from_intent(intent="deny",value= False)
            ],
            "health02": [
                self.from_intent(intent="affirm",value= True),
                self.from_intent(intent="deny",value= False)
            ],
            "health03": [
                self.from_intent(intent="affirm",value= True),
                self.from_intent(intent="deny",value= False)
            ],
            "health04": [
                self.from_intent(intent="affirm",value= True),
                self.from_intent(intent="deny",value= False)
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=30),
                                        name="my_reminder",
                                        kill_on_user_message=True))
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
        if tracker.get_slot('health01') == True or tracker.get_slot('health02') == True or tracker.get_slot('health03') == True or tracker.get_slot('health04') == True:
            return [result,FollowupAction('sub_health_form')]
        else :
            dispatcher.utter_message('Cảm ơn Anh/Chị đã trả lời các câu hỏi. Em xin xác nhận ở thời điểm hiện tại, tình hình sức khoẻ Anh/Chị là rất tốt.Bên em sẽ tiến hành các văn bản khai báo sức khỏe chính thức sau. Trước tiên, em xin phép giới thiệu chi tiết gói sản phẩm.')
            dispatcher.utter_template('utter_step06',tracker)
            return [result,FollowupAction('additional_form')]
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
        result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=30),
                                        name="first_remind",
                                        kill_on_user_message=True))
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
        dispatcher.utter_template('utter_step06',tracker)  
        return [result,FollowupAction('additional_form')]
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
        result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=30),
                                        name="first_remind",
                                        kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
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
        if tracker.get_slot("bad_sick") == False:
            dispatcher.utter_message("Em cám ơn Anh/Chị đã dành thời gian trao đổi với em. Đồng thời em cũng rất tiếc vì thời điểm này cty vẫn chưa thể cung cấp được gói bảo hiểm phù hợp với Anh/Chị. Em rất hy vọng được phục vụ Anh/Chị với những sản phẩm khác trong tương lai")
            return[]
        else:
            dispatcher.utter_message("Các câu hỏi trên đây chỉ dùng để tham khảo về tình hình sức khoẻ hiện tại của Anh/Chị, chưa phải là văn bản chính thức.\nEm nhận thấy Anh/Chị đang rất quan tâm về sản phẩm này, nhân viên bên em sẽ đến tận nơi của anh chị để hỗ trợ hoàn tất bảng câu hỏi sức khoẻ. Anh/Chị vui lòng điền đầy đủ thông tin và kí tên xác nhận.\nNhưng trước tiên, em xin phép giới thiệu chi tiết gói sản phẩm.")
            dispatcher.utter_template('utter_step06',tracker)  
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
                self.from_intent(intent='deny',value= False)
            ],
            "addition02": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ],
            "addition03": [
                self.from_intent(intent='affirm',value= True),
                self.from_intent(intent='deny',value= False)
            ]
        }
    def validate(self, dispatcher, tracker, domain):
        result = []
        result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=30),
                                        name="first_remind",
                                        kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))
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
        dispatcher.utter_message('Em xin lưu ý, kể từ khi bắt đầu ký tên và đóng phí thì bảo hiểm này sẽ có hiệu lực sau 30 ngày cho ốm bệnh thông thường, sau 90 ngày cho bệnh liên quan đến ung thư và sau 1 năm cho bệnh có sẵn và mãn tính.')
        return []
