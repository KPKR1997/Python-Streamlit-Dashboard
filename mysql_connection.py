import mysql.connector
import streamlit as st

#Connection

conn = mysql.connector.connect(
    host = "127.0.0.1",
    port = "3306",
    user = "root",
    password = "",
    db = "startup_funds"
)

c = conn.cursor()

def view_all_data():
    c.execute('SELECT * FROM startup_data ORDER BY Startup asc')
    data = c.fetchall()
    return data

