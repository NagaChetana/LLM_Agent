# README — How to Run the AI Chatbot Assignment

This is a Python project where you're building an AI chatbot that gets smarter step by step. The project has 3 levels:

---

### LEVEL 1 — Basic AI Chatbot

* You build a chatbot that takes your question and sends it to an LLM (like Gemini or OpenAI).
* The chatbot should:

  * Answer with clear, step-by-step explanations.
  * Refuse to solve math problems directly — instead, suggest using a calculator tool.

**Examples to try:**

* "What are the colors in a rainbow?"
* "Tell me why the sky is blue?"
* "What is 15 + 23?" → It should not solve this, just say use a calculator.

Run this using the file: `chatbot.py`

---

### LEVEL 2 — AI Chatbot with Calculator Tool

* The chatbot now becomes smarter!
* If you ask a math question, it doesn’t try to solve it — it uses a calculator tool to do it for you.

**Examples to try:**

* "What is 12 times 7?"
* "Add 45 and 30"
* "Multiply 9 and 8 and also tell me the capital of Japan" → It should try, but will fail gracefully since multi-step isn’t ready yet.

Run this using the file: `chatbot_with_tool.py`

---

### LEVEL 3 — Fully Smart AI Agent

* This is the most advanced level.
* It breaks your questions into steps, uses multiple tools (calculator + translator), and answers everything properly.
* It remembers what it's doing and handles complex queries.

**Examples to try:**

* "Translate 'Good Morning' into German and then multiply 5 and 6"
* "Add 10 and 20, then translate 'Have a nice day' into German"
* "Tell me the capital of Italy, then multiply 12 and 12"

Run this using the file: `full_agent.py`

---

### How to Set Up Everything

1. **Create a virtual environment** (optional but recommended):

   * Open PowerShell or terminal and run:

     ```
     python -m venv env
     ```

2. **Activate the virtual environment**:

   * On Windows:

     ```
     env\Scripts\activate
     ```
   * On Mac or Linux:

     ```
     source env/bin/activate
     ```

3. **Set your Gemini API key**:

   * On Windows PowerShell:

     ```
     setx GEMINI_API_KEY "your_api_key_here"
     ```
   * On Linux/macOS:

     ```
     export GEMINI_API_KEY="your_api_key_here"
     ```

4. **Install required packages**:

   ```
   pip install -r requirements.txt
   ```

5. **Run the chatbot**:

   * For Level 1: `python chatbot.py`
   * For Level 2: `python chatbot_with_tool.py`
   * For Level 3: `python full_agent.py`

---

### What's Included

* `chatbot.py` → Basic LLM chatbot
* `chatbot_with_tool.py` → Chatbot with calculator
* `full_agent.py` → Fully smart agent with tools and multi-step thinking
* `calculator_tool.py` → Does math
* `translator_tool.py` → Translates English to German
* `logs/` folder → Example chatbot conversations
* `README.md` → This guide

