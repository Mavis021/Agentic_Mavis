from backend.core import run_llm
import streamlit as st


st.header("LangChain Documentation Helper")

prompt = st.text_input("prompt", placeholder="Enter your prompt here...")


if (
    "user_prompt_history" not in st.session_state
    and "chat_answers_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_answers_history"] = []
    st.session_state["chat_history"] = []

def create_source_links(source_urls: set[str]) -> str:
    if not source_urls:
        return "No Sources Found"
    
    source_links = list(source_urls)
    source_links.sort()
    source_string = "Sources:\n"

    for i, source in enumerate(source_links):
        source_string += f"{i+1}. {source}\n"
    
    return source_string


if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(query=prompt, chat_history=st.session_state["chat_history"])

        sources = set([docs.metadata["source"] for docs in generated_response["source_documents"]])

        formatted_response = (
            f"{generated_response['result']}\n\n {create_source_links(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("assistant", formatted_response))

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip( st.session_state["chat_answers_history"], st.session_state["user_prompt_history"]):
        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(generated_response)