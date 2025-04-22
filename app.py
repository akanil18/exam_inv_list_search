# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from extract import extract_records
from database import create_table, insert_records, get_connection
import os

app = Flask(__name__)
CORS(app);
create_table()

@app.route("/")
def index():
    return {"status": "Invigilation API is running"}

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    
    if not file:
        print("❌ No file uploaded.")
        return jsonify({"error": "Please upload a valid PDF"}), 400
    
    if not file.filename.endswith(".pdf"):
        print(f"❌ Invalid file type: {file.filename}")
        return jsonify({"error": "Please upload a valid PDF"}), 400

    print(f"✅ File uploaded: {file.filename}")
    
    # Save and extract records
    filepath = os.path.join("temp.pdf")
    file.save(filepath)
    print(f"📂 File saved as: {filepath}")
    
    with open(filepath, "rb") as f:
        records = extract_records(f)
    
    print(f"📄 Extracted {len(records)} records.")
    
    insert_records(records)
    
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"{filepath} has been deleted.")
    else:
        print(f"{filepath} does not exist.")

    return jsonify({"message": f"{len(records)} records inserted."})



@app.route("/search/teacher")
def search_teacher():
    print(request.args)
    name = request.args.get("name", "").strip().lower()
    print(f"🔍 Searching for teacher: {name}")

    if not name:
        return jsonify({"error": "No name provided"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM invigilation_records WHERE LOWER(teacher) LIKE ?", (f"%{name}%",))
        results = [dict(row) for row in cursor.fetchall()]
        print(f"🔎 Found {len(results)} records for teacher '{name}'.")
        return jsonify(results)
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return jsonify({"error": "An error occurred while searching"}), 500
    finally:
        conn.close()


@app.route("/search/room")
def search_room():
    room = request.args.get("room", "").lower()
    print(f"🔍 Searching for room: {room}")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invigilation_records WHERE LOWER(room) LIKE ?", ('%' + room + '%',))
    results = [dict(row) for row in cursor.fetchall()]
    
    print(f"🔎 Found {len(results)} records for room {room}.")
    return jsonify(results)

if __name__ == "__main__":
    print("🚀 Flask App is starting...")
    app.run(debug=True, use_reloader=False)