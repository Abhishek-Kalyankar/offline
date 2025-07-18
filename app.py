from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Database connection details
DB_CONFIG = {
    #"host": "127.0.0.1",
    "host" : "localhost"
    "database": "aircraft_db",
    "user": "postgres",
    "password": "Riti@2901",
    "port": 5432
}

def get_aircraft_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM aircraft_data;")
        rows = cursor.fetchall()

        # Filter rows with latitude and longitude present
        filtered = [r for r in rows if r[6] is not None and r[5] is not None]

        data = [
            {
                "icao24": s[0],
                "callsign": s[1],
                "origin_country": s[2],
                "time_position": s[3],
                "last_contact": s[4],
                "longitude": s[5],
                "latitude": s[6],
                "baro_altitude": s[7],
                "on_ground": s[8],
                "velocity": s[9],
                "true_track": s[10],
                "vertical_rate": s[11],
                "geo_altitude": s[13],
                "squawk": s[14],
                "spi": s[15],
                "position_source": s[16],
                "source": "opensky-live"
            }
            for s in filtered
        ]

        cursor.close()
        conn.close()

        return data

    except Exception as e:
        print("❌ Error fetching aircraft data:", e)
        return []

@app.route("/aircrafts", methods=["GET"])
def aircrafts():
    data = get_aircraft_data()
    return jsonify({
        "aircrafts": data,
        "count": len(data),
        "source": "db"
    })

if __name__ == "__main__":
    app.run(debug=True)
