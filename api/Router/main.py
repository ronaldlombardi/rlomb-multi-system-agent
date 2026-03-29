from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.main import route_query

app = FastAPI(title="Multi-System Agent API", version="0.1.0")


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    departamento: str
    razon: str
    respuesta: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="El campo 'query' no puede estar vacio.")
    result = route_query(request.query)
    return QueryResponse(**result)

