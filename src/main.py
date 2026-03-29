'''
Archivo Orquestador del Sistema Multi-Agente
'''


import argparse
import json
from pathlib import Path

try:
    from .logger_configuration import logger
    from .call_api import call_api
except ImportError:
    from logger_configuration import logger
    from call_api import call_api


BASE_DIR = Path(__file__).parent
DEPARTMENT_PROMPTS = {
    "RRHH": "RRHH.md",
    "Marketing": "Marketing.md",
    "Finanzas": "Finanzas.md",
    "Tech": "Tech.md",
}


def load_prompt(filename: str) -> str:
    return (BASE_DIR / filename).read_text(encoding="utf-8")


def route_query(user_query: str) -> dict:
    orchestrator_prompt = load_prompt("Orquestador.md")
    routing_raw = call_api(orchestrator_prompt, user_query, json_mode=True)

    if not routing_raw:
        return {
            "departamento": "Tech",
            "razon": "No se obtuvo respuesta del orquestador.",
            "respuesta": "No fue posible procesar la consulta en este momento.",
        }

    try:
        routing_data = json.loads(routing_raw)
    except json.JSONDecodeError:
        logger.warning("El orquestador devolvio un JSON invalido. Se usa fallback a Tech.")
        routing_data = {
            "departamento": "Tech",
            "razon": "Fallback por JSON invalido del orquestador.",
        }

    department = str(routing_data.get("departamento", "")).strip()
    reason = str(routing_data.get("razon", "")).strip()

    if department not in DEPARTMENT_PROMPTS:
        logger.warning("Departamento no reconocido: %s. Se usa fallback a Tech.", department)
        department = "Tech"
        if not reason:
            reason = "Departamento no reconocido por el orquestador."

    specialist_prompt = load_prompt(DEPARTMENT_PROMPTS[department])
    specialist_response = call_api(specialist_prompt, user_query, json_mode=False)

    return {
        "departamento": department,
        "razon": reason,
        "respuesta": specialist_response,
    }


def go():
    parser = argparse.ArgumentParser(description="Sistema Multi-Agente")
    parser.add_argument("--query", type=str, help="Consulta del usuario")
    parser.add_argument("query_text", nargs="*", help="Consulta del usuario (sin --query)")
    args = parser.parse_args()

    user_query = args.query
    if not user_query and args.query_text:
        user_query = " ".join(args.query_text).strip()

    if not user_query:
        user_query = input("Escribe tu consulta: ").strip()

    if not user_query:
        parser.error("Debes ingresar una consulta con --query, texto posicional o input interactivo.")

    result = route_query(user_query)

    logger.info("Departamento elegido: %s", result["departamento"])
    logger.info("Razon: %s", result["razon"])
    logger.info("Respuesta final: %s", result["respuesta"])


if __name__ == "__main__":
    go()


## Instrucciones 
# REplica adaptada al caso de uso 
#=============================================================
#            Main Controller (Orquestador)      
#=============================================================

# def main(topic):
#     # 1. El Router decide el camino
#     ruta_seleccionada = agente_router(topic)
#     logger.info(f"Router decidió: {ruta_seleccionada}")
    
#     resultado = ""
    
#     # 2. Switch Case (Lógica de Enrutamiento)
#     if ruta_seleccionada == "RECONCILIACION":
#         resultado = flujo_reconciliacion(topic)
        
#     elif ruta_seleccionada == "ROMANTICO":
#         resultado = flujo_romantico(topic)
        
#     elif ruta_seleccionada == "CASUAL":
#         resultado = flujo_casual(topic)
        
#     else:
#         # Fallback
#         logger.warning("Ruta desconocida, ejecutando flujo casual.")
#         resultado = flujo_casual(topic)
        
#     return {
#         "ruta": ruta_seleccionada,
#         "mensaje": resultado
#     }
