import aiosqlite

class DB_User():
    def __init__(self, PATH_TO_DB_DATA):
        self.path_to_db = PATH_TO_DB_DATA
        self.db = None
    
    async def _ensure_connection(self):
        if self.db is None:   
            self.db = await aiosqlite.connect(self.path_to_db)
            self.db.row_factory = aiosqlite.Row 

        cursor = await self.db.execute("""
                    CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_user 
                    ON users(user_id)
                """)
        await self.db.commit()

    async def new_user(self, user_id, username, first_name, last_name):
        await self._ensure_connection()
        await self.db.execute("INSERT INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET username=excluded.username, first_name=excluded.first_name, last_name=excluded.last_name", (user_id, username, first_name, last_name))
        await self.db.commit()
        
    async def update_user(self, user_id, username, first_name, last_name):
        await self._ensure_connection()
        await self.db.execute("UPDATE users SET user_id=?, username=?, first_name=?, last_name=? WHERE user_id=?", (username, first_name, last_name, user_id))
        await self.db.commit()
    
    async def get_users(self):
        await self._ensure_connection()
        cursor = await self.db.execute("SELECT * FROM users")
        return await cursor.fetchall()