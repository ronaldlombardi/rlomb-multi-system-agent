import json

from src import main as orchestrator


def test_route_query_rrhh_success(monkeypatch):
    calls = []

    def fake_call_api(system_prompt, user_prompt, temp=0.2, json_mode=False):
        calls.append({"prompt": system_prompt, "user": user_prompt, "json_mode": json_mode})
        if json_mode:
            return json.dumps({"departamento": "RRHH", "razon": "Consulta laboral"})
        return "Respuesta de RRHH"

    monkeypatch.setattr(orchestrator, "call_api", fake_call_api)

    result = orchestrator.route_query("Tuve ausencias este mes")

    assert result["departamento"] == "RRHH"
    assert result["razon"] == "Consulta laboral"
    assert result["respuesta"] == "Respuesta de RRHH"
    assert calls[0]["json_mode"] is True
    assert calls[1]["json_mode"] is False
    assert "Agente de RRHH" in calls[1]["prompt"]


def test_route_query_invalid_json_fallback_to_tech(monkeypatch):
    calls = []

    def fake_call_api(system_prompt, user_prompt, temp=0.2, json_mode=False):
        calls.append({"prompt": system_prompt, "json_mode": json_mode})
        if json_mode:
            return "esto-no-es-json"
        return "Respuesta de Tech"

    monkeypatch.setattr(orchestrator, "call_api", fake_call_api)

    result = orchestrator.route_query("consulta ambigua")

    assert result["departamento"] == "Tech"
    assert result["razon"] == "Fallback por JSON invalido del orquestador."
    assert result["respuesta"] == "Respuesta de Tech"
    assert "Agente de Tech" in calls[1]["prompt"]


def test_route_query_unknown_department_fallback_to_tech(monkeypatch):
    def fake_call_api(system_prompt, user_prompt, temp=0.2, json_mode=False):
        if json_mode:
            return json.dumps({"departamento": "Legal", "razon": ""})
        return "Respuesta de Tech"

    monkeypatch.setattr(orchestrator, "call_api", fake_call_api)

    result = orchestrator.route_query("necesito ayuda")

    assert result["departamento"] == "Tech"
    assert result["razon"] == "Departamento no reconocido por el orquestador."
    assert result["respuesta"] == "Respuesta de Tech"


def test_route_query_no_orchestrator_response(monkeypatch):
    calls = []

    def fake_call_api(system_prompt, user_prompt, temp=0.2, json_mode=False):
        calls.append(json_mode)
        return None

    monkeypatch.setattr(orchestrator, "call_api", fake_call_api)

    result = orchestrator.route_query("hola")

    assert result["departamento"] == "Tech"
    assert result["razon"] == "No se obtuvo respuesta del orquestador."
    assert result["respuesta"] == "No fue posible procesar la consulta en este momento."
    assert calls == [True]