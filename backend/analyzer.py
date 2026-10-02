import json
import re

def analyze_conversations():

    file_path = "sample_data/conversations.json"

    with open(file_path, "r") as file:
        conversations = json.load(file)

        numofMessages = 0
        numofConvo = len(conversations)
        findings = []

        emailPattern = r"[\w\.-]+@[\w\.-]+\.\w+"
        phone_pattern = r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"

        for conversation in conversations:
            for message in conversation["messages"]:
                numofMessages += 1
                text = message["content"]
                found_emails = re.findall(emailPattern, text)

                for email in found_emails:
                    findings.append({
                        "type": "email",
                        "value": email,
                        "conversation": conversation.get("title", "Untitled"),
                        "role": message["role"],
                        "evidence": text
                    })
                
                found_phones = re.findall(phone_pattern, text)

                for phone in found_phones:
                    findings.append({
                        "type": "phone",
                        "value": phone,
                        "conversation": conversation.get("title", "Untitled"),
                        "role": message["role"],
                        "evidence": text 
                    })

        return{
            "conversations":numofConvo,
            "messages":numofMessages,
            "findings": findings
        }   