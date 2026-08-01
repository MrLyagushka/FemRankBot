import aiosqlite

class DB_DownloadPhoto():
    def __init__(self, PATH_TO_DB_PHOTO):
        self.path_to_db = PATH_TO_DB_PHOTO
        self.db = None
    async def _ensure_connection(self):
        if self.db is None:   
            self.db = await aiosqlite.connect(self.path_to_db)
            self.db.row_factory = aiosqlite.Row 

            await self.db.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_photo 
                ON photo(user_id, file_id, media_group_id)
            """)
            await self.db.commit()
    async def new_download_photo(self, user_id, file_id, media_group_id, caption):
        await self._ensure_connection()
        await self.db.execute("INSERT OR IGNORE INTO photo (user_id, file_id, media_group_id, caption) VALUES (?, ?, ?, ?)", (user_id, file_id, media_group_id, caption))
        await self.db.commit()
    async def update_download_photo(self, file_id, BLOB):
        await self._ensure_connection()
        await self.db.execute("UPDATE photo SET BLOB=? WHERE file_id=?", (BLOB, file_id))
        await self.db.commit()
    async def get_download_photo(self):
        await self._ensure_connection()
        cursor = await self.db.execute("SELECT user_id, file_id, media_group_id, caption FROM photo")
        self.groups = await cursor.fetchall()
    async def close(self):
        if self.db:
            await self.db.close()
            self.db = None