import sqlite3

class DatabaseInstance: # creates a Connection object & a cursor from it as well
    def __init__(self, database_path) -> None:
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()

    def execute(self, query, data): # calling the Cursor's execute() method
        self.cur.execute(query, data)
        self.conn.commit()
        return self.cur

    def execute_to_many(self, query, data): # same as above except you can pass many more arguments as a list
        self.cur.executemany(query, data)
        self.conn.commit()
        return self.cur

    def execute_script(self, script): # passes a SQL script 
        self.cur.executescript(script)
        self.conn.commit()
        return self.cur

    def add_dsr(self, dsr_name): # creates a method to add dsr(s)
        return self.execute("INSERT INTO dsr (dsr_name) VALUES (?)", (dsr_name,))

    def add_product(self, product_name):
        return self.execute("INSERT INTO products (product_name) VALUES (?)", (product_name,))

    def add_dsr_target(self, dsr_id, product_id, dsr_target, date):
        return self.execute(
            """INSERT INTO dsr_targets (
                dsr_id, product_id, dsr_target, date
            )
            VALUES (?,?,?,?)""", (dsr_id, product_id, dsr_target, date)
        )

    def add_dsr_sales(self, dsr_id, product_id, sales, date):
        return self.execute(
            """INSERT INTO dsr_sales (
                dsr_id, product_id, sales, date
            )
            VALUES (?,?,?,?)""", (dsr_id, product_id, sales, date)
        )

    def __del__(self): # closes the session
        self.conn.close()

def main():
    sales_db = DatabaseInstance("sales.db")
    sales_db.execute_script(
        """
        DROP TABLE IF EXISTS dsr;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS dsr_targets;
        DROP TABLE IF EXISTS dsr_sales;

        CREATE TABLE dsr (
            dsr_id integer PRIMARY KEY,
            dsr_name text NOT NULL
        );

        CREATE TABLE products (
            product_id integer PRIMARY KEY,
            product_name text NOT NULL
        );

        CREATE TABLE dsr_targets (
            dsr_id integer NOT NULL,
            product_id integer NOT NULL,
            dsr_target integer NOT NULL,
            date text NOT NULL,
            FOREIGN KEY (dsr_id)
            REFERENCES dsr (dsr_id)
                ON UPDATE SET NULL
                ON DELETE SET NULL,
            FOREIGN KEY (product_id)
            REFERENCES products (product_id)
                ON UPDATE SET NULL
                ON DELETE SET NULL
        );

        CREATE TABLE dsr_sales (
            dsr_id integer NOT NULL,
            product_id integer NOT NULL,
            sales integer NOT NULL,
            date text NOT NULL,
            FOREIGN KEY (dsr_id)
            REFERENCES dsr (dsr_id)
                ON UPDATE SET NULL
                ON DELETE SET NULL,
            FOREIGN KEY (product_id)
            REFERENCES products (product_id)
                ON UPDATE SET NULL
                ON DELETE SET NULL
        );
        """
    )

    sales_db.add_dsr("Andrew")
    sales_db.add_product("Detergent")
    sales_db.add_dsr_target(1, 1, 20000, "22/03/2021")
    sales_db.add_dsr_sales(1, 1, 5000, "22/03/2021")



if __name__ == "__main__":
    main()

