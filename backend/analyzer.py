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
        phonePattern = r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"
        namePatterns = [
            r"\bmy name is ([A-Z][a-z]+)\b",
            r"\bi am ([A-Z][a-z]+)\b",
            r"\bcall me ([A-Z][a-z]+)\b"
        ]

        for conversation in conversations:
            for message in conversation["messages"]:
                numofMessages += 1
                text = message["content"]
                found_emails = re.findall(emailPattern, text)

                for email in found_emails:
                    findings.append({
                        "type": "email",
                        "category": "contact",
                        "value": email,
                        "conversation": conversation.get("title", "Untitled"),
                        "role": message["role"],
                        "evidence": text
                    })
                
                found_phones = re.findall(phonePattern, text)

                for phone in found_phones:
                    findings.append({
                        "type": "phone",
                        "category": "contact",
                        "value": phone,
                        "conversation": conversation.get("title", "Untitled"),
                        "role": message["role"],
                        "evidence": text 
                    })
                
                for pattern in namePatterns:
                    found_names = re.findall(pattern, text, re.IGNORECASE)

                    for name in found_names:
                        findings.append({
                        "type": "name",
                        "category": "identity",
                        "value": name,
                        "confidence": "high",
                        "conversation": conversation.get("title", "Untitled"),
                        "role": message["role"],
                        "evidence": text 
                        })

        return{
            "conversations":numofConvo,
            "messages":numofMessages,
            "findings": findings,
            "finding_count": len(findings)
        }   