import os
import openai
import sqlite3
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils.db_schema_loader import load_schema
from utils.query_validator import validate_query

load_dotenv()

app = Flask(__name__)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
schema = load_schema("schema/sample_schema.sql")

def generate_sql_query(prompt: str, schema: str) -> str:
    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            messages=[
                {"role": "system", "content": f"You are a SQL expert. Use the schema:\n{schema}\nReturn only SQL."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        query = response.choices[0].message.content.strip()
        if validate_query(query):
            return query
        else:
            raise ValueError("Generated query failed validation")
    except Exception as e:
        raise Exception(f"Error generating SQL query: {e}")

def run_query(sql: str):
    conn = sqlite3.connect("sample.db")
    try:
        cursor = conn.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        return [dict(zip(columns, row)) for row in data]
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.route("/generate_sql", methods=["POST"])
def generate_sql():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        sql_query = generate_sql_query(prompt, schema)
        result = run_query(sql_query)
        return jsonify({
            "sql": sql_query,
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
