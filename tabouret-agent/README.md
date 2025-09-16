# Tabouret Agent

Интеллектуальный агент для автоматизации продаж мебели в аренду от компании Tabouret Solutions. Агент использует Google Gemini AI для ведения структурированных диалогов с потенциальными клиентами.

## Описание

Tabouret Agent - это система автоматизации продаж, которая проводит структурированные диалоги с потенциальными клиентами через различные этапы продаж:

- **GATEKEEPER** - Поиск ответственного лица
- **INTRO** - Представление компании и услуг
- **QUALIFY** - Квалификация клиента
- **TESTIMONIAL** - Предоставление кейсов и отзывов
- **MEETING_ASK** - Предложение консультации
- **SCHEDULING** - Планирование встречи
- **CLOSE** - Завершение диалога
- **END** - Окончание разговора

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd tabouret-agent
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install google-generativeai
```

4. Настройте API ключ Google Gemini:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## Конфигурация

Создайте файл `config.json` с промптами для каждого этапа диалога:

```json
{
  "prompts": {
    "GATEKEEPER": "Добрый день! Могу поговорить с ответственным за интерьер?",
    "INTRO": "Я представляю Tabouret Solutions. Мы предлагаем бесплатную аренду мебели...",
    "QUALIFY": "Сколько у вас сотрудников и на каких соцсетях вы активны?",
    "TESTIMONIAL": "У нас есть успешный кейс с бизнесом, похожим на ваш...",
    "MEETING_ASK": "Предлагаю провести короткую консультацию, удобно ли вам?",
    "SCHEDULING": "Отлично, на какую дату/время можем поставить встречу?",
    "CLOSE": "Спасибо! Я отправлю приглашение в календарь.",
    "END": "Хорошего дня!"
  }
}
```

Если файл конфигурации отсутствует, агент использует встроенные промпты по умолчанию.

## Использование

### Базовое использование

```python
from tabouret_agent import ConversationAgent

# Создание агента
agent = ConversationAgent()

# Начало диалога
response = agent.process_turn()
print(f"Agent ({response['stage']}): {response['message']}")

# Продолжение диалога
while response["stage"] != "END":
    user_input = input("You: ")
    response = agent.process_turn(user_input)
    print(f"Agent ({response['stage']}): {response['message']}")
```

### Демонстрация

Запустите интерактивную демонстрацию:

```bash
python demo_tabouret.py
```

### Тестирование

Запустите тесты для проверки функциональности:

```bash
python test_tabouret.py
```

## API

### ConversationAgent

Основной класс агента для ведения диалогов.

#### Параметры инициализации:
- `api_key` (str, optional): API ключ Google Gemini. По умолчанию берется из переменной окружения `GEMINI_API_KEY`
- `config_path` (str): Путь к файлу конфигурации. По умолчанию `"config.json"`
- `model_name` (str): Название модели Gemini. По умолчанию `"gemini-1.5-flash"`

#### Методы:

##### `process_turn(user_input=None)`
Обрабатывает один ход диалога.

**Параметры:**
- `user_input` (str, optional): Ввод пользователя

**Возвращает:**
- `dict`: Словарь с ключами:
  - `message` (str): Ответ агента
  - `stage` (str): Текущий этап диалога
  - `summary` (str): Краткое описание состояния

### Stage

Класс с константами этапов диалога:
- `GATEKEEPER`
- `INTRO`
- `QUALIFY`
- `TESTIMONIAL`
- `MEETING_ASK`
- `SCHEDULING`
- `CLOSE`
- `OBJECTION`
- `CALLBACK`
- `END`

## Особенности

- **Автоматические переходы**: Агент автоматически переходит между этапами диалога
- **История диалога**: Сохраняет последние 6 ходов для контекста
- **Обработка ошибок**: Graceful handling ошибок API с информативными сообщениями
- **Гибкая конфигурация**: Возможность настройки промптов через JSON файл
- **Fallback конфигурация**: Встроенные промпты по умолчанию при отсутствии конфигурации

## Требования

- Python 3.7+
- google-generativeai
- API ключ Google Gemini

## Лицензия

Проект разработан для внутреннего использования Tabouret Solutions.

## Поддержка

Для вопросов и предложений обращайтесь к команде разработки Tabouret Solutions.