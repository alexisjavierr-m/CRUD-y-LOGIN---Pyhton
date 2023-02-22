import json
from Data_Processor import DataProcessor
from Database_Connection import DatabaseConnection

class Application:
    def __init__(self, host, port, dbname, user, password, table_name, column_name, file_path):
        self.db = DatabaseConnection(host, port, dbname, user, password)
        self.processor = DataProcessor(self.db)
        self.table_name = table_name
        self.column_name = column_name
        self.file_path = file_path

    def run(self):
        self.db.connect()
        common_values, unique_values = self.processor.get_common_and_unique_values(self.table_name, self.column_name, self.file_path)
        self.processor.print_common_and_unique_values(common_values, unique_values)
        self.db.disconnect()



if __name__ == "__main__":
    with open('config.json') as config_file:
        config = json.load(config_file)

    app = Application(
        config['host'],
        config['port'],
        config['dbname'],
        config['user'],
        config['password'],
        config['table_name'],
        config['column_name'],
        config['file_path']
    )
    app.run()