# tabouret_agent.py
import os
import json

try:
    import google.generativeai as genai
except ImportError:
    genai = None  # позволит падать с понятной ошибкой позже

__all__ = ["Stage", "ConversationAgent"]

class Stage:
    GATEKEEPER = "GATEKEEPER"
    INTRO = "INTRO"
    QUALIFY = "QUALIFY"
    TESTIMONIAL = "TESTIMONIAL"
    MEETING_ASK = "MEETING_ASK"
    SCHEDULING = "SCHEDULING"
    CLOSE = "CLOSE"
    OBJECTION = "OBJECTION"
    CALLBACK = "CALLBACK"
    END = "END"

class ConversationAgent:
    def __init__(self, api_key=None, config_path="config.json", model_name="gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY or pass api_key.")

        if genai is None:
            raise ImportError(
                "google-generativeai not installed. Run: pip install google-generativeai"
            )

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

        self.stage = Stage.GATEKEEPER
        self.history = []

        if not os.path.exists(config_path):
            # минимальная конфигурация по умолчанию
            self.config = {
                "prompts": {
                    "GATEKEEPER": "Добрый день! Могу поговорить с ответственным за интерьер?",
                    "INTRO": "Я представляю Tabouret Solutions. Мы предлагаем бесплатную аренду мебели...",
                    "QUALIFY": "Сколько у вас сотрудников и на каких соцсетях вы активны?",
                    "TESTIMONIAL": "У нас есть успешный кейс с бизнесом, похожим на ваш...",
                    "MEETING_ASK": "Предлагаю короткую консультацию, удобно ли вам?",
                    "SCHEDULING": "На какую дату/время поставить встречу и почту для инвайта?",
                    "CLOSE": "Спасибо! Я отправлю приглашение в календарь.",
                    "END": "Хорошего дня!"
                }
            }
        else:
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)

    def process_turn(self, user_input=None):
        if user_input is not None:
            self.history.append({"role": "user", "content": user_input})

        prompt = self._build_prompt()
        response = self._generate_response(prompt)

        self.history.append({"role": "agent", "content": response["message"]})
        self.stage = response["stage"]
        return response

    def _build_prompt(self):
        stage_prompt = self.config.get("prompts", {}).get(self.stage, "")
        history_text = "\n".join(f"{h['role']}: {h['content']}" for h in self.history[-6:])
        return f"{history_text}\nAgent ({self.stage}): {stage_prompt}".strip()

    def _generate_response(self, prompt: str):
        try:
            raw = self.model.generate_content(prompt)
            text = getattr(raw, "text", "").strip() or "..."
            return {
                "message": text,
                "stage": self._next_stage(),
                "summary": f"Stage: {self.stage}, turns: {len(self.history)}"
            }
        except Exception as e:
            return {
                "message": f"[Ошибка генерации: {e}]",
                "stage": Stage.END,
                "summary": "Conversation ended due to error."
            }

    def _next_stage(self):
        order = [
            Stage.GATEKEEPER, Stage.INTRO, Stage.QUALIFY,
            Stage.TESTIMONIAL, Stage.MEETING_ASK,
            Stage.SCHEDULING, Stage.CLOSE, Stage.END
        ]
        if self.stage in order:
            i = order.index(self.stage)
            return order[i + 1] if i + 1 < len(order) else Stage.END
        return Stage.END