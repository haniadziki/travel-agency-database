import mysql.connector

con = mysql.connector.connect(
    host="giniewicz.it",
    user="team10",
    password="te@mzaio",
    database="team10"
)

mycursor = con.cursor()

salary_values = [5000, 7000, 6500, 5500, 7500, 5500]

mycursor.execute("SELECT staff_id FROM staff ORDER BY staff_id")
staff_ids = [row[0] for row in mycursor.fetchall()]

for staff_id, salary in zip(staff_ids, salary_values):
    mycursor.execute("INSERT INTO salary (staff_id, salary) VALUES (%s, %s)", (staff_id, salary))

con.commit()
mycursor.close()
con.close()
