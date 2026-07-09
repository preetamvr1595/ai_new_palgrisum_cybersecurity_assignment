import logging
from schemas.research import KnowledgeGraph, KnowledgeNode, KnowledgeEdge

logger = logging.getLogger(__name__)

def extract_knowledge_graph(text: str) -> KnowledgeGraph:
    """
    Simulates NLP/LLM extraction of Entities and Relationships to build a Knowledge Graph JSON.
    """
    logger.info("Extracting Knowledge Graph Nodes and Edges...")
    
    # Mocking a basic graph structure that the frontend can render
    nodes = [
        KnowledgeNode(id="n1", label="Artificial Intelligence", type="Concept"),
        KnowledgeNode(id="n2", label="Machine Learning", type="Concept"),
        KnowledgeNode(id="n3", label="Transformers", type="Technology")
    ]
    
    edges = [
        KnowledgeEdge(source="n1", target="n2", relationship="encompasses"),
        KnowledgeEdge(source="n2", target="n3", relationship="utilizes")
    ]
    
    return KnowledgeGraph(nodes=nodes, edges=edges)
