import aiosqlite

DB_NAME = "bot.db"

async def log_request(user_id: int, model: str, name: str, description: str, category: str, image_path: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT INTO logs (user_id, model, name, description, category, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, model, name, description, category, image_path))
        await db.commit()
