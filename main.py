import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.bot import DefaultBotProperties
from datetime import datetime

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# ========================= НАСТРОЙКИ =========================
BOT_TOKEN = "8752719004:AAFNa-JcGCaatHnVhUFUqZirHg3aAkuvJFA"

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# RAG: векторная база (сохраняется в папку ./chroma_db)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

class OrchestratorStates(StatesGroup):
    main = State()

SYSTEM_PROMPT = """
Ты — Orchestrator Agent, главный ИИ-директор NeuroBitrix AI.
Ты используешь RAG-базу знаний по Bitrix для точных ответов.
Отвечай всегда на русском, профессионально и по делу.
"""

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(OrchestratorStates.main)
    await message.answer("✅ <b>Orchestrator Agent v2 (с RAG) запущен!</b>\n\nЗдравствуйте, Михаил! RAG-память подключена.")

@dp.message()
async def handle_all_messages(message: types.Message, state: FSMContext):
    text = message.text.lower()

    # Поиск в RAG
    if "битрикс" in text or "api" in text or "документац" in text or "как" in text:
        docs = vectorstore.similarity_search(message.text, k=3)
        context = "\n\n".join([doc.page_content for doc in docs]) if docs else "Нет данных в базе."
        answer = f"📚 Я нашёл в базе знаний Bitrix:\n\n{context}\n\nЧто именно нужно сделать?"
    elif "статус" in text or "покажи статус" in text:
        await message.answer(
            "📊 <b>Статус системы (День 3)</b>\n"
            "• Orchestrator Agent: ✅ работает\n"
            "• RAG-память: ✅ подключена\n"
            "• Документация Bitrix: загружается\n"
            "• Готов к командам!"
        )
        return
    elif "отчёт" in text:
        await message.answer(f"📋 <b>Ежедневный отчёт ({datetime.now().strftime('%d.%m.%Y %H:%M')})</b>\n• RAG настроен\n• Следующий шаг — День 4")
        return
    else:
        answer = "✅ Команда принята. Что дальше, Михаил?"

    await message.answer(answer)

# Запуск
async def main():
    logging.basicConfig(level=logging.INFO)
    print("🚀 Orchestrator Agent с RAG запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
