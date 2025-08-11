from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from core import processar_arquivo, session
from app.rag import consulta_rag
import os

app = FastAPI()

UPLOAD_DIR = "docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        num_chunks = processar_arquivo(file_path)
        return {"mensagem": f"{file.filename} processado com {num_chunks} chunks."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})

@app.post("/perguntar")
async def perguntar(pergunta: str = Form(...)):
    try:
        resposta = consulta_rag(pergunta, session)
        return resposta
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})