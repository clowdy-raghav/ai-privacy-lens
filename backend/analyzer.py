import json

def analyze_conversations():

    file_path = "sample_data/conversations.json"

    with open(file_path, "r") as file:
        content = json.load(file)

        numofMessages = 0

        numofConvo = len(content)

        for conversation in content:
            numofMessages+=len(conversation["messages"])

        return{
            "conversations":numofConvo,
            "messages":numofMessages
        }   