from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as ai

# Load all environment variables
load_dotenv()

# Configure the API key
ai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model and convert text to SQL query
def get_gemini_response(question, prompt):
    model = ai.GenerativeModel('gemini-pro')
    # Combine prompt and question into a single string
    combined_input = f"{prompt}\n{question}"
    response = model.generate_content(combined_input)
    return response.text

# Function to retrieve query results from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

# Defining the prompt for the trains_schedule database
prompt = '''
In this project, we have a database named trains_ with columns for train_name, train_number, source, destination, distance, total_time, departure, and arrival. The goal is to generate SQL queries dynamically based on user questions. For example,If the question is "Show all trains departing from station XYZ", the corresponding SQL query should be SELECT * FROM trains_ WHERE source = 'XYZ'. If the question is "Show me train with number 12345", the corresponding SQL query should be SELECT * FROM trains_ WHERE train_number = 12345;.
This approach allows users to retrieve specific information from the train schedule database through natural language queries. The SQL code should not have any delimiters like backticks or the word "SQL" in the output.
'''
#SELECT * FROM trains_ WHERE train_number = 12345;

# Streamlit app
st.set_page_config(page_title='Retrieve SQL Data')
st.header("Gemini App to Retrieve Train Schedule Data")
question = st.text_input("Input:", key="input")
submit = st.button("Ask the Question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.write(f"Generated SQL Query: {response}")
    
    try:
        data = read_sql_query(response, 'trains_.db')
        st.subheader("The Response is:")
        # Display the results in a readable format
        if data:
            for row in data:
                st.write(row)
        else:
            st.write("No data found.")
    except Exception as e:
        st.write(f"Error executing SQL query: {e}")
