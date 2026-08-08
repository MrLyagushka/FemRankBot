import aiosqlite

class DB_DownloadPhoto():
    def __init__(self, PATH_TO_DB_PHOTO):
        self.path_to_db = PATH_TO_DB_PHOTO
        self.db = None
    
    async def _ensure_connection(self):
        if self.db is None:   
            self.db = await aiosqlite.connect(self.path_to_db)
            self.db.row_factory = aiosqlite.Row 

        cursor = await self.db.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_photo 
            ON photo(user_id, file_id, media_group_id)
        """)
        
        # Индекс для mark
        cursor = await self.db.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_mark 
            ON mark(p_id, user_id, author_id)
        """)
        await self.db.commit()
    
    async def new_download_photo(self, user_id, file_id, media_group_id, caption):
        await self._ensure_connection()
        data = await self.db.execute("INSERT OR IGNORE INTO photo (user_id, file_id, media_group_id, caption) VALUES (?, ?, ?, ?) RETURNING id", (user_id, file_id, media_group_id, caption))
        try:
            data = (await data.fetchone())['id']
            await self.db.commit()
            return data
        except TypeError:
            return -999999999
    
    async def update_download_photo(self, file_id, BLOB):
        await self._ensure_connection()
        await self.db.execute("UPDATE photo SET BLOB=? WHERE file_id=?", (BLOB, file_id))
        await self.db.commit()
    
    async def get_download_photo(self):
        await self._ensure_connection()
        cursor = await self.db.execute("SELECT id, user_id, file_id, media_group_id, caption FROM photo")
        return await cursor.fetchall()

    async def delete_photo(self, primary_key):
        await self._ensure_connection()
        await self.db.execute("DELETE FROM photo WHERE id = ?", (primary_key,))
        await self.db.commit()

    async def get_download_photo_where_id(self, id):
        await self._ensure_connection()
        cursor = await self.db.execute("SELECT user_id, file_id, media_group_id, caption FROM photo WHERE id=?", (id,))
        return await cursor.fetchone()

    async def get_download_photo_where_user_id(self, user_id):
        await self._ensure_connection()
        cursor = await self.db.execute("SELECT id, file_id, media_group_id, caption FROM photo WHERE user_id=?", (user_id,))
        return await cursor.fetchall()

    async def new_mark(self, p_id, user_id, author_id, mark):
        await self._ensure_connection()
        cursor = await self.db.execute("INSERT INTO mark (p_id, user_id, author_id, mark) VALUES (?, ?, ?, ?) ON CONFLICT(p_id, user_id, author_id) DO UPDATE SET mark = excluded.mark ", (p_id, user_id, author_id, mark))
        await self.db.commit()
    
    async def update_mark(self, mark_id, mark):
        await self._ensure_connection()
        cursor = await self.db.execute("UPDATE mark SET mark=? WHERE id=?", (mark, mark_id))
        await self.db.commit()
    
    async def get_mark(self):
        await self._ensure_connection()
        cursor = await self.db.execute("SELECT * FROM mark")
        self.marks = await cursor.fetchall()

    async def get_average_mark(self, primary_key):
            await self._ensure_connection()
            cursor = await self.db.execute("SELECT mark FROM mark WHERE p_id = ?", (primary_key,))
            marks = await cursor.fetchall()
            marks = [mark['mark'] for mark in marks]
            try:
                return round(sum(marks)/len(marks),1)
            except ZeroDivisionError:
                return '⭐️'
    async def close(self):
        if self.db:
            await self.db.close()
            self.db = None