import aiosqlite

class DB_Group():
    def __init__(self, PATH_TO_DB_DATA):
        self.path_to_db = PATH_TO_DB_DATA
        self.db = None
    
    async def _ensure_connection(self):
        if self.db is None:   
            self.db = await aiosqlite.connect(self.path_to_db)
            self.db.row_factory = aiosqlite.Row 
    
    async def new_group(self, id, type, status, full_name):
        await self._ensure_connection()
        await self.db.execute("INSERT INTO group_data (id, type, status, full_name, 1) VALUES (?, ?, ?, ?)", (id, type, status, full_name))
        await self.db.commit()
    
    async def update_group(self, id, type, status, full_name, on_off):
        await self._ensure_connection()
        await self.db.execute("UPDATE group_data SET type=?, status=?, full_name=?, on_off=? WHERE id=?", (type, status, full_name, on_off, int(id)))
        await self.db.commit()
    
    async def get_groups(self):
        await self._ensure_connection()
        cursor = await self.db.execute("SELECT * FROM group_data")
        return await cursor.fetchall()
    
    async def close(self):
        if self.db:
            await self.db.close()
            self.db = None