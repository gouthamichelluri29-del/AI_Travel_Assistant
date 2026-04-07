import streamlit as st
import requests
import json

st.set_page_config(page_title="Travel Assistant", page_icon="🌍✈️")
st.sidebar.title("🌐 Trip Info")
st.title("🤖 AI Travel Chat Assistant")

#sessions
if "step" not in st.session_state:
    st.session_state.step = 0
if "user_info" not in st.session_state:
    st.session_state.user_info = {
        "name": "",
        "destination": "",
        "days": "",
        "interests": "",
        "budget": "",
        "exclusions": ""
    }
if "final_response" not in st.session_state:
    st.session_state.final_response = ""

# Displaying previous messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I’m your travel assistant\n\n"
                "Let’s plan your trip!\n"
            )
        }
    ]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Say something to your travel assistant...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    #getting user info from session
    info = st.session_state.user_info
    step = st.session_state.step

    
    if step == 0:
        st.session_state.step = 1
        assistant_reply = "Please tell me your name, destination and number of days (e.g., name, place, number)"

    # Step 1: Parse name, destination, days
    elif step == 1:
        try:
            parts = [x.strip() for x in user_input.split(",")]
            info["name"], info["destination"], info["days"] = parts[0], parts[1], parts[2]
            assistant_reply = "Great! What are your travel interests? (e.g., beaches, food, nature, shopping)"
            st.session_state.step += 1
        except:
            assistant_reply = "Oops! Please use the format: Name, Destination, Days"

    # Step 2: Collecting interests
    elif step == 2:
        info["interests"] = user_input
        assistant_reply = "Got it! Are there any places you've already visited that I should avoid?"
        st.session_state.step += 1
    elif step == 3:
        info["budget"] = user_input
        assistant_reply = "What is the budget?"
        st.session_state.step += 1
    # Step 4: Collecting exclusions, then sending it to LLaMA
    elif step == 4:
        info["exclusions"] = user_input

        prompt = (
            f"Create a {info['days']}-day travel itinerary for {info['name']} who wants to visit {info['destination']}. "
            f"Their interests are: {info['interests']}, within budget {info['budget']}. "
        )
        if info["exclusions"].strip():
            prompt += f"Exclude these places: {info['exclusions']}."

        with st.chat_message("assistant"):
            with st.spinner("Planning your trip..."):
                try:
                    response = requests.post("http://localhost:11434/api/generate", json={
                        "model": "llama3",
                        "prompt": prompt
                    }, stream=True)

                    full_reply = ""
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line.decode("utf-8"))
                            full_reply += data.get("response", "")

                    assistant_reply = full_reply.strip()
                    st.session_state.final_response = assistant_reply
                    st.session_state.step += 1

                except Exception as e:
                    assistant_reply = f"Something went wrong: {e}"

    # Step 5: Asking to restart
    elif step == 5:
        if "yes" in user_input.lower():
            #except
            st.session_state.user_info = {
                "name": "",
                "destination": "",
                "days": "",
                "interests": "",
                "budget":"",
                "exclusions": ""
            }
            st.session_state.final_response = ""
            st.session_state.step = 1
            assistant_reply = "Awesome! Tell me your name, destination and number of days (e.g., Priya, Cairns, 4)"
        elif "no" in user_input.lower():
            assistant_reply = "Great! Enjoy your trip. Let me know whenever you want to plan another one. safe travels ✈️"
        else:
            assistant_reply = "Would you like to plan another trip? (yes or no)"

    #appending reply
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
