import sqlite3
from pathlib import Path


DB_PATH = (
    Path(__file__).parent.parent
    / "database"
    / "rental.db"
)



def show_table(table_name):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()


    print("\n======================")
    print(table_name.upper())
    print("======================\n")


    cursor.execute(
        f"SELECT * FROM {table_name}"
    )


    rows = cursor.fetchall()


    columns = [
        description[0]
        for description in cursor.description
    ]


    print(columns)


    for row in rows:
        print(row)


    print(
        "\nTotal rows:",
        len(rows)
    )


    connection.close()





if __name__ == "__main__":


    show_table("listings")

    show_table("images")