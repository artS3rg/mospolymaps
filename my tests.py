from db import BotDB
BotDB = BotDB('db.db')
images_id = BotDB.cursor.execute("SELECT image_id FROM information WHERE id = ?", (1,)).fetchone()[0].split(';')
print(images_id)
