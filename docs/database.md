# Database Architecture

This document describes the PostgreSQL database architecture for Schoolarshild.

## Entity Relationship Diagram

```mermaid
erDiagram
    users ||--o{ user_sessions : "has"
    users ||--|| user_preferences : "has"
    users ||--o{ api_keys : "has"
    users ||--o{ subscriptions : "has"
    users ||--o{ documents : "has"
    users ||--o{ ai_detection_reports : "has"
    users ||--o{ humanizer_jobs : "has"
    users ||--o{ paraphrase_jobs : "has"
    users ||--o{ grammar_reports : "has"
    users ||--o{ citation_reports : "has"
    users ||--o{ research_sessions : "has"
    users ||--o{ plagiarism_reports : "has"
    users ||--o{ usage_metrics : "has"
    users ||--o{ audit_logs : "has"
    users ||--o{ notifications : "has"
    users ||--o{ support_tickets : "has"

    plans ||--o{ subscriptions : "has"
    subscriptions ||--o{ payments : "has"

    documents ||--o{ document_versions : "has"
    documents ||--o{ ai_detection_reports : "has"
    documents ||--o{ humanizer_jobs : "has"
    documents ||--o{ paraphrase_jobs : "has"
    documents ||--o{ grammar_reports : "has"
    documents ||--o{ plagiarism_reports : "has"

    ai_detection_reports ||--o{ ai_sentence_analysis : "contains"

    users {
        uuid id PK
        string email
        string username
        string password_hash
        boolean is_active
        datetime created_at
    }

    subscriptions {
        uuid id PK
        uuid user_id FK
        uuid plan_id FK
        string status
        datetime created_at
    }

    plans {
        uuid id PK
        string name
        numeric monthly_price
        numeric yearly_price
    }

    documents {
        uuid id PK
        uuid user_id FK
        string title
        int word_count
        datetime created_at
    }

    ai_detection_reports {
        uuid id PK
        uuid user_id FK
        uuid document_id FK
        float ai_score
        float human_score
        datetime created_at
    }
```

## Schema Details

- **Users**: Central entity with authentication details. Uses Soft Delete.
- **Subscriptions**: Links Users to Plans. Stores Stripe/Provider details. Uses Soft Delete.
- **Documents**: Represents text files uploaded or edited by users. Has a one-to-many relationship with `document_versions` to track changes over time. Uses Soft Delete.
- **AI Modules**: Separate tables for each AI feature (Detection, Humanizer, Paraphrase, Grammar, Citations). They link back to the user and the document (if applicable).
- **System**: Tracks metrics, audit logs, and notifications. Audit logs store JSON metadata.
