# rag_utils.py

INTENTS = [i.lower() for i in [
    "Uitdaging","Persoonlijke ontwikkeling","Sfeer","Autonomie","Samenwerking",
    "Afwisseling","Werk prive balans","Trots","Voldoening","Flexibiliteit",
    "Doorgroeien","Veiligheid","Waardering","Plezier","Aanspreken","Aansturing",
    "Arbeidsvoorwaarden","Begeleiding","Faciliteiten","Reistijd","Administratie",
    "Bureaucratie","Onduidelijke afspraken","Duurt lang","Handhaving regels","Niets",
    "Planning","Solistisch werken","Veranderingen","Vergaderen","Werkdruk","Zwaar werk",
    "Management","Aandacht","Inhoud werk","Functiematch","Duidelijke processen"
]]

PROMPT_HEAD = (
    "User: aanspreken gedrag kaders stellen salaris eerlijke medewerkers\n"
    "model: Aanspreken, Arbeidsvoorwaarden, Onduidelijke afspraken"
)

def extract_intents(text: str):
    text_l = text.lower()
    return {i for i in INTENTS if i in text_l}

def build_prompt(query: str, *, retriever, k: int = 5, dbg: bool = False):
    # retrieved = [
    #     d for d in retriever.get_relevant_documents(query, k=k)
    #     if d.page_content.strip() != query.strip()
    # ]
    retrieved = retriever.invoke(query)
    if dbg:
        print(f"[DBG] hit {len(retrieved)} docs for query='{query[:60]}…'")
    shots = "\n\n".join(
        f"User: {d.page_content}\nmodel: {d.metadata['label']}" for d in retrieved
    )
    full_prompt = f"{PROMPT_HEAD}\n\n{shots}\n\nUser: {query}\nmodel:"
    return full_prompt, shots
