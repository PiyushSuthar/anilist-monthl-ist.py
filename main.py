from utils import fetchData, parseAndCreateStr

username = input("Username:- ")

data = fetchData(username=username)

string = parseAndCreateStr(data)

print(string)
