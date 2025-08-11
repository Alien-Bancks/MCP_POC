import json
from sqlalchemy.orm import Session
from core import gerar_embedding, Document, llm
from deep_translator import GoogleTranslator

def consulta_rag(pergunta: str, session: Session, top_k: int = 10) -> dict:
    try:
        pergunta_en = GoogleTranslator(source='pt', target='en').translate(pergunta)
    except Exception:
        pergunta_en = pergunta

    emb = gerar_embedding(pergunta_en)

    resultados = (
        session.query(Document)
        .order_by(Document.embedding.l2_distance(emb))
        .limit(top_k)
        .all()
    )

    if not resultados:
        return {"resposta": "Desculpe, não encontrei informações relevantes."}

    MAX_CONTEXT_CHARS = 3500
    contexto_en = "\n".join([r.content for r in resultados])
    if len(contexto_en) > MAX_CONTEXT_CHARS:
        contexto_en = contexto_en[:MAX_CONTEXT_CHARS]

    prompt = f"""
    You are an intelligent assistant that answers questions using only the provided text.
    If the answer is not explicit, provide the most accurate and coherent answer possible
    based on the given information. Do not invent facts that contradict the text.
    Please provide a detailed, complete, and clear answer.

    CONTEXT:
    {contexto_en}

    QUESTION:
    {pergunta_en}

    ANSWER:
    """

    llm_response = llm(prompt=prompt, max_tokens=300)


    resposta_en = ""

    if isinstance(llm_response, dict):
        choices = llm_response.get("choices")
        if choices and isinstance(choices, list):
            if "text" in choices[0]:
                resposta_en = choices[0]["text"].strip()
            elif "message" in choices[0] and "content" in choices[0]["message"]:
                resposta_en = choices[0]["message"]["content"].strip()
            else:
                resposta_en = str(llm_response)
        else:
            resposta_en = str(llm_response)
    else:
        resposta_en = str(llm_response).strip()

    try:
        json_parsed = json.loads(resposta_en)
        if isinstance(json_parsed, dict) and "resposta" in json_parsed:
            resposta_en = json_parsed["resposta"]
    except json.JSONDecodeError:
        pass

    # Traduz para português
    try:
        resposta_pt = GoogleTranslator(source='auto', target='pt').translate(resposta_en)
    except Exception:
        resposta_pt = resposta_en

    return {"resposta": resposta_pt}
