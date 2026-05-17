from app.infrastructure.llm.ollama_client import OllamaClient


class ResponseService:
    ACTION_MESSAGES = {
        "search_youtube": "Claro, iniciando agora.",
        "open_youtube": "Claro, abrindo o YouTube.",
        "unknown_command": "Não entendi bem. Pode repetir?",
    }

    @staticmethod
    def generate_spoken_response(
        action: str,
        message: str | None = None,
        query: str | None = None,
    ) -> str:
        if action == "get_time" and message:
            return message

        if action in ResponseService.ACTION_MESSAGES:
            return ResponseService.ACTION_MESSAGES[action]

        prompt = f"""
Você é Jarvis, um assistente pessoal local.

Responda em português do Brasil com apenas uma frase curta.

Regras:
- Não peça desculpas.
- Não diga "aqui está".
- Não explique detalhes técnicos.
- Não use emoji.
- No máximo 12 palavras.
- Tom calmo, inteligente e profissional.

Contexto:
ação: {action}
mensagem: {message}
busca: {query}

Resposta:
"""

        response = OllamaClient.generate(prompt).strip()
        response = response.replace('"', "").strip()

        if not response:
            return "Certo, executando."

        if len(response.split()) > 12:
            return "Certo, executando."

        blocked_terms = [
            "desculpe",
            "aqui está",
            "processando",
            "sou uma ia",
            "como assistente",
        ]

        if any(term in response.lower() for term in blocked_terms):
            return "Certo, executando."

        return response
