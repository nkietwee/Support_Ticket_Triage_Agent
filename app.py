import json
from pathlib import Path
from agent import SupportTriageAgent

DATA_PATH = (Path(__file__).parent / "data" / "sample_tickets.json")

def load_tickets():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    tickets = load_tickets()
    print("=" * 60)
    print("SUPPORT TICKET TRIAGE AGENT")
    print("=" * 60)

    for index, ticket in enumerate(tickets, start=1):
        latest_message = ticket["messages"][-1]["message"]

        if len(latest_message) > 70:
            latest_message = latest_message[:70] + "..."

        print(f"\n[{index}] {ticket['id']} - {ticket['title']}")
        print(f"    Customer : {ticket['customer_id']}")
        print(f"    Messages : {len(ticket['messages'])}")
        print(f'    Latest   : "{latest_message}"')

    print("\n[0] Exit")

    while True:
        choice_input = input("\nSelect ticket: ").strip()
        try:
            choice = int(choice_input)
        except ValueError:
            print("Please enter a number.")
            continue

        if choice == 0:
            print("Goodbye!")
            return

        if 1 <= choice <= len(tickets):
            ticket = tickets[choice - 1]
            break
        print(f"Please select a ticket between 1 and {len(tickets)}.")

    print("\nProcessing...\n")

    agent = SupportTriageAgent()
    result = agent.process(ticket)

    print("\n" + "=" * 60)
    print("TRIAGE RESULT")
    print("=" * 60)

    print(f"Urgency       : {result.urgency.upper()}")
    print(f"Product       : {result.product}")
    print(f"Issue Type    : {result.issue_type}")
    print(f"Sentiment     : {result.customer_sentiment}")
    print(f"Next Action   : {result.next_action}")
    print(f"Assigned Team : {result.assigned_team}")

    print("\nReason:")
    print(result.reason)

    print("\nRecommended Response:")
    print(result.recommended_response)

if __name__ == "__main__":
    main()