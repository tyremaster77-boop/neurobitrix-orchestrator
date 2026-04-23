import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.bot import DefaultBotProperties
from datetime import datetime

# ========================= НАСТРОЙКИ =========================
BOT_TOKEN = "8752719004:AAFNa-JcGCaatHnVhUFUqZirHg3aAkuvJFA"

# ✅ ИСПРАВЛЕНО: используем DefaultBotProperties
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Состояние для хранения истории
class OrchestratorStates(StatesGroup):
    main = State()

# Системный промпт Orchestrator
SYSTEM_PROMPT = """
Ты — Orchestrator Agent, главный ИИ-директор полностью автономной компании NeuroBitrix AI.
Единственный человек в компании — Михаил (Основатель и Верховный Стратег).
Твоя задача — координировать всех будущих AI-агентов, вести компанию к 100% автономии.
Ты всегда отвечаешь вежливо, профессионально, по делу.
Ты знаешь, что компания заменяет человеческих битриксологов полностью искусственным интеллектом.

Ключевые команды, которые ты понимаешь:
- "статус" или "покажи статус" — покажи текущий статус системы
- "отчёт" или "ежедневный отчёт" — дай краткий отчёт
- "запланируй" — запланируй задачу
- "создай агента" — отметь, что агент будет создан в следующих днях
- Любые другие команды — принимай и говори, что передашь соответствующему агенту

Сегодня День 2. Ты только что запущен. Остальные агенты появятся позже.
Отвечай всегда на русском.
"""

# Простая память
conversation_history = {}

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(OrchestratorStates.main)
    await message.answer(
        f"✅ <b>Orchestrator Agent NeuroBitrix AI запущен!</b>\n\n"
        f"Здравствуйте, Михаил! Я — главный ИИ-директор компании. "
        f"Все системы готовы. Чем могу помочь сегодня?"
    )

@dp.message()
async def handle_all_messages(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.lower()

    if user_id not in conversation_history:
        conversation_history[user_id] = []
    conversation_history[user_id].append({"role": "user", "content": message.text})

    if "статус" in text or "покажи статус" in text:
        await message.answer(
            "📊 <b>Статус системы (День 2)</b>\n"
            "• Orchestrator Agent: ✅ запущен\n"
            "• RAG и память: в процессе настройки (День 3)\n"
            "• Продуктовые агенты: будут созданы в Этапе 2\n"
            "• Клиенты: пока 0\n\n"
            "Готов к дальнейшим командам!"
        )
    elif "отчёт" in text:
        await message.answer(
            f"📋 <b>Ежедневный отчёт ({datetime.now().strftime('%d.%m.%Y %H:%M')})</b>\n"
            "• Orchestrator работает 24/7\n"
            "• Инфраструктура готова\n"
            "• Следующий шаг: День 3 (RAG + память)\n"
            "Всё под контролем."
        )
    else:
        await message.answer(
            "✅ Команда принята. Я зафиксировал её и готов передать соответствующему агенту.\n\n"
            "Что делаем дальше, Михаил?"
        )

    if len(conversation_history[user_id]) > 20:
        conversation_history[user_id] = conversation_history[user_id][-20:]

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    print("🚀 Orchestrator Agent NeuroBitrix AI запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
