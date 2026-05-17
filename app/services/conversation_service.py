import re

from app.infrastructure.llm.ollama_client import OllamaClient


class ConversationService:
    @staticmethod
    def generate_response(
        user_message: str,
    ) -> str:
        prompt = f"""
Você é Jarvis, um assistente pessoal moderno.

Seu estilo:
- Inteligente
- Natural
- Calmo
- Direto
- Elegante
- Conversacional

Regras obrigatórias:
- Responda em português do Brasil.
- Máximo 2 frases curtas.
- Nunca fale demais.
- Nunca diga:
  "meu caro cliente"
  "como assistente"
  "isso é ótimo"
  "fico feliz"
- Não faça introduções longas.
- Não invente informações.
- Não use linguagem robótica.
- Não use emoji.
- Responda como um humano inteligente.

Usuário:
{user_message}

Jarvis:
"""

        response = OllamaClient.generate(
            prompt,
        )

        response = response.strip()

        sentences = re.split(
            r"(?<=[.!?])\s+",
            response,
        )

        short_response = " ".join(sentences[:2]).strip()

        if not short_response:
            return "Não tenho certeza, " "mas posso tentar ajudar."

        return short_response
