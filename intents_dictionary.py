# 38 个主题（源自 INTENTS 列表）
INTENTS = [
    "uitdaging", "persoonlijke ontwikkeling", "sfeer", "autonomie", "samenwerking",
    "afwisseling", "werk prive balans", "trots", "voldoening", "flexibiliteit",
    "doorgroeien", "veiligheid", "waardering", "plezier", "aanspreken", "aansturing",
    "arbeidsvoorwaarden", "begeleiding", "faciliteiten", "reistijd", "administratie",
    "bureaucratie", "onduidelijke afspraken", "duurt lang", "handhaving regels", "niets",
    "planning", "solistisch werken", "veranderingen", "vergaderen", "werkdruk", "zwaar werk",
    "management", "aandacht", "inhoud werk", "functiematch", "duidelijke processen",
]

# 1. 预设权重（示范：按出现顺序递减，也可自行调整 0.0-1.0）
LABEL_META = {
    # lbl: {
    #     "group": "default",            # 先全部放同组，可按需细分
    #     "weight": round(1 - i / len(INTENTS), 3),   # 1.000 → 0.026
    # }
    # for i, lbl in enumerate(INTENTS)
    "uitdaging": {
        "group": "default",
        "related_labels": {
            "uitdaging": 0.346,
            "persoonlijke ontwikkeling": 0.038,
            "sfeer": 0.038,
            "autonomie": 0.077,
            "samenwerking": 0.115,
            "afwisseling": 0.038,
            "flexibiliteit": 0.038,
            "doorgroeien": 0.077,
            "arbeidsvoorwaarden": 0.038,
            "inhoud werk": 0.192
        }
    },
    "persoonlijke ontwikkeling": {
        "group": "default",
        "related_labels": {
            "uitdaging": 0.012,
            "persoonlijke ontwikkeling": 0.425,
            "sfeer": 0.012,
            "autonomie": 0.1,
            "samenwerking": 0.025,
            "afwisseling": 0.012,
            "werk prive balans": 0.038,
            "voldoening": 0.012,
            "flexibiliteit": 0.075,
            "doorgroeien": 0.05,
            "waardering": 0.012,
            "aanspreken": 0.012,
            "arbeidsvoorwaarden": 0.075,
            "begeleiding": 0.012,
            "faciliteiten": 0.012,
            "werkdruk": 0.012,
            "aandacht": 0.038,
            "inhoud werk": 0.062
        }
    },
    "sfeer": {
        "group": "default",
        "related_labels": {
            "uitdaging": 0.031,
            "persoonlijke ontwikkeling": 0.021,
            "sfeer": 0.278,
            "autonomie": 0.031,
            "samenwerking": 0.309,
            "afwisseling": 0.041,
            "werk prive balans": 0.021,
            "flexibiliteit": 0.01,
            "waardering": 0.052,
            "plezier": 0.062,
            "aansturing": 0.01,
            "arbeidsvoorwaarden": 0.031,
            "planning": 0.01,
            "vergaderen": 0.01,
            "werkdruk": 0.01,
            "management": 0.021,
            "aandacht": 0.01,
            "inhoud werk": 0.041
        }
    },
    "autonomie": {
        "group": "default",
        "related_labels": {
            "uitdaging": 0.014,
            "persoonlijke ontwikkeling": 0.058,
            "sfeer": 0.022,
            "autonomie": 0.413,
            "samenwerking": 0.13,
            "afwisseling": 0.036,
            "werk prive balans": 0.022,
            "flexibiliteit": 0.065,
            "doorgroeien": 0.007,
            "veiligheid": 0.007,
            "waardering": 0.007,
            "plezier": 0.014,
            "aansturing": 0.014,
            "arbeidsvoorwaarden": 0.022,
            "planning": 0.058,
            "veranderingen": 0.014,
            "vergaderen": 0.007,
            "werkdruk": 0.014,
            "aandacht": 0.014,
            "inhoud werk": 0.043,
            "functiematch": 0.007,
            "duidelijke processen": 0.007
        }
    },
    "samenwerking": {
        "group": "default",
        "related_labels": {
            "uitdaging": 0.009,
            "sfeer": 0.034,
            "autonomie": 0.017,
            "samenwerking": 0.427,
            "afwisseling": 0.034,
            "flexibiliteit": 0.017,
            "doorgroeien": 0.009,
            "waardering": 0.026,
            "plezier": 0.017,
            "aanspreken": 0.077,
            "aansturing": 0.009,
            "arbeidsvoorwaarden": 0.009,
            "begeleiding": 0.017,
            "faciliteiten": 0.026,
            "onduidelijke afspraken": 0.077,
            "duurt lang": 0.009,
            "planning": 0.034,
            "veranderingen": 0.026,
            "vergaderen": 0.009,
            "werkdruk": 0.009,
            "management": 0.043,
            "inhoud werk": 0.026,
            "duidelijke processen": 0.043
        }
    },
    "afwisseling": {
        "group": "default",
        "related_labels": {
            "uitdaging": 0.071,
            "persoonlijke ontwikkeling": 0.035,
            "sfeer": 0.024,
            "autonomie": 0.071,
            "samenwerking": 0.129,
            "afwisseling": 0.388,
            "werk prive balans": 0.047,
            "flexibiliteit": 0.012,
            "waardering": 0.024,
            "plezier": 0.047,
            "arbeidsvoorwaarden": 0.024,
            "planning": 0.012,
            "management": 0.012,
            "inhoud werk": 0.106
        }
    },
    "werk prive balans": {
        "group": "default",
        "related_labels": {
            "persoonlijke ontwikkeling": 0.027,
            "sfeer": 0.013,
            "autonomie": 0.04,
            "samenwerking": 0.067,
            "afwisseling": 0.013,
            "werk prive balans": 0.587,
            "voldoening": 0.013,
            "flexibiliteit": 0.107,
            "waardering": 0.013,
            "plezier": 0.013,
            "arbeidsvoorwaarden": 0.04,
            "begeleiding": 0.013,
            "reistijd": 0.013,
            "veranderingen": 0.013,
            "management": 0.013,
            "inhoud werk": 0.013
        }
    },
    "trots": {
        "group": "default",
        "related_labels": {
            "trots": 0.273,
            "voldoening": 0.364,
            "faciliteiten": 0.091,
            "niets": 0.182,
            "inhoud werk": 0.091
        }
    },
    "voldoening": {
        "group": "default",
        "related_labels": {
            "autonomie": 0.045,
            "samenwerking": 0.114,
            "werk prive balans": 0.023,
            "trots": 0.023,
            "voldoening": 0.25,
            "flexibiliteit": 0.023,
            "waardering": 0.068,
            "plezier": 0.136,
            "arbeidsvoorwaarden": 0.045,
            "begeleiding": 0.045,
            "werkdruk": 0.023,
            "aandacht": 0.045,
            "inhoud werk": 0.159
        }
    },
    "flexibiliteit": {
        "group": "default",
        "related_labels": {
            "persoonlijke ontwikkeling": 0.077,
            "autonomie": 0.051,
            "samenwerking": 0.077,
            "afwisseling": 0.026,
            "werk prive balans": 0.026,
            "voldoening": 0.026,
            "flexibiliteit": 0.487,
            "doorgroeien": 0.026,
            "arbeidsvoorwaarden": 0.103,
            "faciliteiten": 0.026,
            "planning": 0.026,
            "werkdruk": 0.026,
            "inhoud werk": 0.026
        }
    },
    "doorgroeien": {
        "group": "default",
        "related_labels": {
            "uitdaging": 0.015,
            "persoonlijke ontwikkeling": 0.108,
            "autonomie": 0.046,
            "samenwerking": 0.031,
            "afwisseling": 0.015,
            "flexibiliteit": 0.031,
            "doorgroeien": 0.508,
            "waardering": 0.062,
            "arbeidsvoorwaarden": 0.138,
            "management": 0.015,
            "aandacht": 0.015,
            "functiematch": 0.015
        }
    },
    "veiligheid": {
        "group": "default",
        "related_labels": {
            "autonomie": 0.333,
            "veiligheid": 0.667
        }
    },
    "waardering": {
        "group": "default",
        "related_labels": {
            "uitdaging": 0.017,
            "persoonlijke ontwikkeling": 0.033,
            "sfeer": 0.033,
            "autonomie": 0.067,
            "samenwerking": 0.1,
            "afwisseling": 0.017,
            "werk prive balans": 0.017,
            "voldoening": 0.083,
            "doorgroeien": 0.017,
            "waardering": 0.4,
            "plezier": 0.017,
            "aansturing": 0.017,
            "arbeidsvoorwaarden": 0.067,
            "begeleiding": 0.017,
            "niets": 0.017,
            "planning": 0.017,
            "aandacht": 0.05,
            "inhoud werk": 0.017
        }
    },
    "plezier": {
        "group": "default",
        "related_labels": {
            "plezier": 0.556,
            "veranderingen": 0.111,
            "inhoud werk": 0.222,
            "duidelijke processen": 0.111
        }
    },
    "aanspreken": {
        "group": "default",
        "related_labels": {
            "sfeer": 0.024,
            "samenwerking": 0.146,
            "waardering": 0.098,
            "aanspreken": 0.366,
            "aansturing": 0.024,
            "arbeidsvoorwaarden": 0.049,
            "begeleiding": 0.073,
            "onduidelijke afspraken": 0.049,
            "handhaving regels": 0.024,
            "werkdruk": 0.049,
            "management": 0.073,
            "inhoud werk": 0.024
        }
    },
    "aansturing": {
        "group": "default",
        "related_labels": {
            "sfeer": 0.014,
            "samenwerking": 0.143,
            "doorgroeien": 0.029,
            "waardering": 0.057,
            "aanspreken": 0.043,
            "aansturing": 0.1,
            "arbeidsvoorwaarden": 0.029,
            "bureaucratie": 0.029,
            "onduidelijke afspraken": 0.071,
            "planning": 0.057,
            "veranderingen": 0.043,
            "werkdruk": 0.029,
            "management": 0.314,
            "inhoud werk": 0.029,
            "duidelijke processen": 0.014
        }
    },
    "arbeidsvoorwaarden": {
        "group": "default",
        "related_labels": {
            "persoonlijke ontwikkeling": 0.012,
            "sfeer": 0.025,
            "autonomie": 0.012,
            "samenwerking": 0.05,
            "afwisseling": 0.025,
            "flexibiliteit": 0.038,
            "doorgroeien": 0.038,
            "waardering": 0.062,
            "plezier": 0.012,
            "aanspreken": 0.012,
            "arbeidsvoorwaarden": 0.462,
            "reistijd": 0.038,
            "onduidelijke afspraken": 0.012,
            "planning": 0.012,
            "veranderingen": 0.012,
            "werkdruk": 0.062,
            "zwaar werk": 0.012,
            "management": 0.025,
            "inhoud werk": 0.05,
            "functiematch": 0.025
        }
    },
    "begeleiding": {
        "group": "default",
        "related_labels": {
            "persoonlijke ontwikkeling": 0.081,
            "samenwerking": 0.081,
            "doorgroeien": 0.054,
            "aansturing": 0.081,
            "begeleiding": 0.541,
            "planning": 0.027,
            "werkdruk": 0.081,
            "inhoud werk": 0.027,
            "duidelijke processen": 0.027
        }
    },
    "faciliteiten": {
        "group": "default",
        "related_labels": {
            "persoonlijke ontwikkeling": 0.019,
            "sfeer": 0.038,
            "autonomie": 0.019,
            "samenwerking": 0.038,
            "werk prive balans": 0.038,
            "voldoening": 0.019,
            "plezier": 0.019,
            "aanspreken": 0.019,
            "arbeidsvoorwaarden": 0.019,
            "faciliteiten": 0.673,
            "reistijd": 0.019,
            "administratie": 0.019,
            "duurt lang": 0.019,
            "werkdruk": 0.038
        }
    },
    "reistijd": {
        "group": "default",
        "related_labels": {
            "reistijd": 1.0
        }
    },
    "administratie": {
        "group": "default",
        "related_labels": {
            "aansturing": 0.067,
            "begeleiding": 0.067,
            "administratie": 0.533,
            "bureaucratie": 0.067,
            "onduidelijke afspraken": 0.067,
            "duurt lang": 0.067,
            "werkdruk": 0.133
        }
    },
    "bureaucratie": {
        "group": "default",
        "related_labels": {
            "doorgroeien": 0.027,
            "aansturing": 0.027,
            "begeleiding": 0.027,
            "faciliteiten": 0.027,
            "administratie": 0.081,
            "bureaucratie": 0.595,
            "onduidelijke afspraken": 0.027,
            "duurt lang": 0.027,
            "vergaderen": 0.027,
            "management": 0.054,
            "duidelijke processen": 0.081
        }
    },
    "onduidelijke afspraken": {
        "group": "default",
        "related_labels": {
            "persoonlijke ontwikkeling": 0.012,
            "sfeer": 0.024,
            "autonomie": 0.012,
            "samenwerking": 0.12,
            "doorgroeien": 0.012,
            "waardering": 0.012,
            "aanspreken": 0.06,
            "aansturing": 0.084,
            "arbeidsvoorwaarden": 0.036,
            "begeleiding": 0.012,
            "bureaucratie": 0.024,
            "onduidelijke afspraken": 0.325,
            "duurt lang": 0.012,
            "vergaderen": 0.012,
            "werkdruk": 0.048,
            "management": 0.084,
            "inhoud werk": 0.012,
            "functiematch": 0.024,
            "duidelijke processen": 0.072
        }
    },
    "duurt lang": {
        "group": "default",
        "related_labels": {
            "samenwerking": 0.2,
            "doorgroeien": 0.1,
            "aansturing": 0.1,
            "duurt lang": 0.4,
            "werkdruk": 0.2
        }
    },
    "handhaving regels": {
        "group": "default",
        "related_labels": {
            "samenwerking": 0.25,
            "flexibiliteit": 0.025,
            "aanspreken": 0.125,
            "aansturing": 0.05,
            "onduidelijke afspraken": 0.1,
            "handhaving regels": 0.325,
            "werkdruk": 0.05,
            "management": 0.025,
            "inhoud werk": 0.05
        }
    },
    "niets": {
        "group": "default",
        "related_labels": {
            "voldoening": 0.105,
            "aanspreken": 0.053,
            "duurt lang": 0.053,
            "niets": 0.737,
            "aandacht": 0.053
        }
    },
    "planning": {
        "group": "default",
        "related_labels": {
            "samenwerking": 0.034,
            "werk prive balans": 0.017,
            "waardering": 0.017,
            "aanspreken": 0.017,
            "aansturing": 0.017,
            "reistijd": 0.051,
            "administratie": 0.017,
            "planning": 0.542,
            "veranderingen": 0.102,
            "vergaderen": 0.017,
            "werkdruk": 0.153,
            "management": 0.017
        }
    },
    "solistisch werken": {
        "group": "default",
        "related_labels": {
            "samenwerking": 0.636,
            "aanspreken": 0.091,
            "reistijd": 0.091,
            "solistisch werken": 0.182
        }
    },
    "veranderingen": {
        "group": "default",
        "related_labels": {
            "sfeer": 0.011,
            "samenwerking": 0.067,
            "afwisseling": 0.011,
            "werk prive balans": 0.011,
            "aansturing": 0.033,
            "arbeidsvoorwaarden": 0.011,
            "faciliteiten": 0.022,
            "administratie": 0.022,
            "bureaucratie": 0.011,
            "onduidelijke afspraken": 0.044,
            "duurt lang": 0.033,
            "planning": 0.022,
            "veranderingen": 0.611,
            "werkdruk": 0.067,
            "management": 0.022
        }
    },
    "vergaderen": {
        "group": "default",
        "related_labels": {
            "samenwerking": 0.25,
            "planning": 0.25,
            "vergaderen": 0.25,
            "werkdruk": 0.25
        }
    },
    "werkdruk": {
        "group": "default",
        "related_labels": {
            "sfeer": 0.015,
            "samenwerking": 0.061,
            "afwisseling": 0.03,
            "werk prive balans": 0.03,
            "flexibiliteit": 0.015,
            "veiligheid": 0.015,
            "aanspreken": 0.015,
            "aansturing": 0.045,
            "arbeidsvoorwaarden": 0.03,
            "administratie": 0.03,
            "handhaving regels": 0.045,
            "planning": 0.076,
            "werkdruk": 0.545,
            "zwaar werk": 0.03,
            "management": 0.015
        }
    },
    "zwaar werk": {
        "group": "default",
        "related_labels": {
            "werk prive balans": 0.2,
            "arbeidsvoorwaarden": 0.2,
            "reistijd": 0.2,
            "werkdruk": 0.2,
            "zwaar werk": 0.2
        }
    },
    "management": {
        "group": "default",
        "related_labels": {
            "sfeer": 0.041,
            "autonomie": 0.027,
            "samenwerking": 0.205,
            "afwisseling": 0.027,
            "waardering": 0.055,
            "aanspreken": 0.041,
            "aansturing": 0.247,
            "begeleiding": 0.014,
            "faciliteiten": 0.014,
            "veranderingen": 0.014,
            "werkdruk": 0.014,
            "management": 0.288,
            "aandacht": 0.014
        }
    },
    "aandacht": {
        "group": "default",
        "related_labels": {
            "persoonlijke ontwikkeling": 0.033,
            "sfeer": 0.033,
            "autonomie": 0.016,
            "samenwerking": 0.115,
            "flexibiliteit": 0.016,
            "doorgroeien": 0.016,
            "veiligheid": 0.016,
            "waardering": 0.066,
            "aanspreken": 0.016,
            "aansturing": 0.033,
            "begeleiding": 0.115,
            "faciliteiten": 0.016,
            "bureaucratie": 0.016,
            "niets": 0.016,
            "veranderingen": 0.016,
            "werkdruk": 0.016,
            "management": 0.066,
            "aandacht": 0.361,
            "inhoud werk": 0.016
        }
    },
    "inhoud werk": {
        "group": "default",
        "related_labels": {
            "persoonlijke ontwikkeling": 0.167,
            "samenwerking": 0.167,
            "afwisseling": 0.167,
            "arbeidsvoorwaarden": 0.167,
            "inhoud werk": 0.333
        }
    },
    "functiematch": {
        "group": "default",
        "related_labels": {
            "persoonlijke ontwikkeling": 0.071,
            "afwisseling": 0.214,
            "voldoening": 0.143,
            "waardering": 0.071,
            "plezier": 0.143,
            "begeleiding": 0.143,
            "niets": 0.071,
            "inhoud werk": 0.143
        }
    },
    "duidelijke processen": {
        "group": "default",
        "related_labels": {
            "autonomie": 0.2,
            "plezier": 0.2,
            "handhaving regels": 0.2,
            "duidelijke processen": 0.4
        }
    }
}


# 2. follow-up 题库（minst / meest）
#    未列出的主题自动视为 []，逻辑层会跳过
POOL_MINST = {
    "aandacht": [
        "Hoe heeft jouw werkgever op dit moment aandacht voor jou?",
        "Wat kan jouw werkgever doen om meer aandacht te hebben voor mensen?",
    ],
    "aanspreken": [
        "Wat was de laatste keer dat teamleden elkaar aanspraken op gedrag? Wat was er gebeurd en hoe is het opgelost?",
        "Als je feedback krijgt van collega's kan je er dan iets mee? Waarom?",
    ],
    "aansturing": [
        "Wat is voor jou de grootste uitdaging in hoe de organisatie wordt aangestuurd?",
        "Hoe zou de organisatie jou het beste kunnen betrekken bij het bepalen van de lange termijn plannen?",
        "Worden beslissingen van het management voldoende uitgelegd? Waarom vind je dat?",
    ],
    "afwisseling": [
        "Als je terugdenkt aan de afgelopen week, was je werk dan afwisselend genoeg? Waarom wel of niet?",
        "Hoe zou jouw werk meer afwisselend kunnen worden?",
    ],
    "arbeidsvoorwaarden": [
        "Wat zou je graag anders zien in je arbeidsvoorwaarden?",
        "Zou je overwegen om weg te gaan als je ergens betere arbeidsvoorwaarden kon krijgen? Waarom wel of niet?",
    ],
    "autonomie": [
        "Krijg je voldoende ruimte voor eigen inbreng in je werk? Waarom?",
        "Kan je een voorbeeld noemen van een werksituatie waarin je weinig vrijheid kreeg?",
        "Zijn er bepaalde regels of processen die je het gevoel geven dat je beperkt wordt in je vrijheid?",
    ],
    "bureaucratie": [
        "Kan je een voorbeeld noemen van een werksituatie waarin je bureaucratie hebt ervaren?",
        "Heb je voorbeelden van processen die minder bureaucratisch kunnen?",
        "Wat is volgens jou de grootste uitdaging in het terugdringen van bureaucratie in de organisatie?",
    ],
    "doorgroeien": [
        "Zou je graag meer doorgroeimogelijkheden krijgen in je werk?",
        "Is voor jou duidelijk hoe je zou kunnen doorgroeien in je werk? Waarom wel of niet?",
        "Hoe zou je het liefst willen doorgroeien? En waarom?",
    ],
    "faciliteiten": [
        "Wat zou je graag anders zien in de faciliteiten op je werk?",
    ],
    "management": [
        "Wat is voor jou de belangrijkste uitdaging in het contact met je leidinggevende? Waarom?",
        "Zijn er momenten dat je je niet begrepen voelt door je leidinggevende? Waarom?",
        "Hoe zou jouw leidinggevende de samenwerking kunnen verbeteren?",
    ],
    "onduidelijke afspraken": [
        "Kan je een voorbeeld geven van een werksituatie waarin er onduidelijke afspraken waren? Hoe is dat opgelost?",
        "Wat zou je graag anders zien in hoe er met afspraken en proces wordt omgegaan?",
    ],
    "persoonlijke ontwikkeling": [
        "Wat is voor jou de grootste uitdaging in het werken aan je persoonlijke ontwikkeling?",
        "Op welke manier zou je het liefst willen werken aan je persoonlijke ontwikkeling?",
    ],
    "planning": [
        "Wat is voor jou de grootste uitdaging rond de planning en roostering?",
        "Wat zou je graag anders zien in hoe er met de planning wordt omgegaan?",
    ],
    "samenwerking": [
        "Wat zijn volgens jou de grootste uitdagingen in de samenwerking met collega's? Waarom?",
        "En kan je ook een voorbeeld noemen van een werksituatie waarin de samenwerking wel goed verliep? Hoe kwam dat en hoe is het opgelost?",
        "Wat zou je graag anders zien in de samenwerking met collega's?",
    ],
    "sfeer": [
        "Hoe zou je de sfeer op je werk omschrijven?",
        "Kan je een voorbeeld noemen van een werksituatie waarin de sfeer niet goed was?",
        "Wat kan de organisatie doen om de sfeer te verbeteren?",
    ],
    "veranderingen": [
        "Vind je dat de organisatie voldoende doet om de werknemers mee te nemen in veranderingen?",
        "Hoe kan de organisatie beter omgaan met veranderingen?",
    ],
    "voldoening": [
        "Haal je voldoening uit je werk? Waarom wel of niet",
        "Hoe zou je meer voldoening uit je werk kunnen krijgen?",
    ],
    "waardering": [
        "Wat is volgens jou op je werk de grootste uitdaging in het tonen van waardering naar elkaar ? Waarom?",
        "Wat zou er kunnen veranderen zodat collega's meer waardering voelen voor hun werk?",
    ],
    "werk prive balans": [
        "Hoe wordt er op dit moment in je werk omgegaan met de werk- prive balans?",
        "Kan je een voorbeeld geven van een werksituatie waardoor je in de knoop kwam met je thuis situatie?",
    ],
    "werkdruk": [
        "Wanneer had je voor het laatst last van werkdruk? Wat was er gebeurd en hoe is het opgelost?",
        "Hoe zou de organisatie jouw werkdruk kunnen verlichten?",
    ],
}

POOL_MEEST = {
    "aandacht": [
        "Op welke manier heeft jouw werkgever nu aandacht nu voor jou?",
        "Wat kan jouw werkgever doen om nog meer aandacht voor jou te hebben?",
    ],
    "aanspreken": [
        "Hoe geven collega's elkaar op dit moment feedback?",
        "Wat was de laatste keer dat teamleden elkaar aanspraken op gedrag? Wat was er gebeurd en hoe is het opgelost?",
        "Op welke manier draagt het geven feedback bij aan jouw motivatie en betrokkenheid?",
    ],
    "aansturing": [
        "Wat zou je graag anders zien in hoe de organisatie wordt aangestuurd?",
        "Hoe zou je het liefst geinformeerd willen worden genomen in de lange termijn plannen voor de organisatie?",
    ],
    "afwisseling": [
        "Hoe zou je de balans tussen variatie en routine in je werk omschrijven?",
        "Kan je een voorbeeld geven van hoe je werk afwisselend is?",
    ],
    "arbeidsvoorwaarden": [
        "Over welke onderdelen van je arbeidsvoorwaarden ben je het meest tevreden en waarom?",
        "Zou je overwegen om weg te gaan als je ergens betere arbeidsvoorwaarden kon krijgen? Waarom wel of niet?",
        "Op welke manier dragen jouw arbeidsvoorwaarden bij aan jouw motivatie en betrokkenheid?",
    ],
    "autonomie": [
        "Kan je een voorbeeld noemen van een werksituatie waarin je veel vrijheid kreeg?",
        "Hoe ervaar je de mate van vrijheid die je nu hebt in je werk?",
        "Op welke manier draagt vrijheid bij aan jouw motivatie en betrokkenheid?",
    ],
    "doorgroeien": [
        "Heb je een duidelijk beeld van doorgroeimogelijkheden in je werk? Waarom wel of niet?",
        "Zijn er obstakels die je belemmeren om door te groeien in je werk?",
        "Hoe dragen doorgroeimogelijkheden bij aan jouw motivatie en betrokkenheid?",
    ],
    "faciliteiten": [
        "Over welke faciliteiten ben je tevreden op je werk?",
        "Wat zou er gedaan kunnen worden om de faciliteiten te verbeteren?",
    ],
    "management": [
        "Op welke manier ondersteunt jouw leidinggevende jou in je werk?",
        "Wat moet jouw leidinggevende vooral blijven doen? En waarom?",
    ],
    "niets": [
        "Wat waardeer je het meest in de manier waarop de organisatie met jou omgaat?",
    ],
    "persoonlijke ontwikkeling": [
        "Hoe werk jij op dit moment aan je persoonlijke ontwikkeling?",
        "Op welke manier zou je het liefst willen werken aan je persoonlijke ontwikkeling?",
        "Is het voor jou belangrijk om je te blijven ontwikkelen in je werk? Waarom?",
    ],
    "planning": [
        "Kan je een voorbeeld geven van een situatie waarin je erg tevreden was over de planning?",
        "Hoe zou de organisatie de planning kunnen verbeteren?",
    ],
    "samenwerking": [
        "Hoe zou je de samenwerking met collega's omschrijven?",
        "Wat zijn de sterke punten in de samenwerking met jouw collega's?",
        "Wat zou er moeten veranderen om de samenwerking met collega's nog verder te verbeteren?",
    ],
    "sfeer": [
        "Hoe houden jullie de sfeer op het werk goed?",
        "Wat moeten de organisatie vooral blijven doen om de sfeer goed te houden?",
        "Op welke manier draagt de sfeer bij aan jouw motivatie en betrokkenheid?",
    ],
    "veranderingen": [
        "Kan je een voorbeeld noemen van veranderingen waar je tevreden mee bent?",
        "Doet de organisatie voldoende om medewerkers te ondersteunen bij veranderingen?",
    ],
    "voldoening": [
        "Hoe haal je de meeste voldoening uit je werk?",
        "Kan je een voorbeeld noemen van een werksituatie die jou veel voldoening gaf?",
    ],
    "waardering": [
        "Hoe ervaar je nu waardering in je werk?",
        "Kan je een voorbeeld noemen van een moment dat je veel waardering voelde? Wat maakte deze ervaring voor jou zo positief?",
    ],
    "werk prive balans": [
        "Hoe wordt er op dit moment omgegaan met de werk- prive balans in jouw organisatie?",
        "Wat zijn voor jou de grootste uitdagingen in je werk- prive balans?",
        "Zijn er dingen die de organisatie kan doen om jou beter te helpen met je werk prive balans?",
    ],
    "werkdruk": [
        "Wanneer had je voor het laatst last van werkdruk? Wat was er gebeurd en hoe is het opgelost?",
    ],
}
