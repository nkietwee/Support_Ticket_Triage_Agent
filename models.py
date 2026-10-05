from typing import Literal
from pydantic import BaseModel

class TriageResult(BaseModel):

    urgency: Literal[
        "critical",
        "high",
        "medium",
        "low"
    ]

    product: str
    issue_type: str
    customer_sentiment: str
    next_action: Literal[
        "auto_respond",
        "route_to_specialist",
        "escalate_to_human"
    ]
    assigned_team: str
    reason: str
    recommended_response: str