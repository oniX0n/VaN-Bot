import sqlite3


class BotDb:

    def __init__(self, file):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()

    async def insert_message(self, author, content, channel, date_send):
        format_str = """INSERT INTO message (message_number, author, content, channel, date_send)
            VALUES (NULL, "{author}", "{content}", "{channel}", "{date_send}");"""
        sql_command = format_str.format(author=author, content=content, channel=channel, date_send=date_send)
        self.cursor.execute(sql_command)
        self.connection.commit()
