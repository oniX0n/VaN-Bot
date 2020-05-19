import sqlite3


class BotDb:

    def __init__(self, file):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()

    async def insert(self, table, params):
        cmd = 'INSERT INTO ' + table + ' VALUES (NULL'
        for param in params:
            if param == 'NULL':
                cmd += ', NULL'
            else:
                cmd += ", '" + str(param) + "'"
        cmd += ')'
        self.cursor.execute(cmd)
        self.connection.commit()
