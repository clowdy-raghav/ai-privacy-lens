import json

file_path = "sample_data/conversations.json"

with open(file_path, "r") as file:
    content = json.load(file)
    count = 0
    numofConvo = len(content)
    print("Number of Conversations: ", numofConvo)
    for conversation in content:
        count+=len(conversation["messages"])
    print("Number of Messages: ", count)
    for conversation in content:
        for message in conversation["messages"]:
            print(message["role"], " : ", message["content"])