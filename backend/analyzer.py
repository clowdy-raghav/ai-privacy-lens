import json
import re

def analyze_conversations():

    file_path = "sample_data/conversations.json"

    with open(file_path, "r") as file:
        conversations = json.load(file)

        numofMessages = 0
        numofConvo = len(conversations)
        emails = []

        emailPattern = r"[\w\.-]+@[\w\.-]+\.\w+"

        for conversation in conversations:
            for message in conversation["messages"]:
                numofMessages += 1
                text = message["content"]
                found_emails = re.findall(emailPattern, text)

                for email in found_emails:
                    emails.append({
                        "value": email,
                        "conversation": conversation.get("title", "Untitled"),
                        "role": message["role"],
                        "evidence": text
                    })

        return{
            "conversations":numofConvo,
            "messages":numofMessages,
            "emails": emails
        }   