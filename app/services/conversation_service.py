import re

from app.infrastructure.llm.ollama_client import OllamaClient


class ConversationService:
    @staticmethod
    def generate_response(
        user_message: str,
    ) -> str:
        prompt = f"""
Você é Jarvis, um assistente pessoal inteligente.

Seu comportamento:
- Natural
- Calmo
- Elegante
- Objetivo
- Inteligente

Regras obrigatórias:
- Responda em português do Brasil.
- Responda de forma curta.
- No máximo 1 frase curta.
- Nunca invente contexto.
- Nunca suponha situações.
- Nunca dramatize.
- Nunca faça perguntas longas.
- Nunca fale como chatbot.
- Nunca use emoji.
- Nunca diga:
  "como IA"
  "fico feliz"
  "meu caro"
  "isso é ótimo"
- Se o usuário falar algo simples:
  responda de forma simples.
- Se o usuário perguntar algo:
  responda de forma objetiva.
- Soe como Jarvis do Homem de Ferro.
- Seja fluido e humano.

Usuário:
{user_message}

Jarvis:
"""

        response = OllamaClient.generate(
            prompt,
        )

        response = response.strip()

        response = re.sub(
            r"\s+",
            " ",
            response,
        )

        sentences = re.split(
            r"(?<=[.!?])\s+",
            response,
        )

        short_response = sentences[0].strip()

        if len(short_response.split()) > 18:
            short_response = "Entendido."

        if not short_response:
            return "Certo."

        return short_response
