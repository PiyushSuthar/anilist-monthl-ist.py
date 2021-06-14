import requests
import datetime

query: str = """
query ($username: String){
  MediaListCollection(userName: $username type: ANIME){
    lists {
      name
      status
      entries {
        id
        startedAt {
          year
          month
          day
        }
        completedAt{
          year
          month
          day
        }
        
        createdAt
        progress
        media{
          title {
            romaji
            english
            native
            userPreferred
          }
        }
      }
    }
  }
}
"""


def fetchData(username: str):
    payload = {
        "query": query,
        "variables": {
            "username": username
        }
    }

    req = requests.post("https://graphql.anilist.co", json=payload)

    data = req.json()
    return data


def parseAndCreateStr(data):
    lists: list = data["data"]["MediaListCollection"]["lists"]
    string = ""
    count = 1

    for single_list in lists:
        entries = single_list["entries"]

        for entry in entries:
            current_month = datetime.datetime.now().month
            previous_month = current_month - 1

            entryStartedMonth = entry["startedAt"]["month"]
            entryCompletedMonth = entry["completedAt"]["month"]

            entryTitle = entry["media"]["title"]["english"] or entry["media"]["title"]["native"]

            condition = (entryStartedMonth == current_month) or (entryCompletedMonth == current_month) or (
                entryStartedMonth == previous_month) or (entryCompletedMonth == previous_month)

            if condition:
                string += f"{count} {entryTitle} \n"
                count += 1

    return string
