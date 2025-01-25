from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os
import random

LEADERBOARD_FILE = "records.json"

# Функция для загрузки таблицы лидеров из файла
def load_leaderboard():
    try:
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Ошибка загрузки таблицы лидеров: {e}")
    return {}

# Функция для сохранения таблицы лидеров в файл
def save_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(global_leaderboard, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ошибка сохранения таблицы лидеров: {e}")

# Создаем файл, если его нет
if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)

# Глобальная таблица лидеров загружается из файла
global_leaderboard = load_leaderboard()

# Массив вопросов
sample_questions = [
    {
        "question": "Как расшифровывается LTS?",
        "answers": [
            "a) Long Time Support",
            "b) Long Time Service",
            "c) Long Term Support",
            "d) Linux Term Service",
            "e) Linux Time Support"
        ],
        "correct_answer": "c"
    }
]

# Состояния квиза
active_quizzes = {}  # {chat_id: {"remaining_questions": [...], "scores": {user_id: score}}}

# Начать квиз
async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id in active_quizzes:
        await update.message.reply_text("Квиз уже идет! Подождите его завершения.")
        return

    # Инициализация квиза
    random.shuffle(sample_questions)  # Перемешиваем список вопросов
    active_quizzes[chat_id] = {"remaining_questions": sample_questions.copy(), "scores": {}}
    await send_question(update, context)

# Отправить вопрос
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    quiz = active_quizzes.get(chat_id)
    if not quiz:
        await update.message.reply_text("Квиз не запущен. Используйте /quiz, чтобы начать.")
        return

    if not quiz["remaining_questions"]:
        await end_quiz(update, context)  # Завершаем квиз, если вопросы закончились
        return

    # Берем первый вопрос из перемешанного списка
    question_data = quiz["remaining_questions"][0]
    question_text = f"Вопрос: {question_data['question']}\n\n" + "\n".join(question_data["answers"])
    await update.message.reply_text(question_text)

# Обработать ответ
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = update.effective_user.first_name or "Участник"
    quiz = active_quizzes.get(chat_id)

    if not quiz:
        return  # Игнорируем, если квиз не идет

    answer = update.message.text.lower().strip()
    if answer not in ["a", "b", "c", "d", "e"]:
        return  # Игнорируем сообщения не из набора [a, b, c, d, e]

    # Проверяем правильность ответа
    question_data = quiz["remaining_questions"].pop(0)  # Убираем вопрос после обработки
    if answer == question_data["correct_answer"]:
        quiz["scores"][user_id] = quiz["scores"].get(user_id, 0) + 1
        await update.message.reply_text(f"Правильно, {username}! 🎉")
    else:
        await update.message.reply_text(f"Неправильно, {username}. Правильный ответ: {question_data['correct_answer']}")

    # Переходим к следующему вопросу или заканчиваем квиз
    if quiz["remaining_questions"]:
        await send_question(update, context)
    else:
        await end_quiz(update, context)

# Завершить квиз
async def end_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global global_leaderboard
    chat_id = update.effective_chat.id
    quiz = active_quizzes.pop(chat_id, None)

    if not quiz:
        await update.message.reply_text("Квиз уже завершен.")
        return

    # Обновляем глобальную таблицу лидеров
    for user_id, score in quiz["scores"].items():
        user_id = str(user_id)  # Приводим user_id к строке для совместимости
        username = "Хазрат" if user_id == "1415003296" else (await update.effective_chat.get_member(int(user_id))).user.first_name
        if user_id in global_leaderboard:
            global_leaderboard[user_id]["score"] += score
        else:
            global_leaderboard[user_id] = {"username": username, "score": score}

    # Сохраняем обновленную таблицу лидеров
    save_leaderboard()

    # Выводим таблицу лидеров квиза
    scores = quiz["scores"]
    if scores:
        leaderboard = "\n".join(
            [
                f"{'Хазрат' if user_id == '1415003296' else (await update.effective_chat.get_member(int(user_id))).user.first_name}: {score}"
                for user_id, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)
            ]
        )
        await update.message.reply_text(f"Квиз завершен! 🎉\nТаблица лидеров для этого квиза:\n\n{leaderboard}")
    else:
        await update.message.reply_text("Никто не ответил на вопросы. 😔")

# Показать таблицу лидеров
async def show_records(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not global_leaderboard:
        await update.message.reply_text("Таблица лидеров пока пуста.")
        return

    leaderboard = "\n".join(
        [
            f"{'Хазрат' if user_id == '1415003296' else record['username']}: {record['score']}"
            for user_id, record in sorted(global_leaderboard.items(), key=lambda x: x[1]['score'], reverse=True)
        ]
    )
    await update.message.reply_text(f"Текущая таблица лидеров:\n\n{leaderboard}")


# Команда для завершения квиза вручную
async def stop_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in active_quizzes:
        await update.message.reply_text("Квиз не активен.")
        return

    # Завершаем квиз
    await end_quiz(update, context)
    await update.message.reply_text("Квиз завершен по вашему запросу.")

# Показать таблицу лидеров
async def show_records(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not global_leaderboard:
        await update.message.reply_text("Таблица лидеров пока пуста.")
        return

    leaderboard = "\n".join(
        [
            f"{record['username']}: {record['score']}"
            for record in sorted(global_leaderboard.values(), key=lambda x: x['score'], reverse=True)
        ]
    )
    await update.message.reply_text(f"Текущая таблица лидеров:\n\n{leaderboard}")

# Основной код
def main():
    application = Application.builder().token("7696889634:AAFvquRqGjd9mdY7EgU5QrSJQXpNvGMwTHQ").build()

    # Регистрируем команды
    application.add_handler(CommandHandler("quiz", start_quiz))
    application.add_handler(CommandHandler("stop", stop_quiz))
    application.add_handler(CommandHandler("records", show_records))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
