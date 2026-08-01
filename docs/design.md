# SmartLearn Agent — Product Design

## User Stories

1. As a student, I want to upload a PDF and ask questions about it, so that I can study more efficiently.
2. As a student, I want answers with page citations, so that I can quickly verify information in the original PDF.
3. As a student, I want to ask follow-up questions, so that I can deepen my understanding of a topic.

## Feature List

| Priority | Feature | Day |
|----------|---------|-----|
| P0 | PDF text extraction | Day 2 |
| P0 | LLM Q&A with page citations | Day 2 |
| P1 | RAG pipeline | Day 3 |
| P1 | Web UI | Day 3 |
| P2 | Chat history | Day 3 |

## What We Will NOT Build

- User authentication
- Multi-file support
- Mobile app

## Data Flow

### Day 2: Simple Mode

PDF File
  -> [extract text]
  -> pages[]
  -> [build prompt: pages + question]
  -> [LLM]
  -> Answer with [Page X]

### Day 3: RAG Mode

PDF
  -> [extract text]
  -> pages
  -> [split into chunks]
  -> chunks with source_page
  -> [embed]
  -> embeddings
  -> [vector store (FAISS)]

Question
  -> [encode]
  -> [similarity search]
  -> relevant chunks
  -> [LLM]
  -> Answer
