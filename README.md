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
git clone https://github.com/TU_USUARIO/multi-system-agent.git
cd multi-system-agent

# 2. Instalar dependencias
uv sync

# 3. Configurar variables de entorno
cp .env_example .env
# Editar .env y completar OPENAI_API_KEY
```

## Uso

```bash
# Ejecutar el orquestador de forma interactiva
uv run python src/main.py

# Enviar una consulta directa
uv run python src/main.py --query "¿Cómo solicito vacaciones?"
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
├── api/                         # Endpoints FastAPI (en desarrollo)
├── .env_example                 # Plantilla de variables de entorno
├── pyproject.toml               # Dependencias y configuración
└── Makefile                     # Comandos de desarrollo
```

## Variables de entorno

| Variable         | Requerida | Descripción                        |
|------------------|-----------|------------------------------------|
| `OPENAI_API_KEY` | Sí        | Clave de API de OpenAI             |
| `OPENAI_MODEL`   | No        | Modelo a usar (default: gpt-4o-mini) |

