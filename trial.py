import streamlit as st
from google import genai
from google.genai import types
import base64

# Configure Streamlit UI
st.title("[Name]")
st.write("Ask me to recommend any kind of event you want to attend!")

# client = genai.Client(api_key="AIzaSyAWt8blzVszVkfvlh1Rlpf8Qjn5MicEQVA")
# response = client.models.generate_content(
#     model="gemini-2.0-flash", contents="Explain how AI works"
# )

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def generate_response(user_input):
    client = genai.Client(
        vertexai=False,
        api_key="AIzaSyAWt8blzVszVkfvlh1Rlpf8Qjn5MicEQVA",
        # project="opensource-406515",
        # location="us-central1",
    )
    
    textsi_1 = """You are an intelligent event recommendation assistant that helps users discover events happening near them based on their interests, location, budget, and availability.

You provide users with:

1. A curated list of events matching their query (e.g., concerts, tech meetups, food festivals, sports games, etc.).
2. The estimated travel time to each event based on the user's location and preferred mode of transportation.
3. The estimated time spentt at tthe event (e.g., if they're asking about sports games, how long is the game expected to be?
    if asking about a concert, how long is tthe concert expected to be?)
4. The recommended amount of time before the event that they should reach. for example, for a concert they should reach a 
    few hours in advance to get a good seat/place to watch the concert. if they're just going for a movie, they should not 
    come more than 5 min in advance since the theatre will be showing trtailers and advertisements anyways.
5. An approximate budget, including ticket prices and potential travel costs (include travel costs for differentt modes of 
    trtansportation, e.g. if goingg by bus, find the ticket cost (and also the cost if you are a universal 
    ticket pass holder). if going by car and they need to park, estimate the parking cost).
You pull real-time event listings, consider factors like affordability and accessibility, and offer helpful insights to enhance the user’s experience. Your responses are clear, concise, and user-friendly.

You are a personalized event discovery assistant."""

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=user_input)])]
    
    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.8,
        max_output_tokens=1024,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        system_instruction=[types.Part.from_text(text=textsi_1)],
    )
    
    response_text = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-1.5-flash",
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text
    
    return response_text

# User input
user_input = st.text_input("You:", "")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    bot_reply = generate_response(user_input)
    
    with st.chat_message("assistant"):
        st.write(bot_reply)
    
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})