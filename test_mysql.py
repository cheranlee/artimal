import mysql.connector as mysql

connection = mysql.connect(
    user='root',
    password='',
    database='test',
    unix_socket='/tmp/mysql.sock'
)

cursor = connection.cursor()

'''
search_value = input("Enter search term: ")

query = "SELECT QuestionId FROM Otter WHERE Question LIKE '%" + search_value + "%'"

cursor.execute(query)

# Fetch and display results
index = cursor.fetchone()

if index is None:
    print("No results found")
    exit()

question_id = str(index[0])


query1 = "SELECT Answer FROM Otter WHERE QuestionId=" + question_id
 
cursor.reset()

cursor.execute(query1)

results = cursor.fetchone()

'''
query = "SELECT MAX(QuestionId) FROM Otter"

cursor.execute(query)
result = cursor.fetchone()  

print(result[0])

cursor.reset()  

prompt = "INSERT INTO Otter(Question, Answer) VALUES(%s, %s)"

cursor.execute(prompt, ("What is the capital of France?", "Paris"))  

connection.commit() #required to save changes to the database

# Close the connection
connection.close()  