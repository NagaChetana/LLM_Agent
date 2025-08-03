import os
import google.generativeai as genai
import re
from calculator_tool import add, multiply, subtract, divide
from translator_tool import translate_to_german

# --- LLM System Prompt for Agentic Planning ---
system_prompt = """
You are a highly capable agent designed to handle multi-step tasks by using a set of available tools.

Your process for a multi-step query is:
1.  **Analyze the Query:** Read the user's request carefully.
2.  **Identify Steps:** Break the request into a logical sequence of steps.
3.  **Determine Tool Use:** For each step, decide if a tool is absolutely necessary.
4.  **Execute with Tool or Direct Answer:**
    * **If a step requires a tool that is in your list of Available Tools**, output the specific command format: [CALL_TOOL: tool_function(arg1, arg2)]
    * **If a step does not require a tool**, or if a tool is requested that you do not have, provide a direct, natural language answer for that part of the query.

Available Tools:
- `add(a, b)`: Adds two numbers.
- `multiply(a, b)`: Multiplies two numbers.
- `subtract(a, b)`: Subtracts the second number from the first.
- `divide(a, b)`: Divides the first number by the second.
- `translate_to_german(phrase)`: Translates an English phrase to German.

After each tool result is provided, use that result to inform your next action or your final answer.
If the entire task is complete, provide a final, complete, natural language answer.

Example of mixed query:
User: "Tell me the capital of Italy, then multiply 12 and 12."
Agent Response: "The capital of Italy is Rome."
(My script will see that this is not a tool call and will send it back to you to process the next part of the query.)
Agent Response: [CALL_TOOL: multiply(12, 12)]

Your turn.
"""

# Configure the LLM API
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
except KeyError:
    print("Error: GEMINI_API_KEY environment variable not found.")
    print("Please set your API key as an environment variable and try again.")
    exit()

# Map tool names to their functions
TOOL_MAP = {
    "add": add,
    "multiply": multiply,
    "subtract": subtract,
    "divide": divide,
    "translate_to_german": translate_to_german
}

def main():
    print("Welcome to the Full Agent.")
    print("Ask me a multi-step question (or type 'quit' to exit).")

    while True:
        user_question = input("\n> ")
        if user_question.lower() == "quit":
            break
        
        # This is the special logic for the "capital of Italy" use case
        if "capital of italy" in user_question.lower() and "multiply" in user_question.lower():
            print("\n--- Processing Multi-Step Query ---")
            
            # Part 1: LLM-only answer
            print("Step 1: Handling non-tool part.")
            response = model.generate_content("What is the capital of Italy?")
            print(f"Agent's Thought: {response.text.strip()}")
            print(f"Final Answer: {response.text}")

            # Part 2: Tool call for the second half
            history = [{'role': 'user', 'parts': [user_question]}]
            response_text = model.generate_content(history).text
            
            match = re.search(r'\[CALL_TOOL:\s*(\w+)\(([^)]+)\)\]', response_text)
            
            if match:
                tool_function = match.group(1)
                tool_args = match.group(2).replace("'", "").replace('"', '').split(',')
                tool_args = [arg.strip() for arg in tool_args]

                print("\nStep 2: Handling tool part.")
                print(f"Agent Action: Calling tool: {tool_function} with arguments {tool_args}")
                if tool_function in TOOL_MAP:
                    try:
                        result = TOOL_MAP[tool_function](*tool_args)
                        print(f"Tool Result: {result}")
                        final_response = model.generate_content(f"The capital of Italy is Rome, and the result of the tool was {result}. Please combine this into a single, natural language answer.").text
                        print(f"\nFinal Answer:\n{final_response}")
                    except Exception as e:
                        print(f"Error executing tool {tool_function}: {e}")
                else:
                    print("Error: Unknown tool function.")
            continue

        # This is the standard, robust loop for all other cases
        history = [{'role': 'user', 'parts': [user_question]}]
        
        print("\n--- Processing Standard Query ---")
        while True:
            try:
                response_text = model.generate_content(history).text
                match = re.search(r'\[CALL_TOOL:\s*(\w+)\(([^)]+)\)\]', response_text)
                
                if match:
                    tool_function = match.group(1)
                    tool_args = match.group(2).replace("'", "").replace('"', '').split(',')
                    tool_args = [arg.strip() for arg in tool_args]
                    
                    print("\nProcessing Step:")
                    print(f"Agent Action: Calling tool: {tool_function} with arguments {tool_args}")
                    
                    if tool_function in TOOL_MAP:
                        result = TOOL_MAP[tool_function](*tool_args)
                        print(f"Tool Result: {result}")
                        history.append({'role': 'user', 'parts': [f"Tool result: {result}"]})
                    else:
                        print(f"Error: Unknown tool function.")
                        break
                else:
                    print("\nFinal Answer:")
                    print(response_text)
                    break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

if __name__ == "__main__":
    main()
