import json
import re

def build_infereces(findings, recurrence):
    inferences = []

    has_location = False
    has_morning_time = False
    has_commute = False

    location_value = None

    for finding in findings:
        text = finding["evidence"].lower()

        if finding["type"] == "location":
            has_location = True
            location_value = finding["value"]
        
        if "6:30" in text or "6.30" in text:
            has_morning_time = True
        
        if "commute" in text:
            has_commute = True

    print("LOCATION:", has_location)
    print("MORNING:", has_morning_time)
    print("COMMUTE:", has_commute)


    if has_location and has_morning_time and has_commute:
        inferences.append({
            "type": "routine",
            "classification": "potential_inference",
            "value": "Recurring early-morning college commute",
            "confidence": "medium",
            "explanation": "Multiple conversations mention a college location, an early departure time, and a long commute",
            "evidence": [
                finding["evidence"]
                for finding in findings
                if("6:30" in finding["evidence"]
                    or "6.30" in finding["evidence"]
                    or "commute" in finding["evidence"].lower()
                    or finding["type"] == "location")
            ]
        })
    return inferences

def build_privacy_profile(findings, recurrence):
    profile = {
        "identity": [],
        "contact": [],
        "location": [],
        "education": [],
        "other": []
    }

    for finding in findings:
        classification = finding.get("classification", "explicit")
        item = {
            "type": finding["type"],
            "value": finding["value"],
            "classification": classification,
            "confidence": finding.get("confidence", "unknown"),
            "conversation_id": finding.get("conversation_id"),
            "conversation": finding["conversation"],
            "evidence": finding["evidence"]
        }

        category = finding["category"]

        if category == "identity":
            profile["identity"].append(item)
        elif category == "contact":
            profile["contact"].append(item)
        elif category == "location":
            profile["location"].append(item)
        elif category == "education":
            profile["education"].append(item)
        else:
            profile["other"].append(item)

    return profile

def normalize_conversations(conversations):
    normalized = []

    for conversation in conversations:

        if "messages" in conversation:
            normalized.append({
                "id": conversation.get("id"),
                "title": conversation.get("title", "Untitled"),
                "messages": conversation.get("messages", [])
            })
            continue

        if "mapping" in conversation:
            messages = []
            for node_id, node in conversation["mapping"].items():
                message = node.get("message")

                if not message:
                    continue

                author = message.get("author", {})
                role = author.get("role", "unknown")
                content = message.get("content", {})
                parts = content.get("parts", [])
                text_parts = []

            for part in parts:

                if isinstance(part, str):
                    text_parts.append(part)

            text = "\n".join(text_parts)

            if text.strip():

                messages.append({
                    "role": role,
                    "content": text
                })
            
            normalized.append({
                "id": conversation.get("conversation_id") or conversation.get("id"),
                "title": conversation.get("title", "Untitled"),
                "messages": messages
            })
    return normalized

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


def analyze_conversations(conversations):

    conversations = normalize_conversations(conversations)
    
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
                    "confidence": "high",
                    "classification": "explicit",
                    "severity": "high",
                    "status": "review",
                    "conversation_id": conversation.get("id"),
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
                    "confidence": "high",
                    "classification": "explicit",
                    "severity": "high",
                    "status": "review",
                    "conversation_id": conversation.get("id"),
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
                    "classification": "explicit",
                    "severity": "medium",
                    "status": "review",
                    "conversation_id": conversation.get("id"),
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
                    "classification": "explicit",
                    "severity": "high",
                    "status": "review",
                    "conversation_id": conversation.get("id"),
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
                    "classification": "explicit",
                    "severity": "medium",
                    "status": "review",
                    "conversation_id": conversation.get("id"),
                    "conversation": conversation.get("title", "Untitled"),
                    "role": message["role"],
                    "evidence": text 
                    }

                    if not finding_exists(findings, finding):
                        findings.append(finding)

    recurrence = build_recurrence(findings)
    summary = build_summary(findings)
    category_summary = build_category_summary(findings)
    profile = build_privacy_profile(findings, recurrence)
    inferences = build_infereces(findings, recurrence)

    return{
        "conversations":numofConvo,
        "messages":numofMessages,
        "summary": summary,
        "recurrence": recurrence,
        "findings": findings,
        "finding_count": len(findings),
        "profile": profile,
        "inferences": inferences
    }   