# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import datetime
import re
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict

class ActionProcessarHorarioCampus(Action):
    def name(self) -> Text:
        return "action_processar_horario_campus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        now = datetime.datetime.now()

        abrira_final_de_semana = "O campus abrirá na próxima segunda-feira, às 7 horas. O seu horário de funcionamento é de segunda a sexta, das 7h às 23h30."
        abrira_hoje = "O campus abrirá hoje, às 7 horas. O seu horário de funcionamento é de segunda a sexta, das 7h às 23h30."
        abrira_amanha = "O campus abrirá amanhã, às 7 horas. O seu horário de funcionamento é de segunda a sexta, das 7h às 23h30."
        aberto_agora = "O campus está aberto agora, até 23h30. O seu horário de funcionamento é de segunda a sexta, das 7h às 23h30."

        if now.weekday() == 5 or now.weekday() == 6:
            dispatcher.utter_message(text=abrira_final_de_semana)
            return []
        
        opening_time = datetime.time(7, 0)
        closing_time = datetime.time(23, 30)
        
        current_time = now.time()
        
        if current_time >= closing_time:
            if now.weekday() == 4:
                dispatcher.utter_message(text=abrira_final_de_semana)
                return []
            dispatcher.utter_message(text=abrira_amanha)
            return []
        elif current_time < opening_time:
            dispatcher.utter_message(text=abrira_hoje)
            return []
        
        dispatcher.utter_message(text=aberto_agora)

        return []

class ActionEnviarRequererDocumento(Action):
    def name(self) -> Text:
        return "action_enviar_requerer_documento"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        documento = tracker.get_slot("documento")
        print("Documento: " + documento)

        tipo_documento = tracker.get_slot("tipo_documento")
        print("Tipo de documento: " + tipo_documento)
        
        if documento == "atestado_matricula":
            documento = "atestado de matrícula"
        elif documento == "atestado_frequencia":
            documento = "atestado de frequência"
        else:
            dispatcher.utter_message(text=f"Desculpe, não consegui entender que tipo de documento você quer. Você poderia tentar de novo?")
            return
        
        if tipo_documento == "digital":
            dispatcher.utter_message(text=f"Certo. Para emitir o seu {documento} a partir do SIGAA, siga os passos abaixo:")
            dispatcher.utter_message(text=f"- Primeiro acesse o [SIGAA](https://sigaa.ifsc.edu.br) utilizando seu login e senha; Ao acessar o SIGAA, no menu superior, clique em \"Ensino\" e, em seguida, em \"{documento}\".")
            dispatcher.utter_message(text=f"- Então,  o seu {documento} será aberto em uma nova janela. Você pode imprimi-lo ou salvá-lo através do botão “imprimir” no final da página.")
        else:
            dispatcher.utter_message(text=f"Beleza. Para receber o seu {documento} impresso com carimbo e assinatura, você deve ir à secretaria do IFSC Campus Gaspar pessoalmente. O horário de atendimento é de segunda a sexta-feira, das 7h às 23h30.")

        return [SlotSet("documento", None), SlotSet("tipo_documento", None)]

class ValidateRequererDocumentoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_requerer_documento_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Text]:
        additional_slots = ["tipo_documento"]
        if tracker.slots.get("tipo_documento") == "digital":
            additional_slots.append("possui_conta")

        return additional_slots + domain_slots

class ActionEnviarChegadaTardia(Action):
    def name(self) -> Text:
        return "action_enviar_chegada_tardia"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        nome = tracker.get_slot("nome")
        print("Nome: " + nome)

        turma = tracker.get_slot("turma").lower()
        turma = turma.replace("informática", "I")
        turma = turma.replace("informatica", "I")
        turma = turma.replace("química", "Q")
        turma = turma.replace("quimica", "Q")
        turma = turma.replace(" ", "").upper()

        if not bool(re.search(r"[IQ][1-6]", turma)):
            dispatcher.utter_message(text=f"Desculpe, não consegui entender a sua turma. Você poderia tentar de novo?")
            return [SlotSet("turma", None)]
        
        print("Turma: " + turma)

        horario = datetime.datetime.now().strftime("%H:%M")

        dispatcher.utter_message(text=f"Ótimo. Registrei uma chegada tardia em nome de {nome} da turma {turma} às {horario}. Certifique-se de retirar o comprovante na secretaria.")

        return []

class ValidateChegadaTardiaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_chegada_tardia_form"

    def validate_turma(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        turma = slot_value.lower()
        # turma = turma.replace("informática", "I")
        # turma = turma.replace("informatica", "I")
        # turma = turma.replace("química", "Q")
        # turma = turma.replace("quimica", "Q")
        # turma = turma.replace(" ", "").upper()

        # if not bool(re.search(r"[IQ][1-6]", turma)):
        #     dispatcher.utter_message(text=f"Desculpe, não consegui entender a sua turma. Você poderia tentar de novo?")
        #     return {"turma": None}

        return {"turma": turma}