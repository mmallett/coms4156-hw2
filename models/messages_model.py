from model import Model

class Messages(Model):

    def init_messages(self):
        result = self.db.execute("CREATE TABLE IF NOT EXISTS messages (id serial, message text);")
        return

    def get_messages(self):
        result = self.db.execute("SELECT * FROM messages;")
        return self.deproxy(result)

    def create_message(self, message):
        query = "INSERT INTO messages VALUES('$MESSAGE$');".replace('$MESSAGE$', message)
        result = self.db.execute(query)
        return

    def delete_message(self, id):
        query = "DELETE from messages where id = '$ID$'".replace('$ID$', id)
        result = self.db.execute(query)
        return
