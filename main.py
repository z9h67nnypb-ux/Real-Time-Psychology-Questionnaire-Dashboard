import requests
import streamlit as st
import json
from datetime import datetime as dt
from abc import ABC, abstractmethod
import time

INTERVAL = 20
LIMIT = 20

API_KEY = ""

FORMS = {
    "BDI": "0Q6YdQ",
    "BPD": "zxDvJ0",
    "CORE_OM": "obMYr1",
    "GAD": "VL5Xka",
    "OCD" : "81QOyk"
}
NAME_QUESTION_IDS = {
    "BDI": "KMx7Pg",
    "BPD": "XeoV8L",
    "CORE_OM": "qbGxog",
    "GAD": "OAXpoY",
    "OCD": "24PKvL"
}

BIRTH_NUMBER_QUESTION_IDS = {
    "BDI": "42rKZX",
    "BPD": "rlPoeN",
    "CORE_OM": "OAG7R7",
    "GAD": "GrlRMp",
    "OCD": "EPWx24"
}

INSURENCE_CODE_QUESTION_IDS = {
    "BDI": "OAG7Ng",
    "BPD": "GrlRPk",
    "CORE_OM": "xdYJqr",
    "GAD": "24PKWj",
    "OCD": "xdYJyy"
}

NUMBER_OF_QUESTIONS = {
    "BDI": 21,
    "BPD": 9,
    "CORE_OM": 34,
    "GAD": 7,
    "OCD": 10
}

CORE_OM_QUESTION_CLASSES = "FPFWPRFPRFPFPWPRWPFPFRPRFFPPFPWFFR"
fCount = rCount = wCount = pCount = 0

fCount = CORE_OM_QUESTION_CLASSES.count('F')
rCount = CORE_OM_QUESTION_CLASSES.count('R')
wCount = CORE_OM_QUESTION_CLASSES.count('W')
pCount = CORE_OM_QUESTION_CLASSES.count('P')

wPercentileTable = [
    [ 5, 0.00, 0.75, 0.25, 0.75, 0.25, 0.75],
    [10, 0.25, 1.50, 0.25, 1.00, 0.25, 1.00],
    [15, 0.50, 1.75, 0.36, 1.01, 0.50, 1.50],
    [20, 0.50, 2.00, 0.50, 1.35, 0.50, 1.75],
    [25, 0.50, 2.00, 0.50, 1.50, 0.50, 1.75],
    [30, 0.75, 2.25, 0.50, 1.75, 0.75, 2.00],
    [35, 0.75, 2.25, 0.75, 1.75, 0.75, 2.25],
    [40, 0.80, 2.50, 0.75, 2.00, 0.75, 2.25],
    [45, 1.00, 2.50, 0.75, 2.00, 1.00, 2.50],
    [50, 1.00, 2.75, 1.00, 2.25, 1.00, 2.50],
    [55, 1.25, 2.75, 1.00, 2.46, 1.25, 2.70],
    [60, 1.25, 2.75, 1.00, 2.50, 1.25, 2.75],
    [65, 1.25, 3.00, 1.25, 2.75, 1.25, 2.75],
    [70, 1.50, 3.00, 1.25, 2.75, 1.50, 3.00],
    [75, 1.50, 3.00, 1.25, 2.75, 1.50, 3.00],
    [80, 1.75, 3.25, 1.50, 2.90, 1.70, 3.00],
    [85, 1.75, 3.50, 1.75, 3.00, 1.75, 3.25],
    [90, 2.25, 3.75, 1.75, 3.50, 2.00, 3.50],
    [95, 2.50, 3.75, 2.21, 3.50, 2.50, 3.75],
   [100, 3.25, 4.00, 3.50, 3.75, 3.50, 4.00]
]

pPercentileTable = [
    [ 5, 0.24, 0.70, 0.26, 0.86, 0.25, 0.82],
    [10, 0.33, 1.15, 0.36, 0.98, 0.33, 1.08],
    [15, 0.39, 1.50, 0.42, 1.25, 0.42, 1.42],
    [20, 0.42, 1.67, 0.55, 1.45, 0.50, 1.60],
    [25, 0.50, 1.83, 0.58, 1.65, 0.58, 1.75],
    [30, 0.67, 1.92, 0.67, 1.84, 0.67, 1.92],
    [35, 0.75, 2.08, 0.75, 1.95, 0.75, 2.00],
    [40, 0.77, 2.25, 0.83, 2.00, 0.83, 2.08],
    [45, 0.92, 2.38, 1.03, 2.08, 0.92, 2.25],
    [50, 1.00, 2.50, 1.08, 2.17, 1.00, 2.42],
    [55, 1.08, 2.62, 1.17, 2.33, 1.08, 2.50],
    [60, 1.17, 2.82, 1.18, 2.42, 1.17, 2.74],
    [65, 1.25, 2.92, 1.25, 2.71, 1.25, 2.83],
    [70, 1.38, 3.00, 1.34, 2.83, 1.33, 2.93],
    [75, 1.50, 3.08, 1.50, 2.94, 1.50, 3.00],
    [80, 1.67, 3.20, 1.50, 3.00, 1.67, 3.15],
    [85, 1.86, 3.32, 1.67, 3.16, 1.83, 3.25],
    [90, 2.08, 3.50, 1.83, 3.28, 1.99, 3.42],
    [95, 2.42, 3.63, 2.06, 3.58, 2.41, 3.60],
   [100, 3.75, 3.92, 3.08, 4.00, 3.75, 4.00],
]

fPercentileTable = [
    [5, 0.17, 0.73, 0.08, 0.70, 0.17, 0.73],
    [10, 0.25, 0.90, 0.25, 0.98, 0.25, 0.97],
    [15, 0.33, 1.08, 0.33, 1.09, 0.33, 1.08],
    [20, 0.42, 1.22, 0.42, 1.32, 0.42, 1.25],
    [25, 0.50, 1.33, 0.56, 1.50, 0.50, 1.42],
    [30, 0.58, 1.50, 0.67, 1.58, 0.67, 1.58],
    [35, 0.69, 1.67, 0.75, 1.70, 0.75, 1.67],
    [40, 0.77, 1.75, 0.83, 1.75, 0.83, 1.75],
    [45, 0.83, 1.83, 0.86, 1.92, 0.83, 1.83],
    [50, 0.92, 1.92, 0.92, 1.92, 0.92, 1.92],
    [55, 1.00, 1.92, 1.00, 2.07, 1.00, 1.92],
    [60, 1.08, 2.00, 1.08, 2.17, 1.08, 2.08],
    [65, 1.17, 2.17, 1.16, 2.21, 1.17, 2.17],
    [70, 1.17, 2.22, 1.18, 2.25, 1.17, 2.25],
    [75, 1.25, 2.42, 1.27, 2.35, 1.25, 2.33],
    [80, 1.33, 2.50, 1.42, 2.50, 1.33, 2.50],
    [85, 1.50, 2.65, 1.50, 2.58, 1.50, 2.58],
    [90, 1.67, 2.75, 1.58, 2.67, 1.66, 2.70],
    [95, 1.93, 3.08, 1.98, 2.97, 1.92, 3.00],
    [100, 2.42, 3.42, 2.58, 3.08, 2.58, 3.42],
]

rPercentileTable = [
    [5, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    [10, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    [15, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    [20, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    [25, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    [30, 0.00, 0.17, 0.00, 0.17, 0.00, 0.17],
    [35, 0.00, 0.17, 0.00, 0.17, 0.00, 0.17],
    [40, 0.00, 0.17, 0.00, 0.17, 0.00, 0.17],
    [45, 0.00, 0.27, 0.00, 0.33, 0.00, 0.33],
    [50, 0.00, 0.33, 0.00, 0.42, 0.00, 0.33],
    [55, 0.00, 0.33, 0.00, 0.50, 0.00, 0.47],
    [60, 0.00, 0.50, 0.13, 0.53, 0.00, 0.50],
    [65, 0.00, 0.50, 0.17, 0.76, 0.00, 0.50],
    [70, 0.00, 0.50, 0.17, 0.83, 0.00, 0.67],
    [75, 0.17, 0.67, 0.33, 0.88, 0.17, 0.83],
    [80, 0.17, 0.83, 0.33, 1.10, 0.17, 1.00],
    [85, 0.17, 1.00, 0.42, 1.33, 0.33, 1.17],
    [90, 0.33, 1.17, 0.50, 1.67, 0.33, 1.40],
    [95, 0.52, 1.80, 0.97, 2.33, 0.67, 2.00],
    [100, 2.33, 2.67, 2.33, 3.83, 2.33, 3.83],
]

no_rPercentileTable = [
    [5, 0.25, 0.79, 0.25, 0.85, 0.25, 0.88],
    [10, 0.36, 1.16, 0.36, 1.13, 0.36, 1.14],
    [15, 0.39, 1.43, 0.44, 1.32, 0.43, 1.37],
    [20, 0.50, 1.59, 0.49, 1.43, 0.50, 1.51],
    [25, 0.57, 1.71, 0.56, 1.53, 0.57, 1.68],
    [30, 0.68, 1.82, 0.61, 1.69, 0.68, 1.81],
    [35, 0.75, 1.93, 0.79, 1.84, 0.75, 1.91],
    [40, 0.83, 2.01, 0.90, 1.96, 0.86, 2.00],
    [45, 0.93, 2.13, 0.96, 2.04, 0.93, 2.11],
    [50, 0.96, 2.25, 1.00, 2.13, 0.98, 2.21],
    [55, 1.04, 2.37, 1.07, 2.21, 1.07, 2.29],
    [60, 1.14, 2.50, 1.10, 2.29, 1.14, 2.40],
    [65, 1.25, 2.57, 1.25, 2.41, 1.25, 2.54],
    [70, 1.29, 2.67, 1.25, 2.57, 1.29, 2.61],
    [75, 1.36, 2.75, 1.32, 2.60, 1.36, 2.71],
    [80, 1.46, 2.86, 1.41, 2.69, 1.43, 2.78],
    [85, 1.62, 2.96, 1.52, 2.75, 1.61, 2.89],
    [90, 1.86, 3.09, 1.66, 2.94, 1.82, 3.04],
    [95, 2.15, 3.38, 1.89, 3.11, 2.11, 3.33],
    [100, 2.86, 3.46, 2.93, 3.46, 2.93, 3.46],
]

wholePercentileTable = [
    [5, 0.21, 0.65, 0.21, 0.70, 0.21, 0.72],
    [10, 0.29, 1.02, 0.29, 0.94, 0.29, 0.99],
    [15, 0.34, 1.18, 0.37, 1.12, 0.35, 1.16],
    [20, 0.41, 1.37, 0.44, 1.21, 0.44, 1.27],
    [25, 0.47, 1.44, 0.49, 1.28, 0.48, 1.44],
    [30, 0.56, 1.54, 0.53, 1.45, 0.56, 1.52],
    [35, 0.62, 1.59, 0.68, 1.60, 0.62, 1.61],
    [40, 0.68, 1.69, 0.76, 1.71, 0.71, 1.72],
    [45, 0.76, 1.88, 0.82, 1.80, 0.76, 1.85],
    [50, 0.85, 1.97, 0.85, 1.85, 0.85, 1.91],
    [55, 0.88, 2.06, 0.88, 1.88, 0.88, 1.97],
    [60, 0.94, 2.11, 0.91, 1.97, 0.94, 2.09],
    [65, 1.05, 2.24, 1.03, 2.09, 1.03, 2.18],
    [70, 1.09, 2.29, 1.03, 2.17, 1.09, 2.26],
    [75, 1.16, 2.32, 1.13, 2.26, 1.15, 2.32],
    [80, 1.24, 2.47, 1.24, 2.33, 1.24, 2.44],
    [85, 1.38, 2.64, 1.32, 2.47, 1.35, 2.55],
    [90, 1.56, 2.75, 1.49, 2.71, 1.53, 2.74],
    [95, 1.86, 2.88, 1.68, 2.96, 1.79, 2.89],
    [100, 2.35, 3.26, 2.82, 3.32, 2.82, 3.32],
]

percTableTags = {
    "W" : wPercentileTable,
    "P" : pPercentileTable,
    "F" : fPercentileTable,
    "R" : rPercentileTable,
    "no_R" : no_rPercentileTable
}

def find_percentile(table, col_index, target_value):
    last_valid_percentile = None
    
    for row in table:
        if row[col_index] <= target_value:
            last_valid_percentile = row[0]
        else: break
            
    return last_valid_percentile

# --- THE PARENT CLASS ---
class Questionnaire(ABC):
    def __init__(self, submission, form_key):
        self.raw_submission = submission

        self.patient_name = "Chyba"
        self.total_score = 0
        self.average_score = 0.0
        self.birth_number = "Chyba"
        self.insurence_code = "Chyba"
        
        raw_date = submission.get("submittedAt")
        if raw_date:
            dt_obj = dt.strptime(raw_date[:19], "%Y-%m-%dT%H:%M:%S")
            self.date = dt_obj.strftime("%d. %m. %Y")
        else:
            self.date = "Neznámé datum"

        self.name_field_id = NAME_QUESTION_IDS.get(form_key)
        self._process_responses(submission.get("responses", []), form_key)

    def _process_responses(self, responses, form_key):
        current_sum = 0
        for f in responses:
            # Look for the name
            if f.get("questionId") == self.name_field_id:
                self.patient_name = f.get("answer", "Chyba")
            elif f.get("questionId") == BIRTH_NUMBER_QUESTION_IDS[form_key]:
                self.birth_number = f.get("answer", "Chyba")
            elif f.get("questionId") == INSURENCE_CODE_QUESTION_IDS[form_key]:
                self.insurence_code = f.get("answer", "Chyba")
            # Sum up any numeric answers
            elif isinstance(f.get("answer"), (int, float)):
                current_sum += int(f["answer"])
        
        self.total_score = current_sum
        self.processDetails()

    @abstractmethod
    def processDetails(self):
        pass

    @abstractmethod
    def interpret(self):
        pass

#----------------------------------------------------------------

class BdiSubmission(Questionnaire):
    def __init__(self, submission):
        super().__init__(submission, "BDI")
        self.max_score = NUMBER_OF_QUESTIONS["BDI"] * 3

    def processDetails(self):
        self.average_score = round(self.total_score / NUMBER_OF_QUESTIONS["BDI"], 2)

    def interpret(self):
        if(self.total_score <= 10): return "Výsledek spadá do pásma minimální depresivní symptomatiky. V současnosti nejsou přítomny známky klinicky významné deprese, přesto je vhodné nadále sledovat vývoj nálady v čase."
        if(self.total_score <= 20): return "Výsledek naznačuje přítomnost mírného depresivního ladění. Intenzita symptomů je nízká, nicméně je vhodné sledovat jejich vývoj a případný dopad na každodenní fungování."
        if(self.total_score <= 30): return "Výsledek svědčí pro přítomnost středně těžké depresivní symptomatiky. Obtíže mají pravděpodobně klinickou závažnost a mohou negativně ovlivňovat každodenní fungování."
        return "BDI-II svědčí pro přítomnost výrazné depresivní symptomatiky těžké intenzity. Obtíže pravděpodobně významně zasahují do každodenního fungování a je vyjádřen somatický syndrom. Projevuje se ranními pesimy, výraznou anhedonií (ztráta radosti), předčasným probouzením, úbytkem hmotnosti a zpomalením."
    
class BpdSubmission(Questionnaire):
    def __init__(self, submission):
        super().__init__(submission, "BPD")
        self.max_score = NUMBER_OF_QUESTIONS["BPD"] * 2

    def processDetails(self):
        self.average_score = round(self.total_score / NUMBER_OF_QUESTIONS["BPD"], 2)

    def interpret(self):
        return ""
    

class CoreOmSubmission(Questionnaire):
    def __init__(self, submission):
        super().__init__(submission, "CORE_OM")
        self.max_score = NUMBER_OF_QUESTIONS["CORE_OM"] * 4


    def processDetails(self):
        self.wSum = self.pSum = self.fSum = self.rSum = 0
        self.average_score = round(self.total_score / NUMBER_OF_QUESTIONS["CORE_OM"], 2)
        responses = self.raw_submission.get("responses", [])
        counter = 0
        for i in range(len(responses)):
            resp = responses[i]
            if (isinstance(resp.get("answer"), (int, float)) and resp.get("questionId") != INSURENCE_CODE_QUESTION_IDS["CORE_OM"]):
                #print(str(counter) + "-------------------------------------")
                qType = CORE_OM_QUESTION_CLASSES[counter]
                if(qType == 'F'): self.fSum += int(resp["answer"])
                elif(qType == 'R'): self.rSum += int(resp["answer"])
                elif(qType == 'W'): self.wSum += int(resp["answer"])
                elif(qType == 'P'): self.pSum += int(resp["answer"])
                counter += 1
            elif(resp.get("questionId") == "jBloER"):
                self.gender = resp["answer"][0]

        self.wAvg = round(self.wSum / wCount,2)
        self.rAvg = round(self.rSum / rCount,2)
        self.fAvg = round(self.fSum / fCount,2)
        self.pAvg = round(self.pSum / pCount,2)
        self.minusRSum = round(self.total_score - self.rSum,2)
        self.minusRAvg = round(self.minusRSum / (NUMBER_OF_QUESTIONS["CORE_OM"] - rCount),2)


        #women,       men,    other
        #non-clinical, clinical 
        #percentiles

        genderColumn = 1
        if(self.gender == "Muž"): genderColumn = 3
        elif(self.gender == "Další"): genderColumn = 5

        self.pPerc = find_percentile(pPercentileTable, genderColumn, self.pAvg)
        self.pPercClinical = find_percentile(pPercentileTable, genderColumn + 1, self.pAvg)
        self.wPerc = find_percentile(wPercentileTable, genderColumn, self.wAvg)
        self.wPercClinical = find_percentile(wPercentileTable, genderColumn + 1, self.wAvg)
        self.fPerc = find_percentile(fPercentileTable, genderColumn, self.fAvg)
        self.fPercClinical = find_percentile(fPercentileTable, genderColumn + 1, self.fAvg)
        self.rPerc = find_percentile(rPercentileTable, genderColumn, self.rAvg)
        self.rPercClinical = find_percentile(rPercentileTable, genderColumn + 1, self.rAvg)
        self.no_rPerc = find_percentile(no_rPercentileTable, genderColumn, self.minusRAvg)
        self.no_rPercClinical = find_percentile(no_rPercentileTable, genderColumn + 1, self.minusRAvg)
        self.wholePerc = find_percentile(wholePercentileTable, genderColumn, self.average_score)
        self.wholePercClinical = find_percentile(wholePercentileTable, genderColumn + 1, self.average_score)

    def interpret(self):
        return ""



class GadSubmission(Questionnaire):
    def __init__(self, submission):
        super().__init__(submission, "GAD")
        self.max_score = NUMBER_OF_QUESTIONS["GAD"] * 3

    def processDetails(self):
        self.average_score = round(self.total_score / NUMBER_OF_QUESTIONS["GAD"], 2)

    def interpret(self):
        if(self.total_score <= 4): return "Skóre odpovídá běžné míře napětí, které je přiměřené situaci. Úzkostné prožívání je spíše ojedinělé, krátkodobé a bez významného dopadu na každodenní fungování. Tělesné projevy se mohou objevit sporadicky, ale nepůsobí výrazné obtíže."
        if(self.total_score <= 9): return "Výsledek svědčí pro přítomnost mírné úzkostné symptomatiky. Obavy jsou častější a mohou být hůře ovladatelné, objevuje se zvýšené napětí, podrážděnost či lehké potíže se spánkem. Úzkost může mírně snižovat koncentraci nebo efektivitu, avšak celkové fungování zůstává většinou zachováno."
        if(self.total_score <= 14): return "Skóre poukazuje na klinicky významnější úzkostné prožívání. Obavy jsou výraznější, přetrvávající a obtížně kontrolovatelné. Často jsou přítomny somatické projevy, jako je vnitřní neklid, svalové napětí, bušení srdce či gastrointestinální obtíže. Úzkost již znatelně zasahuje do pracovního, studijního nebo sociálního fungování."
        return "Výsledek odpovídá závažné úzkostné symptomatice. Úzkost je intenzivní, všudypřítomná a obtížně zvládnutelná. Výrazné jsou i tělesné projevy a může docházet k vyhýbavému chování či omezení běžných aktivit. Obtíže významně narušují každodenní fungování a vyžadují odbornou intervenci."


class OcdSubmission(Questionnaire):
    def __init__(self, submission):
        super().__init__(submission, "OCD")
        self.max_score = NUMBER_OF_QUESTIONS["OCD"] * 3

    def processDetails(self):
        self.average_score = round(self.total_score / NUMBER_OF_QUESTIONS["OCD"], 2)

    def interpret(self):
        if(self.total_score <= 6): return "bez významných OCD symptomů"
        if(self.total_score <= 12): return "lehké obsedantně-kompulzivní rysy"
        if(self.total_score <= 19): return "středně výrazné OCD symptomy – doporučeno další klinické posouzení"
        return "výrazné OCD symptomy – doporučeno odborné vyšetření"


FORM_CLASS_MAP = {
    "BDI": BdiSubmission,
    "BPD": BpdSubmission,
    "CORE_OM": CoreOmSubmission,
    "GAD": GadSubmission,
    "OCD": OcdSubmission
}

#---------------------------------------------------------------------------------
        

def three_row(label, total, avg):
            c1, c2, c3 = st.columns([2,1,1])
            c1.write(f"**{label}**")
            c2.write(total)
            c3.write(avg)

def four_row(label, total, avg, percentile):
            c1, c2, c3, c4 = st.columns([2,1,1,1])
            c1.write(f"**{label}**")
            c2.write(total)
            c3.write(avg)
            c4.write(percentile)

#DIALOG CARD
@st.dialog(" ")
def show_details(submission_obj: Questionnaire, form_key):
    st.header(f"{submission_obj.patient_name}  |  {form_key}")
    st.write(f"Datum odevzdání: {submission_obj.date}")
    st.write(f"Rodné číslo: {submission_obj.birth_number}")
    st.write(f"Kód pojišťovny: {submission_obj.insurence_code}")
    st.divider()
    
    if(isinstance(submission_obj, CoreOmSubmission)): 
        four_row("Kategorie", "Celkem", "Průměr", "Percentil (Nekl./Kl.)")
        four_row(f"Skóre (max = {submission_obj.max_score})", submission_obj.total_score, submission_obj.average_score, f"{submission_obj.wholePerc} / {submission_obj.wholePercClinical}")
    else: 
        three_row("Kategorie", "Celkem", "Průměr")
        three_row(f"Skóre (max = {submission_obj.max_score})", submission_obj.total_score, submission_obj.average_score)
    
    if isinstance(submission_obj, CoreOmSubmission):
        four_row("W (Duševní pohoda)", submission_obj.wSum, submission_obj.wAvg, f"{submission_obj.wPerc} / {submission_obj.wPercClinical}")
        four_row("P (Problémy)", submission_obj.pSum, submission_obj.pAvg, f"{submission_obj.pPerc} / {submission_obj.pPercClinical}")
        four_row("F (Fungování)", submission_obj.fSum, submission_obj.fAvg, f"{submission_obj.fPerc} / {submission_obj.fPercClinical}")
        four_row("R (Riziko)", submission_obj.rSum, submission_obj.rAvg, f"{submission_obj.rPerc} / {submission_obj.rPercClinical}")
        four_row("Bez Rizika", submission_obj.minusRSum, submission_obj.minusRAvg, f"{submission_obj.no_rPerc} / {submission_obj.no_rPercClinical}")

    st.divider()
    st.write(submission_obj.interpret())
    
    
    if st.button("Zavřít"):
        st.rerun()


def can_refresh():
    """Checks if we have exceeded 10 manual refreshes in the last 60 seconds."""
    now = time.time()
    st.session_state.refresh_history = [t for t in st.session_state.refresh_history if now - t < 60]
    return len(st.session_state.refresh_history) < 10

# DATA SERVICE
class PatientDataService:
    def __init__(self, api_key):
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.base_url = "https://api.tally.so/forms/{}/submissions"

    
    @st.cache_data(ttl=INTERVAL) 
    def fetch_form_data(_self, form_id): 
        try:
            url = _self.base_url.format(form_id)
            response = requests.get(url, headers=_self.headers, params={"limit": LIMIT})
            if response.status_code == 200:
                #if(form_id =="obMYr1"): print(json.dumps(response.json(), indent = 4))
                return response.json().get("submissions", [])
        except Exception as e:
            st.error(f"Connection Error: {e}")
        return []




# CONFIG
if "api_service" not in st.session_state:
    st.session_state.api_service = PatientDataService(API_KEY)

if "refresh_history" not in st.session_state:
    st.session_state.refresh_history = []

SERVICE = st.session_state.api_service


st.set_page_config(layout="wide", page_title="Dotazníky")

#UI FRAGMENT 
@st.fragment(run_every=INTERVAL)
def live_patient_grid():
    cols = st.columns(len(FORMS))
    
    for i, (form_name, form_id) in enumerate(FORMS.items()):
        with cols[i]:
            st.subheader(form_name)
            raw_submissions = SERVICE.fetch_form_data(form_id) 

            for sub_json in raw_submissions:
                # 1. Instantiate the correct object using our Map
                submission_class = FORM_CLASS_MAP.get(form_name)
                if not submission_class:
                    continue
                
                # This is extremely fast, no need to worry about performance
                obj = submission_class(sub_json)

                # 2. Draw the Card
                with st.container(border=True):
                    col_text, col_btn = st.columns([3, 1])
                    col_text.write(f"**{obj.patient_name}**")
                    col_text.write(f"r.č.: {obj.birth_number}")
                    col_text.write(f"kód pojišťovny: {obj.insurence_code}")
                    col_text.caption(f"{obj.total_score}/{obj.max_score}b. | {obj.date}")
                    
                    # Pass the OBJECT to the dialog function
                    if col_btn.button("👁️", key=f"btn_{sub_json['id']}"):
                        show_details(obj, form_name)

# MAIN FUNCTION
title_col, timer_col = st.columns([2, 1])

with title_col:
    st.title("👩‍⚕️ Dotazníky")

with timer_col:
    info_col, btn_col = st.columns([1,1])
    with info_col:
        st.info("Obnova každých " + str(INTERVAL) + "s.")
    with btn_col:
        if st.button("🔄 Obnovit hned", use_container_width=True):
            if can_refresh():
                st.session_state.refresh_history.append(time.time())
                
                st.cache_data.clear() 
                
                st.toast("Data aktualizována")
                st.rerun()
            else:
                st.error("Příliš mnoho požadavků. Počkejte chvíli.")
live_patient_grid()
