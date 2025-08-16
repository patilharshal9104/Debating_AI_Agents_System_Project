# AI Agents based Debate System

The AI Debate System is a Python-based project that uses **multiple AI models** to debate with each other before giving you a final answer.  
Instead of relying on one AI’s opinion, it makes them **argue, fact-check, and refine their responses** to produce the most **accurate and well-supported answer possible**.

---

## Overview

When you ask an AI a question — whether it’s _“Which tech stack should I use?”_, _“How do I fix this code?”_, or _“Which political party is better?”_ — the answer might not always be accurate.  
A single AI model can miss details, make mistakes, or give biased opinions.

This project sends your question to **multiple LLMs**.  
Agents then:

1. Receive each LLM’s suggestions.
2. Debate and challenge each other’s reasoning.
3. Use fact-checking and evidence retrieval (RAG) to refine results.
4. Produce the **most accurate and validated answer possible**.

It can be used for:

- **Coding help** – e.g., “Find the bug in my MERN stack code and suggest the best fix.”
- **Technology comparisons** – e.g., “React vs Vue: Which is better for my project?”
- **General debates** – e.g., “BJP vs Congress: Which has better economic policies?”

---

## How It Works

The workflow is designed to simulate a **structured courtroom debate** between AI agents.

1. **User Input**

   - You enter a question in the command line.
   - Example: `"How to fix a MERN stack CORS error?"`

2. **Initial Suggestions**

   - The system sends the query to multiple LLMs (e.g., Gemini, DeepSeek).
   - Each LLM returns its own **proposed answer**.

3. **Debate Round**

   - Agents take the role of **lawyers**:
     - **Prosecution Agent** defends one answer.
     - **Defense Agent** challenges it, pointing out flaws or alternative solutions.
   - They exchange counterarguments over multiple rounds.

4. **Evidence Retrieval (RAG)**

   - When an agent makes a claim, the system uses a **Retrieval-Augmented Generation** pipeline to:
     - Search for relevant documents or articles from trusted sources.
     - Verify if the claim is factually correct.
     - Discard unsupported claims.

5. **Refinement Stage**

   - Agents revise their arguments based on verified evidence.
   - Any contradictions or weak reasoning are removed.

6. **Final Answer Generation**
   - A **Judge Agent** evaluates the refined arguments.
   - The best-supported, fact-checked conclusion is returned to you.
   - A Markdown transcript (`debate_transcript.md`) is saved showing the full debate.

---

## Features

- **Multi-LLM Debating** – Two or more AI models discuss, critique, and refine each other’s answers.
- **Lawyer-Style Argumentation** – Agents defend and challenge points logically.
- **Evidence-Based Reasoning** – Uses RAG to pull verified facts from trusted sources.
- **Multi-Domain Support** – Works for coding, tech advice, politics, and general topics.
- **Readable Output** – Console results + saved Markdown transcript of the debate.

---

## Technologies Used

- [LangChain](https://www.langchain.com/) – Agent orchestration
- [Transformers](https://huggingface.co/transformers/) – LLM integration
- Retrieval-Augmented Generation (RAG) – Fact-based evidence retrieval
- Python 3.9+
- Git

---

## file structure

main.py # Entry point
debate_engine.py # Debate orchestration logic
llm_calls.py # API calls to Gemini & DeepSeek
output_formatter.py # Transcript formatting
utils.py # Helper functions
evidence_retriever.py # Data gathering
debate_agent.py # Agent definitions
web_loader.py # Reference validation
config.py # API endpoints & constants
requirements.txt # Dependencies
.env # API keys (ignored by Git)

---

## how to run 
- add gemini api and deepseek api in .env file and just run the main.py file

---

## contact

- hspatil000@gmail.com


