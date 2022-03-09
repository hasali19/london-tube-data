import sys
import psycopg2

try:
    conn = psycopg2.connect(host="localhost", database="london_tube", user="postgres", password="postgres")
    cur = conn.cursor()
except:
    print("Couldn't connect to database", file=sys.stderr)
    exit(1)

def query_children(name, parent_table, child_table, parent_id_col, child_id_col):
    sql = f"SELECT id FROM {parent_table} WHERE name = %s"
    cur.execute(sql, [name])
    row = cur.fetchone()

    if not row:
        print(f"No {parent_table} found with name: {name}")
        return

    parent_id = row[0]

    sql = f"SELECT name FROM {child_table} JOIN stations_lines ON {child_table}.id = {child_id_col} WHERE {parent_id_col} = %s"
    cur.execute(sql, [parent_id])
    
    for row in cur.fetchall():
        print(row[0])

def get_station_lines(args):
    if len(args) < 1:
        print("Missing argument for station name")
        return

    station_name = " ".join(args)
    query_children(station_name, "stations", "lines", "station_id", "line_id")

def get_line_stations(args):
    if len(args) < 1:
        print("Missing argument for line name")
        return

    line_name = " ".join(args)
    query_children(line_name, "lines", "stations", "line_id", "station_id")

commands = {
    "get_station_lines": get_station_lines,
    "get_line_stations": get_line_stations,
}

def main():
    while True:
        cmd_line = input("> ")
        args = cmd_line.split(" ")

        cmd = args[0]
        args = args[1:]

        if cmd in ["quit", "exit", "q", "e"]:
            break

        if cmd not in commands:
            print(f"Invalid command: {cmd}")
        else:
            commands[cmd](args)


if __name__ == "__main__":
    main()

