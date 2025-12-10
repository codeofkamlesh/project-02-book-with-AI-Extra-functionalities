---
id: 1
title: Update Constitution
stage: constitution
date: 2025-12-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["constitution","spec-driven","architectural-decision"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.contitution /sp.contitution

Project: AI-Native Hackathon Project — Full Spec-Driven System

Purpose:
Establish the governing principles, constraints, quality requirements, and success criteria for all phases
of the project including specification, modeling, implementation, documentation, and evaluation.

Core Principles:
- Primary-source accuracy: All claims and references must be validated directly from authoritative origins.
- AI-native workflow: All deliverables must follow SpecKit+, Context7 MCP architecture, and Docusaurus UI.
- Clarity & readability: Content must be written for general technical audiences (CS, AI, and software engineering background).
- Structural rigor: All modules must follow hierarchical spec structure (Module → Chapters → Subsections).
- Traceable reproducibility: Every claim, diagram, and design decision must be traceable to its corresponding spec or model.

Academic Writing Standards:
- Factual traceability: Every factual statement must have a source.
- Citation style: APA (7th edition)
- Source quality: At least 50% peer-reviewed journal articles
- Plagiarism policy: 0% tolerance; all content must be fully original or properly quoted
- Readability requirement: Flesch-Kincaid Grade 10–12

Document Constraints:
- Total content per major module: 5,000–7,000 words
- Minimum references per major module: 15 sources
- Output format: PDF with embedded citations + Markdown source for Docusaurus
- Visual content: All diagrams must be created through Draw.io, exported, and referenced in the UI

System Constraints:
- Frontend rendered using Docusaurus with collapsible sidebar for chapters
- Full Context7 MCP Server integration for specification → code → validation flow
- All modules must be organized using the structure:
  - Module 1: Constitution Phase
  - Module 2: Specification Phase
  - Module 3: Modeling Phase
  - Module 4: Implementation Phase
  - Module 5: Reflection & Evaluation Phase

Success Criteria:
- All project components comply with constitution rules
- All claims are source-v

## Response snapshot

I have successfully updated the constitution file at `.specify/memory/constitution.md` to match the requirements provided. The updated constitution now includes:

1. Core Principles section with Primary-source accuracy, AI-native workflow, Clarity & readability, Structural rigor, and Traceable reproducibility
2. Academic Writing Standards section with Factual traceability, Citation style, Source quality, Plagiarism policy, and Readability requirement
3. Document Constraints section with word count, reference, format, and visual content requirements
4. System Constraints section with Docusaurus rendering, Context7 MCP integration, and module organization
5. Success Criteria section with compliance, validation, deployment, and documentation requirements

The file was previously incomplete and has been fully updated to match the specification provided in the user request.

## Outcome

- ✅ Impact: Updated constitution file to match all specified requirements
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with complete constitution
- 🔁 Next prompts: User can proceed with other spec-driven development tasks
- 🧠 Reflection: Constitution serves as the foundational document for all future project work

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - Constitution file properly updated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin with specification phase based on updated constitution