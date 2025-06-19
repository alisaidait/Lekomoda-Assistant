import aiosqlite

DB_NAME = "db.sqlite3"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                ref_count INTEGER DEFAULT 0,
                ref_by INTEGER
            )
        ''')
        await db.commit()

async def add_user(user_id: int, ref_by: int = None):
    async with aiosqlite.connect(DB_NAME) as db:
        user = await db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        if await user.fetchone() is None:
            await db.execute("INSERT INTO users (id, ref_by) VALUES (?, ?)", (user_id, ref_by))
            if ref_by:
                await db.execute("UPDATE users SET ref_count = ref_count + 1 WHERE id = ?", (ref_by,))
            await db.commit()

async def get_progress(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT ref_count FROM users WHERE id = ?", (user_id,))
        row = await cursor.fetchone()
        return row[0] if row else 0 