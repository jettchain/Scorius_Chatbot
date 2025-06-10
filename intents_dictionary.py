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
    lbl: {
        "group": "default",            # 先全部放同组，可按需细分
        "weight": round(1 - i / len(INTENTS), 3),   # 1.000 → 0.026
    }
    for i, lbl in enumerate(INTENTS)
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
