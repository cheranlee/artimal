import mysql.connector as mysql

connection = mysql.connect(
    
)

cursor = connection.cursor()

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

print(results[0])

# Close the connection
connection.close()  