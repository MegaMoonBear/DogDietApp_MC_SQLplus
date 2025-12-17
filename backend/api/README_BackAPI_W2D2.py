# Backend API_(Module4Unit1W2D2)

# FastAPI backend for Dog Diet App - Example from Week 2's Day 2 (under Module 4, Unit 1)

 
import openai
import os
import getpass

# ✅ Securely input API key
api_key = getpass.getpass("Enter your OpenAI API key: ")

# ✅ Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)
#################### See notebook for key (ignore Slack, since instructors can add their own key) ########################################

# ✅ Initialize conversation history
conversation_history = [
    {"role": "Veterinary Communication Assistant", "content": "You are a Veterinary Communication Assistant. Your goal is to improve dog owners’ conversations with their veterinarian. You do not provide medical advice, product or drug recommendations, diagnoses, or treatment plans. Instead, you generate 3 simple, educational questions for the owner to ask their vet."}
]
# See end of 3rd section for more on role and content


####################Check doc/Word file for model="gpt-4o-mini" ################################################################################
# ✅ Define function to interact with ChatGPT API (Streaming Enabled)
    def chat_with_gpt(user_input, model="gpt-4o-mini", temperature=0.3, max_tokens=200, frequency_penalty=0.7, presence_penalty=0.25):
        """Sends user answers from 3, form questions to ChatGPT and receives an AI-generated response as 3 questions."""
#################### user_input as field - first reference to 3 user answers to form questions #################################################   

#################### Check doc/Word file for model="gpt-4o-mini" ################################################################################
        # Append user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})
#################### user_input as field - SECOND reference to 3 user answers #################################################################       

#################### user_input as field - User-answers lumped into "conversation_history" (THIRD reference to 3 user answers) ###################  
        # Make API request with advanced settings
        response = client.chat.completions.create(
            model=model,
            messages=conversation_history,
            temperature=temperature,  # Controls randomness
            max_tokens=max_tokens,    # Limits response length
            frequency_penalty=frequency_penalty,  # Reduces repetition
            presence_penalty=presence_penalty,    # Encourages topic diversity
            stream=True  # Enables streaming for real-time response
    )

    # ✅ Streaming Response Handling
        reply_text = ""
        print("\nChatGPT: ", end="", flush=True)
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
                reply_text += chunk.choices[0].delta.content

        print("\n")  # Newline for readability
        conversation_history.append({"role": "Veterinary Communication Assistant", "content": reply_text})  # Store AI response - See 2nd section


#################### NOT need indirect access to AI (through displayed questions AFTER "Submit" button for 3-question #####################
# ✅ Interactive Chat Loop
    # print("🤖 ChatGPT (Advanced) - Type 'exit' to quit")

    # while True:
    #     user_input = input("\nYou: ")
    #     if user_input.lower() == "exit":
    #         print("Session ended.")
    #         break
    #     chat_with_gpt(user_input)
#################### NOT need an "Exit" button, since "Submit" button for 3-question (NO direct access to AI) #############################