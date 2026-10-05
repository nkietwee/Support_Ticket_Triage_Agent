import json
import os
from urllib import response

from dotenv import load_dotenv
from openai import OpenAI

from prompts import SYSTEM_PROMPT
from tools.customer_history import check_customer_history
from tools.knowledge_base import search_knowledge_base
from models import TriageResult

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

TOOLS = [
    {
        "type": "function",
        "name": "check_customer_history",
        "description": (
            "Retrieve customer account information and support history."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The unique customer ID."
                }
            },
            "required": ["customer_id"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "search_knowledge_base",
        "description": (
            "Search the support knowledge base for relevant FAQs "
            "and troubleshooting documentation."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Search query describing the customer's issue."
                    )
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
]

class SupportTriageAgent:

    def process(self, ticket: dict) -> TriageResult:

        input_messages = [
            {
                "role": "user",
                "content": (
                    "Analyze the following support ticket:\n\n"
                    + json.dumps(
                        ticket,
                        ensure_ascii=False
                    )
                )
            }
        ]

        while True:

            response = client.responses.create(
                model="gpt-5-mini",
                instructions=SYSTEM_PROMPT,
                input=input_messages,
                tools=TOOLS
            )

            input_messages += response.output

            tool_called = False

            for item in response.output:

                if item.type != "function_call":
                    continue

                tool_called = True
                arguments = json.loads(item.arguments)
                print(f"Tool called: {item.name}")
                tool_result = execute_tool(item.name, arguments)

                input_messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps(
                            tool_result,
                            ensure_ascii=False
                        )
                    }
                )

            if not tool_called:
                break

        # Final structured decision
        final_response = client.responses.parse(
            model="gpt-5-mini",
            instructions=(
                SYSTEM_PROMPT
                + "\nUsing all information gathered above, "
                  "make the final triage decision."
            ),
            input=input_messages,
            text_format=TriageResult
        )

        result = final_response.output_parsed

        if result is None:
            raise ValueError(
                "Model did not return a valid triage result."
            )

        return result
    
def execute_tool(tool_name: str, arguments: dict):

    if tool_name == "check_customer_history":
        return check_customer_history(customer_id=arguments["customer_id"])

    if tool_name == "search_knowledge_base":
        return search_knowledge_base(query=arguments["query"])

    raise ValueError(f"Unknown tool: {tool_name}")