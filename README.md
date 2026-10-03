# AI Privacy Lens

> Discover → Explain → Control your AI privacy footpro=int.

AI Privacy Lens is a local-first privacy analysis tool
designed to help users understand the cumulative personal
information exposed across their AI conversations.

## Problem 

Users increasingly share personal information with AI
assistants across many separate conversations.

A single conversation may appear harmless, but information
distributed acroess multiple conversations can collectively
reveal a much richer personal profile.

## Solution

AI Privacy Lens allows users to import their AI conversation
history and analyze it locally.

The system identifies:

- Explicitly disclosed information
- Recurring information
- Cross-conversation relationships
- Potential privacy-relevant inferences

Users can then review individual findings and mark them as:

- Keep
- Review
- Delete

## Architecture

Browser
↓
Flask
↓
Conversation normalization
↓
Privacy analysis
↓
Privacy profile
↓
Evidence and User controls

## Privacy by Design

Raw conversation data is processed locally in the MVP.

The application does not require a cloud database to store
conversational history.

Potential inferences are explicitly labelled as potential
rather than established facts.

## Current MVP

The prototype currently supports:

- JSON conversation import
- Conversation normalization
- Email detection
- Phone detection
- Name detection
- Location detection
- Institute detection
- Cross-conversation recurrence
- Privacy categories
- Potential inference demonstration
- Evidence display
- Local finding controls

## Limitations

The current prototype uses simpplified detection methods.

Production deployment would require:
- Robust NLP/NER
- Context-aware entity classification
- Support for multiple AI export formats
- Stronger inference validation
- Provider-specific deletion workflows

## Future Worl

- More AI providers
- Local privacy-preserving language models
- Advanced contextual inference
- Provider-specific deletion integrations
- Privacy risk visualization