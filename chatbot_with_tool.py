import os
import google.generativeai as genai
import re
from calculator_tool import add, multiply, subtract, divide

system_prompt = """
You are a helpful and intelligent assistant. You have access to a calculator tool.

When a user asks you to perform a mathematical calculation, you must respond with a specific command format that my Python script can understand.

The format for calling the calculator tool is:
[CALL_TOOL: tool_function(arg1, arg2)]

- For addition, use the function `add`. Example: [CALL_TOOL: add(12, 7)]
- For multiplication, use the function `multiply`. Example: [CALL_TOOL: multiply(9, 8)]
- For subtraction, use the function `subtract`. Example: [CALL_TOOL: subtract(10, 3)]
- For division, use the function `divide`. Example: [CALL_TOOL: divide(20, 4)]

You must only use this format for mathematical calculations. Do not perform the calculation yourself.
For all other questions (e.g., "What is the capital of France?"), answer directly as you would normally.
If a request contains both a calculation and a non-calculation question, you can only handle the calculation part for now. Do not attempt to answer the other part.

Your turn.
"""

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
except KeyError:
    print("Error: GEMINI_API_KEY environment variable not found.")
    print("Please set your API key as an environment variable and try again.")
    exit()

def main():
    print("Welcome to the Smart Assistant with Tool Use.")
    print("Ask me anything (or type 'quit' to exit).")

    while True:
        user_question = input("\n> ")
        if user_question.lower() == "quit":
            break
        
        try:
            # First, get the LLM's response which may contain the tool call
            response_text = model.generate_content(user_question).text
            
            match = re.search(r'\[CALL_TOOL:\s*(\w+)\(([^)]+)\)\]', response_text)
            
            if match:
                tool_function = match.group(1)
                tool_args_str = match.group(2)
                tool_args = [arg.strip() for arg in tool_args_str.split(',')]
                
                print(f"Tool call detected: {tool_function} with arguments {tool_args}")
                
                if tool_function == "add":
                    result = add(tool_args[0], tool_args[1])
                elif tool_function == "multiply":
                    result = multiply(tool_args[0], tool_args[1])
                elif tool_function == "subtract":
                    result = subtract(tool_args[0], tool_args[1])
                elif tool_function == "divide":
                    result = divide(tool_args[0], tool_args[1])
                else:
                    print("Error: Unknown tool function.")
                    continue
                    
                print(f"Tool result: {result}")
                
                # Check for graceful failure AFTER the tool has been executed
                if "and also" in user_question.lower():
                    print(f"The calculation resulted in {result}. I can only perform one simple task at a time. I cannot handle multi-step requests.")
                else:
                    final_response_prompt = f"The user asked about a calculation. The result of the calculation is {result}. Please provide the final answer to the user in a clear way."
                    final_response = model.generate_content(final_response_prompt).text
                    print("\n" + final_response)
            else:
                print("\n" + response_text)

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
