import streamlit as st
import requests

# Page title
st.title("🧠 Chat with Alpha AI")

# Session state to store messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🎯I already have an idea and I want help turning it into a WorldQuant-worthy alpha.  \n\n🧭I’m looking for a fresh idea — can Alpha AI suggest one and help me build the corresponding alpha?"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Say something..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Send message to backend
    try:
        res = requests.post("http://localhost:8000/api/chat/", json={"message": prompt , "memory":st.session_state.messages})
        ai_response = res.json().get("response", "Sorry, something went wrong.")
    except Exception as e:
        ai_response = f"Error: {e}"

    # Add AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    st.chat_message("assistant").markdown(ai_response)


st.sidebar.markdown(
    """
    <div style='font-size:20px;'>
        <strong style='color:#ffbd45; font-size:23px; font-weight:bold; font-family:Arial;'>Welcome to Alpha AI</strong><br>
        Step into Alpha AI — your gateway to transforming bold ideas into cutting-edge alphas using <b>CrewAI</b>'s powerful multi-agent workflow, you can confidently submit to <b style='color:#ff6c6c;'>WorldQuant</b>.
    </div>
    """,
    unsafe_allow_html=True
)




# # Function to extract "alpha expression" from a string
# def extract_alpha_expression(text):
#     # Define your alpha expression pattern (you can customize this!)
#     # Example: alpha expressions are marked like [alpha: some expression]
#     match = re.search(r"\[alpha: (.+?)\]", text, re.IGNORECASE)
#     if match:
#         return match.group(1)
#     return None

# # Handle Get Alpha button
# if st.sidebar.button("🔍 Get Alpha"):
#     messages = st.session_state.messages
#     bot_messages = [msg for msg in messages if msg["role"] == "assistant"]

#     if bot_messages:
#         last_response = bot_messages[-1]["content"]
#         alpha = extract_alpha_expression(last_response)

#         if alpha:
#             alpha_message = f"✅ Extracted Alpha: `{alpha}`"
#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": alpha_message
#             })
            
#             with st.chat_message("assistant"):
#                 st.markdown(alpha_message)
#                 # Add a copy-to-clipboard button
#                 st.code(alpha, language='plaintext')
#         else:
#             error_msg = "⚠️ Unable to Extract alpha"
#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": error_msg
#             })
#             st.chat_message("assistant").markdown(error_msg)
#     else:
#         st.sidebar.warning("No previous AI response found.")