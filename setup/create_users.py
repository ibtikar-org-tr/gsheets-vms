import csv
import requests

# Read the CSV file
with open('contacts.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    rows = list(csv_reader)

port = input("port: ")

for row in rows:
    username = row[0]
    password = row[1]

    # Define the URL and payload
    url = "http://127.0.0.1:" + port + '/user' + "?username=" + username + "&password=" + password

    # Make the POST request
    response = requests.post(url)

    # Print the response
    print(response.text)
