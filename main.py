import os, json
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])

VALID_TOKEN = os.environ.get("ACCESS_TOKEN", "novetech2024")
BASE = os.path.dirname(__file__)

with open(os.path.join(BASE, "data_d.json"), encoding="utf-8") as f: DATA_D = json.load(f)
with open(os.path.join(BASE, "data_u.json"), encoding="utf-8") as f: DATA_U = json.load(f)
with open(os.path.join(BASE, "painel.html"), encoding="utf-8") as f: PAINEL_HTML = f.read()

def check_token(token):
    if token != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.get("/", response_class=HTMLResponse)
def get_painel(token: str = Query(None)):
    if not token or token != VALID_TOKEN:
        return HTMLResponse(content='<html><body style="background:#fff;color:#1a2e6b;font-family:system-ui;display:flex;align-items:center;justify-content:center;height:100vh;flex-direction:column;gap:16px;margin:0"><div style="font-size:2rem">🔒</div><div style="font-size:1.1rem;font-weight:700">Acesso restrito</div><div style="font-size:.8rem;color:#5a6a8a">Solicite seu link à equipe Novetech</div></body></html>', status_code=401)
    return HTMLResponse(content=PAINEL_HTML)

@app.get("/data/d")
def get_data_d(token: str = Query(...)):
    check_token(token)
    return JSONResponse(content=DATA_D)

@app.get("/data/u")
def get_data_u(token: str = Query(...)):
    check_token(token)
    return JSONResponse(content=DATA_U)
