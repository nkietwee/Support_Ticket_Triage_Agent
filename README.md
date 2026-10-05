## Setup and Run

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```
### 2. Clone the repository
For Windows:
```
python -m venv .venv
.venv\Scripts\activate
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Configure the OpenAI API key
This project does not include an API key in the repository.
Copy the provided .env.example file:
```
cp .env.example .env
```
Then open .env and replace the placeholder with your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```
### 5. Run the application
```
python app.py
```
The application will display the available sample tickets:
```
============================================================
SUPPORT TICKET TRIAGE AGENT
============================================================

[1] ticket_001 - Multiple pending charges
[2] ticket_002 - Enterprise users unable to access system
[3] ticket_003 - Dark mode not working

Select ticket:
```
Enter a ticket number to run the triage agent.
Example:
```
Select ticket: 1

Processing...

Tool called: check_customer_history
Tool called: search_knowledge_base
```