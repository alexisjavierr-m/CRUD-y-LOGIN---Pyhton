import pandas as pd

class DataProcessor:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_common_and_unique_values(self, table_name, column_name, file_path):
        cur = self.db_conn.conn.cursor()
        # Query for distinct values in the specified column of the specified table that match values in the dataframe
        df = pd.read_csv(file_path + '.csv', sep=',', error_bad_lines=False)
        columns = df.columns
        lowercase_columns = [col.lower() if col.strip() != "" else col for col in columns]
        df.columns = lowercase_columns
        mi_lista = df[column_name].to_numpy()
        cur.execute(f"SELECT DISTINCT {column_name} FROM {table_name} WHERE {column_name} IN %s", (tuple(mi_lista),))
        results = cur.fetchall()
        unique_values = [str(value[0]) for value in results]

        # Find common and unique values
        common_values = set(unique_values) & set(mi_lista)
        unique_array_values = set(mi_lista) - set(unique_values)

        return common_values, unique_array_values

    def print_common_and_unique_values(self, common_values, unique_array_values):
        print("Valores que conciden:\n", common_values)
        print("Valores que no se encuentran en la base de datos:\n", unique_array_values)
