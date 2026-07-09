from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum

class ResearchMode(str, Enum):
    EXPLORE = "explore"
    LIT_REVIEW = "literature_review"
    DOC_ANALYSIS = "document_analysis"

class KnowledgeNode(BaseModel):
    id: str
    label: str
    type: str # e.g., "Concept", "Entity", "Author"

class KnowledgeEdge(BaseModel):
    source: str # Node ID
    target: str # Node ID
    relationship: str

class KnowledgeGraph(BaseModel):
    nodes: List[KnowledgeNode]
    edges: List[KnowledgeEdge]

class DiscoveredSource(BaseModel):
    title: str
    authors: List[str]
    url: Optional[str]
    snippet: str

class ResearchReport(BaseModel):
    report_id: str
    title: str
    executive_summary: str
    detailed_findings: List[str]
    key_insights: List[str]
    discovered_sources: List[DiscoveredSource]
    knowledge_graph: Optional[KnowledgeGraph] = None
    generation_time_ms: int

class ResearchQueryRequest(BaseModel):
    query: str
    mode: ResearchMode = ResearchMode.EXPLORE
    document_ids: Optional[List[str]] = None
