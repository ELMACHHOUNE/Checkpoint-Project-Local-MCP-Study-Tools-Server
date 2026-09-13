from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import BaseModel, Field
from typing import List, Optional
import json

mcp = FastMCP("StudyToolsServer")


class ExplainTopicInput(BaseModel):
    topic: str = Field(..., description="The topic to explain", min_length=1)


class StudyPlanInput(BaseModel):
    topic: str = Field(..., description="The topic for the study plan", min_length=1)
    days: int = Field(..., description="Number of study days (1-14)", ge=1, le=14)


class RevisionChecklistInput(BaseModel):
    topic: str = Field(..., description="The topic for the revision checklist", min_length=1)


class ToolError(BaseModel):
    error: str
    code: str
    details: Optional[str] = None


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
def explain_topic(topic: str) -> dict:
    """Explain a study topic in simple terms with examples."""
    if not topic or not topic.strip():
        return {
            "error": "Topic cannot be empty",
            "code": "EMPTY_TOPIC",
            "details": "Please provide a valid topic to explain"
        }
    
    topic = topic.strip()
    explanations = {
        "python": "Python is a high-level, interpreted programming language known for its readability and simplicity. It uses indentation to define code blocks and supports multiple programming paradigms.",
        "machine learning": "Machine Learning is a subset of AI that enables computers to learn from data without explicit programming. It involves algorithms that improve automatically through experience.",
        "mcp": "Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to LLMs. It allows AI assistants to connect to external data sources and tools.",
        "fastapi": "FastAPI is a modern, fast web framework for building APIs with Python. It uses type hints for automatic validation and documentation generation.",
        "git": "Git is a distributed version control system that tracks changes in source code. It enables collaboration, branching, and history management for software projects."
    }
    
    explanation = explanations.get(topic.lower(), f"Topic '{topic}' is not in the predefined explanations. Consider adding it to the knowledge base.")
    
    return {
        "topic": topic,
        "explanation": explanation,
        "related_topics": [k for k in explanations.keys() if k != topic.lower()][:3]
    }


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
def create_study_plan(topic: str, days: int) -> dict:
    """Create a structured study plan for a topic over a specified number of days (1-14)."""
    if not topic or not topic.strip():
        return {
            "error": "Topic cannot be empty",
            "code": "EMPTY_TOPIC",
            "details": "Please provide a valid topic for the study plan"
        }
    
    topic = topic.strip()
    clamped_days = max(1, min(14, days))
    
    if clamped_days != days:
        return {
            "error": f"Days value {days} was clamped to {clamped_days}",
            "code": "DAYS_CLAMPED",
            "details": f"Valid range is 1-14 days. Your input of {days} days has been adjusted to {clamped_days}.",
            "study_plan": _generate_plan(topic, clamped_days)
        }
    
    return {
        "topic": topic,
        "days": clamped_days,
        "study_plan": _generate_plan(topic, clamped_days)
    }


def _generate_plan(topic: str, days: int) -> List[dict]:
    plan = []
    for day in range(1, days + 1):
        plan.append({
            "day": day,
            "focus": f"Day {day}: {topic} fundamentals" if day <= 3 else f"Day {day}: Advanced {topic} concepts" if day <= days - 2 else f"Day {day}: {topic} practice & review",
            "estimated_hours": 2 if day <= 3 else 3,
            "activities": [
                f"Read {topic} documentation",
                f"Complete {topic} exercises",
                f"Build a small {topic} project"
            ][:min(day, 3)]
        })
    return plan


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
def generate_revision_checklist(topic: str) -> dict:
    """Generate a revision checklist for a study topic."""
    if not topic or not topic.strip():
        return {
            "error": "Topic cannot be empty",
            "code": "EMPTY_TOPIC",
            "details": "Please provide a valid topic for the revision checklist"
        }
    
    topic = topic.strip()
    
    checklist_items = [
        f"Understand core concepts of {topic}",
        f"Explain {topic} to someone else in simple terms",
        f"Solve 3 practice problems related to {topic}",
        f"Review common {topic} pitfalls and best practices",
        f"Create a mind map of {topic} connections",
        f"Complete a mini-project using {topic}",
        f"Teach {topic} basics to a peer"
    ]
    
    return {
        "topic": topic,
        "checklist": checklist_items,
        "total_items": len(checklist_items),
        "completion_status": {item: False for item in checklist_items}
    }


@mcp.resource("project://course-outline")
def course_outline() -> str:
    """Read-only resource: Course outline for study tools."""
    return json.dumps({
        "course": "MCP Study Tools",
        "version": "1.0",
        "modules": [
            {"id": 1, "title": "Introduction to MCP", "topics": ["What is MCP", "MCP Architecture", "Clients vs Servers"]},
            {"id": 2, "title": "Building MCP Servers", "topics": ["FastMCP", "Tools", "Resources", "Prompts"]},
            {"id": 3, "title": "MCP Security", "topics": ["Input Validation", "Resource Access Control", "Rate Limiting"]},
            {"id": 4, "title": "Testing MCP", "topics": ["Client Testing", "Agent Integration", "Error Handling"]}
        ],
        "total_modules": 4
    }, indent=2)


@mcp.resource("project://status")
def server_status() -> str:
    """Read-only resource: Server status information."""
    return json.dumps({
        "server": "StudyToolsServer",
        "status": "running",
        "tools_available": ["explain_topic", "create_study_plan", "generate_revision_checklist"],
        "resources_available": ["project://course-outline", "project://status"],
        "version": "1.0.0"
    }, indent=2)


if __name__ == "__main__":
    mcp.run()