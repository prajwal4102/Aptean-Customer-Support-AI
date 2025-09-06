from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
import os
import mysql.connector
from typing import List, Dict, Any

# API key
os.environ["DEEPSEEK_API_KEY"] = "sk-636335104afd4684b0d6147df2a3a9a9"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# MySQL connection details
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'customer_support_database',
    'port': 3306
}

# LLM
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

# Prompts
sql_prompt = ChatPromptTemplate.from_template("""
Based on table schema below, write a SQL query for user's question. Do not include backticks or markdown in the response.
{schema}
question: {question}
SQL query:
""")

response_prompt = ChatPromptTemplate.from_template("""
Based on schema, question, SQL query, and SQL response, write natural language answer. No backticks or markdown.
{schema}
question: {question}
SQL query: {query}
SQL response: {response}
""")

# FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

class Question(BaseModel):
    question: str

# Database connection function
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Helper function to execute queries and return results as dictionaries
def execute_query(query: str, params: tuple = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Database error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Helper functions for the chatbot
def generate_sql(question: str):
    # For simplicity, we'll use the direct database connection for schema info
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get table information
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        schema_info = ""
        for table in tables:
            cursor.execute(f"DESCRIBE {table}")
            columns = cursor.fetchall()
            schema_info += f"Table: {table}\nColumns:\n"
            for col in columns:
                schema_info += f"  - {col[0]} ({col[1]})\n"
            schema_info += "\n"
        
        prompt_text = sql_prompt.format(schema=schema_info, question=question)
        response = llm.invoke(prompt_text)
        
        # Extract text content if it's an AIMessage
        if hasattr(response, "content"):
            sql_query = response.content
        else:
            sql_query = str(response)
            
        return sql_query
    except Exception as e:
        print(f"Error generating SQL: {e}")
        return "SELECT 1"  # Fallback query
    finally:
        cursor.close()
        conn.close()

def generate_answer(question: str):
    try:
        sql = generate_sql(question)
        result = execute_query(sql)
        prompt_text = response_prompt.format(
            schema="Database schema information",
            question=question,
            query=sql,
            response=str(result)
        )
        response = llm.invoke(prompt_text)
        
        # Extract text content
        if hasattr(response, "content"):
            answer = response.content
        else:
            answer = str(response)
            
        return answer
    except Exception as e:
        print(f"Error generating answer: {e}")
        return f"Sorry, I encountered an error: {str(e)}"

# Endpoints for dashboard data
@app.get("/tickets")
def get_tickets():
    """Return all tickets with customer and agent information"""
    try:
        query = """
        SELECT 
            t.ticket_id as id,
            c.company_name as company,
            c.contact_name as contact,
            t.subject,
            t.status,
            t.priority,
            u.name as assigned_to
        FROM tickets t
        LEFT JOIN customers c ON t.customer_id = c.customer_id
        LEFT JOIN users u ON t.assigned_to = u.user_id
        ORDER BY t.created_at DESC
        """
        result = execute_query(query)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/customers")
def get_customers():
    """Return all customers"""
    try:
        query = "SELECT customer_id as id, company_name as company, contact_name as contact, email, phone FROM customers"
        result = execute_query(query)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/users")
def get_users():
    """Return all users"""
    try:
        query = "SELECT user_id as id, name, email, role, department FROM users"
        result = execute_query(query)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/agents")
def get_agents():
    """Return all agents with their active ticket count"""
    try:
        query = """
        SELECT 
            u.user_id as id,
            u.name,
            u.department,
            COUNT(t.ticket_id) as active_tickets
        FROM users u
        LEFT JOIN tickets t ON u.user_id = t.assigned_to AND t.status IN ('Open', 'In Progress')
        WHERE u.role = 'Agent'
        GROUP BY u.user_id, u.name, u.department
        """
        result = execute_query(query)
        return result
    except Exception as e:
        return {"error": str(e)}

# Chatbot endpoint
@app.post("/ask")
def ask_question(q: Question):
    try:
        answer = generate_answer(q.question)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "OK", "message": "Customer Support API is running"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)