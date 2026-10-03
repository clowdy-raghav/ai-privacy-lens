import json
import re

def build_summary(findings):
    summary = {
        "total_findings": len(findings),
        "high_confidence": 0,
        "categories": {}
    }

    for finding in findings:
        if finding.get("confidence") == "high":
            summary["high_confidence"] += 1

        category = finding["category"]

        if category not in summary["categories"]:
            summary["categories"][category] = 0

        summary["categories"][category] += 1

    return summary

def build_category_summary(findings):
    
    categories = {}

    for finding in findings:
        category = finding["category"]

        if category not in categories:
            categories[category] = 0
        
        categories[category] += 1

    return categories

def build_recurrence(findings):

    recurrence = {}

    for finding in findings:

        key = finding["type"] + ":" + finding["value"].lower()

        if key not in recurrence:
            recurrence[key] = {
                "type": finding["type"],
                "category": finding["category"],
                "value": finding["value"],
                "conversation_count" : 0,
                "conversations": [],
                "evidence": []
            }

        item = recurrence[key]

        conversation = finding["conversation"]

        if conversation not in item["conversations"]:
            item["conversations"].append(conversation)
            item["conversation_count"] += 1

        item["evidence"].append({
            "conversation": conversation,
            "role": finding["role"],
            "text": finding["evidence"],
        })

    return list(recurrence.values())

def finding_exists(findings, finding):
    for existing in findings:
        if(
            existing["type"] == finding["type"]
            and existing["value"] == finding["value"]
            and existing["conversation"] == finding["conversation"]
            and existing["evidence"] == finding["evidence"]
        ):
            return True

        return False


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
            r"\bcall me ([A-Z][a-z]+)\b"]
        locations = ["Delhi",
                     "Meerut",
                     "Noida",
                     "Ghaziabad",
                     "Gurgaon",
                     "Mumbai",
                     "Banglore",
                     "Kolkata",
                     "Chennai"]
        institutions = ["Shivaji College",
                        "University of Delhi",
                        "Delhi University",
                        "IIT Delhi"]

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

                for location in locations:
                    if re.search(r"\b" + re.escape(location) + r"\b", text, re.IGNORECASE):
                        finding = {
                        "type": "location",
                        "category": "location",
                        "value": location,
                        "confidence": "high",
                        "conversation": conversation.get("title", "Untitled"),
                        "role": message["role"],
                        "evidence": text 
                        }

                        if not finding_exists(findings, finding):
                            findings.append(finding)

                for institution in institutions:
                    if re.search(r"\b" + re.escape(institution) + r"\b", text, re.IGNORECASE):
                        finding = {
                        "type": "institution",
                        "category": "education",
                        "value": institution,
                        "confidence": "high",
                        "conversation": conversation.get("title", "Untitled"),
                        "role": message["role"],
                        "evidence": text 
                        }

                        if not finding_exists(findings, finding):
                            findings.append(finding)

        recurrence = build_recurrence(findings)
        summary = build_summary(findings)
        category_summary = build_category_summary(findings)

        return{
            "conversations":numofConvo,
            "messages":numofMessages,
            "summary": summary,
            "findings": findings,
            "finding_count": len(findings),
            "recurrence": recurrence
        }   