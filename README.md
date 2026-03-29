# Sistema Multi-Agente — Los Chicos de Henry

Sistema de enrutamiento inteligente basado en LLM que deriva consultas al departamento correcto (RRHH, Marketing, Finanzas o Tech) usando un agente orquestador y agentes especialistas.

## Arquitectura

```
Usuario → Orquestador (GPT-4o-mini) → Enrutamiento JSON → Agente Especialista → Respuesta
```

El orquestador lee la consulta, decide el departamento y el especialista responde en contexto.

## Requisitos

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes)
- Clave de API de OpenAI

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/ronaldlombardi/rlomb-multi-system-agent.git
cd rlomb-multi-system-agent

# 2. Instalar dependencias
uv sync

# 3. Configurar variables de entorno
cp .env_example .env
# Editar .env y completar OPENAI_API_KEY
```

## Uso

### CLI

```bash
# Ejecutar el orquestador de forma interactiva
uv run python src/main.py

# Enviar una consulta directa
uv run python src/main.py --query "¿Cómo solicito vacaciones?"
```

### API FastAPI

```bash
# Levantar API en local
make api

# Alternativa sin make
uv run uvicorn api.Router.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Ejemplo de request a /query

```bash
curl -X POST "http://localhost:8000/query" \
	-H "Content-Type: application/json" \
	-d '{"query":"Quiero solicitar vacaciones para el mes que viene"}'
```

Respuesta esperada (ejemplo):

```json
{
	"departamento": "RRHH",
	"razon": "La consulta corresponde a gestion laboral y vacaciones.",
	"respuesta": {
		"diagnostico": "Para solicitar vacaciones, debes iniciar el proceso en el portal de RRHH.",
		"acciones": [
			"Revisar saldo de dias disponibles.",
			"Completar formulario con fechas de inicio y fin.",
			"Enviar solicitud a supervisor para aprobacion."
		],
		"consideraciones_legales": "Solicitar con la antelacion minima definida por politica interna.",
		"validacion": "Estado 'aprobada' en portal RRHH y correo de confirmacion.",
		"datos_faltantes": "Fechas exactas y area del colaborador."
	}
}
```

## Tests

```bash
uv run pytest tests/ -v
```

## Estructura del proyecto

```
.
├── src/
│   ├── main.py                  # Orquestador y punto de entrada
│   ├── call_api.py              # Cliente OpenAI reutilizable
│   ├── logger_configuration.py  # Logger con colores
│   ├── Orquestador.md           # System prompt del orquestador
│   ├── RRHH.md                  # Prompt agente RRHH
│   ├── Marketing.md             # Prompt agente Marketing
│   ├── Finanzas.md              # Prompt agente Finanzas
│   └── Tech.md                  # Prompt agente Tech
├── tests/
│   └── test_main_routing.py     # Tests del sistema de enrutamiento
├── api/                         # Endpoints FastAPI
├── .env_example                 # Plantilla de variables de entorno
├── pyproject.toml               # Dependencias y configuración
└── Makefile                     # Comandos de desarrollo
```

## Variables de entorno

| Variable         | Requerida | Descripción                        |
|------------------|-----------|------------------------------------|
| `OPENAI_API_KEY` | Sí        | Clave de API de OpenAI             |
| `OPENAI_MODEL`   | No        | Modelo a usar (default: gpt-4o-mini) |

