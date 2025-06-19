# evaluation_questions.py (MODIFIED with full descriptive scales)

"""
This file contains the list of subjective evaluation questions
to be asked at the end of the conversation, now with fully descriptive scales.
"""

EVALUATION_QUESTIONS = [
    {
        "id": "begripsnauwkeurigheid",
        "text": "Tot slot, een paar vragen over uw ervaring. Hoe goed heeft de chatbot de kernonderwerpen die u noemde herkend?",
        "scale_labels": {
            "1": "Niet goed",
            "2": "Matig",
            "3": "Voldoende",
            "4": "Goed",
            "5": "Perfect"
        }
    },
    {
        "id": "relevantie_vervolgvragen",
        "text": "Dank u. En hoe relevant waren de vervolgvragen die gesteld werden op basis van uw antwoorden?",
        "scale_labels": {
            "1": "Niet relevant",
            "2": "Weinig relevant",
            "3": "Redelijk relevant",
            "4": "Relevant",
            "5": "Zeer relevant"
        }
    },
    {
        "id": "vrijheid_meningsuiting",
        "text": "Helder. Gaf dit gesprek u de ruimte om uw gedachten vrij en volledig te uiten?",
        "scale_labels": {
            "1": "Helemaal niet",
            "2": "Beperkt",
            "3": "Neutraal",
            "4": "Grotendeels wel",
            "5": "Volledig de ruimte"
        }
    },
    {
        "id": "algehele_effectiviteit",
        "text": "Bijna klaar. Hoe effectief was dit gesprek in het helpen delen van uw feedback?",
        "scale_labels": {
            "1": "Niet effectief",
            "2": "Weinig effectief",
            "3": "Redelijk effectief",
            "4": "Effectief",
            "5": "Zeer effectief"
        }
    },
    {
        "id": "vertrouwen_veiligheid",
        "text": "Laatste vraag: Voelde u zich veilig en op uw gemak tijdens het delen van uw feedback?",
        "scale_labels": {
            "1": "Onveilig",
            "2": "Weinig vertrouwen",
            "3": "Neutraal",
            "4": "Vertrouwd",
            "5": "Volledig veilig"
        }
    }
]