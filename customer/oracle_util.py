import oracledb


class OracleDB:
    def __init__(self, user, password, dsn):
        self.user = user
        self.password = password
        self.dsn = dsn

    @classmethod
    def create_instance(cls):
        # This method initializes and returns an instance of OracleDB
        return cls(user="SYSTEM", password="Ritu#1507", dsn="localhost:1521/testdb")

    def execute_select(self, query, params=None):
        with oracledb.connect(user=self.user, password=self.password, dsn=self.dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params or {})
                return cursor.fetchall()

    def execute_insert_many(self, query, params=None):
        with oracledb.connect(user=self.user, password=self.password, dsn=self.dsn) as connection:
            with connection.cursor() as cursor:
                cursor.executemany(query, params or [])
                connection.commit()

    def execute_delete(self, query, params=None):
        with oracledb.connect(user=self.user, password=self.password, dsn=self.dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params or {})
                connection.commit()
