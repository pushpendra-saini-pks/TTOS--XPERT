from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text

## function to retrieve the query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# define prompt
prompt = [
    """
    you are an expert in converting English question to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME , CLASS ,
    SECTION and MARKS \n\nFor example, \nExample 1 - How many entries of records are present 
    the SQL Command will be something like this SELECT COUNT(*) FROM STUDENT;
    \nExample 2 - Tell me all the students studying in Data Science class?,
    the SQL command will be something like this SELECT * FROM STUDENT
    where CLASS="Data Science";
    also the sql code should not have 
    in beginning or end and sql word in output
    """
]

# streamlit app
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("TTOS-Xpert")
st.subheader("You can ask anything about your database with TEXT TO SQL Xpert..")

def main():
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'responses' not in st.session_state:
        st.session_state.responses = []
    if 'current_input' not in st.session_state:
        st.session_state.current_input = ""

    # Display all previous questions and responses
    for i, (question, response) in enumerate(zip(st.session_state.questions, st.session_state.responses)):
        st.subheader(f"Query {i+1}:")
        st.write(question)
        st.subheader("Answer:")
        for row in response:
            st.write(row)

    # Input section for the current question
    st.session_state.current_input = st.text_input("Input: ", value=st.session_state.current_input, key="input")

    if st.button("Submit"):
        if st.session_state.current_input:
            question = st.session_state.current_input
            response = get_gemini_response(question, prompt)
            data = read_sql_query(response, "student.db")
            # Update the session state immediately
            st.session_state.questions.append(question)
            st.session_state.responses.append(data)
            st.session_state.current_input = ""  # Clear the input field after submission
            st.rerun()  # Rerun the app to update the display

if __name__ == "__main__":
    main()
