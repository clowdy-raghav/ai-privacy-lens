# Architecture

AI Privacy Lens follows a local-first architecture.

## Pipeline

Conversation Export
↓
Import Layer
↓
Normalization
↓
Privacy Detection
↓
Cross-Conversation Analysis
↓
Privacy Profile
↓
Evidence
↓
User Control

## Detection

Structured identifiers can be detected using pattern-based
methods.

Entities such as names, locations and organizations can be
handeled through NLP/NER and contextual analysis in a 
production implementation.

## Privacy

Raw conversation data remains within the local application
during the MVP workflow.

the systen is designed to minimize unnecessary external
data transmission.
