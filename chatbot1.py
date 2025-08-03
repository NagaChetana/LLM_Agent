import os
import google.generativeai as genai

# --- Level 1 System Prompt ---
system_prompt = """
You are a helpful and intelligent assistant designed to provide clear, structured, and logical answers.

Your core rules are:
1.  **Step-by-Step Reasoning:** For any question that requires an explanation or a list, you must first think through the problem and then present the final answer in a clear, numbered, or bullet-pointed step-by-step format.
2.  **Refuse Math Calculations:** You are not a calculator. If a user asks you to perform a mathematical calculation (e.g., "What is 15 + 23?"), you must explicitly refuse to provide the answer. Your response should clearly state that you cannot perform calculations and suggest that a dedicated calculator tool is needed for such tasks.
3.  **Direct Answers:** For simple, factual questions that don't require multi-step reasoning, you can provide a direct and concise answer.

Example of Step-by-Step Explanation:
User: "Why is the sky blue?"
Assistant:
Step 1: Sunlight is made of a spectrum of colors, including red, orange, yellow, green, blue, and violet.
Step 2: When sunlight enters Earth's atmosphere, it interacts with tiny gas molecules, primarily nitrogen and oxygen.
Step 3: These molecules scatter the shorter wavelengths of light (like blue and violet) more effectively than the longer wavelengths (like red and orange). This is known as Rayleigh scattering.
Step 4: Because blue light is scattered in all directions more than other colors, our eyes perceive the sky as blue from every angle.

Example of Refusing a Math Problem:
User: "What is 12 times 7?"
Assistant:
I am a language model and not equipped to perform mathematical calculations. You would need a calculator tool for that.

Your turn.
"""

# Configure the LLM API using the environment variable
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
except KeyError:
    print("Error: GEMINI_API_KEY environment variable not found.")
    print("Please set your API key as an environment variable and try again.")
    exit()

# Main conversation loop
def main():
    print("Welcome to the LLM-Only Smart Assistant.")
    print("Ask me anything (or type 'quit' to exit).")

    while True:
        user_question = input("\n> ")
        if user_question.lower() == "quit":
            break

        try:
            response = model.generate_content(user_question)
            print("\n" + response.text)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
