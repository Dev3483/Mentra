import streamlit as st
import ollama

st.set_page_config(page_title="Mental Health Chatbot")

st.session_state.setdefault('conversation_history', [])


def generate_response(user_input):
    st.session_state['conversation_history'].append(
        {"role": "user", "content": user_input})

    response = ollama.chat(model="mistral",
                           messages=st.session_state['conversation_history'])
    ai_response = response['message']['content']

    st.session_state['conversation_history'].append(
        {"role": "assistant", "content": ai_response})
    return ai_response


def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed"
    response = ollama.chat(model="mistral", messages=[
                           {"role": "user", "content": prompt}])
    return response['message']['content']


def generate_meditation_guide():
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    response = ollama.chat(model="mistral", messages=[
                           {"role": "user", "content": prompt}])
    return response['message']['content']


st.title("Mental Health Support Agent")

if st.button("🆕 Start New Chat"):
    st.session_state.conversation_history = []
    st.session_state.user_input = ""
    st.query_params["dummy"] = str(st.session_state.user_input)  # Corrected
    st.rerun()  # Use st.rerun() instead of experimental_rerun()


for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

user_message = st.text_input("How can I help you today?")

if user_message:
    with st.spinner("Thinking....."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

col1, col2 = st.columns(2)

with col1:
    if st.button("Give me a positive Afiirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("Give me a guided meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")
