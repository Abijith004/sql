# 🧠 AI-Powered SQL Query Generator

This project leverages OpenAI's GPT models to automatically generate and execute **SQL queries** based on natural language prompts, using a **sample SQLite database** and schema.

---

## 🚀 Features

- 🤖 **AI-Generated Queries**: Converts natural language input into valid SQL queries using OpenAI GPT models.
- 🔍 **Schema-Aware**: Queries are generated based on a provided schema file.
- ✅ **Validation**: All generated queries are syntax-checked before execution.
- 🗃️ **SQLite Integration**: Runs validated queries on a local SQLite database.
- 🔐 **Environment-Based Configuration**: Uses `.env` to manage API keys and model names securely.

---

## 📂 Project Structure
sql/
├── utils/
│ ├── db_schema_loader.py # Loads SQL schema from file
│ └── query_validator.py # Validates SQL syntax
├── schema/
│ └── sample_schema.sql # Example schema used for query generation
├── .env # Stores OpenAI API key and model name
├── main.py # Main script for query generation & execution
├── README.md # Project documentation
└── sample.db # SQLite database (optional/test)
