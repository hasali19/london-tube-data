import json
import psycopg2

conn = psycopg2.connect(host="localhost", database="london_tube", user="postgres", password="postgres")
cur = conn.cursor()

with open("train-network.json") as data_file:
    dataset = json.loads(data_file.read())
    
for station in dataset["stations"]:
    sql = "INSERT INTO stations (id, name, latitude, longitude) VALUES (%s, %s, %s, %s)"
    cur.execute(sql, vars=[station["id"], station["name"], station["latitude"], station["longitude"]])

for line in dataset["lines"]:
    sql = "INSERT INTO lines (name) VALUES (%s) RETURNING id"
    cur.execute(sql, [line["name"]])
    line_id = cur.fetchone()[0]
    for station in line["stations"]:
        sql = "INSERT INTO stations_lines (station_id, line_id) VALUES (%s, %s)"
        cur.execute(sql, [station, line_id])

conn.commit()
cur.close()
