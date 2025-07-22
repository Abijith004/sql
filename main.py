import os
import openai
import sqlite3
from dotenv import load_dotenv
from utils.db_schema_loader import load_schema
from utils.query_validator import validate_query

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_sql_query(prompt: str, schema: str) -> str:
    """Generate SQL query using OpenAI"""
    try:
        response = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4'),
            messages=[
                {"role": "system", "content": f"""You are a SQL expert. 
Generate standard SQL queries based on the following schema:
{schema}
Return only the SQL query without any explanations or markdown formatting."""},
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
        raise Exception(f"Error generating SQL query: {str(e)}")

def run_query(sql: str) -> str:
    """Run generated SQL query on SQLite database"""
    conn = sqlite3.connect('sample.db')  # Ensure DB exists
    try:
        result = conn.execute(sql).fetchall()
        return str(result)
    except Exception as e:
        return f"❌ SQL Execution Error: {e}"
    finally:
        conn.close()

if __name__ == "__main__":
    schema = load_schema("schema/sample_schema.sql")

    while True:
        print("\nEnter your query request (or 'quit' to exit):")
        user_prompt = input("> ")

        if user_prompt.lower() in ['quit', 'exit']:
            break

        try:
            sql_query = generate_sql_query(user_prompt, schema)
            print("\n✅ Generated SQL Query:\n", sql_query)

            result = run_query(sql_query)
            print("\n📊 Query Result:\n", result)

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
