from app.services.intent_service import IntentService


class TestDetectIntentGetTime:
    def test_horas_returns_get_time(self):
        result = IntentService.detect_intent("que horas são")

        assert result == {"action": "get_time"}

    def test_hora_returns_get_time(self):
        result = IntentService.detect_intent("me diz a hora")

        assert result == {"action": "get_time"}

    def test_horario_returns_get_time(self):
        result = IntentService.detect_intent("qual o horário")

        assert result == {"action": "get_time"}


class TestDetectIntentSearchYouTube:
    def test_tocar_queen_no_youtube(self):
        result = IntentService.detect_intent("tocar Queen no YouTube")

        assert result["action"] == "search_youtube"
        assert result["query"] == "queen"

    def test_toque_musica(self):
        result = IntentService.detect_intent("toque Bohemian Rhapsody")

        assert result["action"] == "search_youtube"
        assert "bohemian rhapsody" in result["query"]

    def test_pesquise_no_youtube(self):
        result = IntentService.detect_intent("pesquisa Imagine")

        assert result["action"] == "search_youtube"
        assert "imagine dragons" in result["query"]


class TestDetectIntentConversation:
    def test_unknown_command_returns_conversation(self):
        result = IntentService.detect_intent("como está o tempo hoje")

        assert result["action"] == "conversation"
        assert result["query"] == "como está o tempo hoje"

    def test_greeting_returns_conversation(self):
        result = IntentService.detect_intent("bom dia")

        assert result["action"] == "conversation"
        assert result["query"] == "bom dia"

    def test_empty_string_returns_conversation(self):
        result = IntentService.detect_intent("")

        assert result["action"] == "conversation"
