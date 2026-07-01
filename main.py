import pandas as pd
import sqlite3 as sq
import matplotlib.pyplot as mp

# Read CSV file
df = pd.read_csv("employees.csv")

while True:

    name = input(
        "Enter the first name of the employee (FIRST LETTER CAPITAL): "
    )

    # Search employee by first name
    employee = df.loc[df['First Name'] == name]

    if not employee.empty:

        print(
            f"\nThere are {len(employee)} employees with the first name {name}\n"
        )

        names = []
        experience = []

        # Display matching employees
        for idx, row in enumerate(employee.itertuples(), start=1):

            print(
                f"{idx}. {row[1]} {row[2]}"
            )

            names.append(
                row[1] + " " + row[2]
            )

            experience.append(
                row[8]  # Years Of Experience
            )

        try:

            n = int(
                input(
                    "\nSelect an employee by entering their number: "
                )
            )

            if n < 1 or n > len(employee):
                print("\nInvalid Employee Number")
                continue

            selected = employee.iloc[n - 1]

            print("\nEmployee Details:\n")
            print(selected)

            # SQLite Database Connection
            con = sq.connect("employees.db")

            # Create Table
            con.execute("""
            CREATE TABLE IF NOT EXISTS employee_results
            (
                first_name TEXT,
                last_name TEXT,
                department TEXT,
                salary REAL,
                job_title TEXT,
                years_of_experience INTEGER,
                phone TEXT,
                email TEXT
            )
            """)

            # Insert Data
            con.execute("""
            INSERT INTO employee_results
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                selected['First Name'],
                selected['Last Name'],
                selected['Department'],
                selected['Salary'],
                selected['Job Title'],
                int(selected['Years Of Experience']),
                selected['Phone'],
                selected['Email']
            ))

            con.commit()

            # Display Database Records
            cursor = con.cursor()

            cursor.execute(
                "SELECT * FROM employee_results"
            )

            data = cursor.fetchall()

            print("\nData saved in database:\n")

            count = 1

            for row in data:

                print(
                    count,
                    ".",
                    row
                )

                count += 1

            cursor.close()
            con.close()

            # Plot Graph

            mp.figure(figsize=(10, 5))

            mp.xlabel("FULL NAME")
            mp.ylabel("Years Of Experience")

            mp.bar(
                names,
                experience,
                color='c'
            )

            mp.legend(
                ["Experience Data"],
                loc="upper left"
            )

            mp.xticks(rotation=45)

            mp.tight_layout()

            mp.show()

        except ValueError:

            print("\nPlease enter a valid number.")

        except Exception as e:

            print("\nError:", e)

    else:

        print(
            f"\nError: NO EMPLOYEE FOUND with the first name: {name}"
        )

    k = input(
        "\nWant to search for another employee? [y/n]: "
    )

    if k.lower() == 'n':
        print("\nThank You!")
        break