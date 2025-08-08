from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from pathlib import Path
import streamlit as st
import pyperclipfix


def initialize_llm(model: str = "llama3.2:3b", temperature: float = 0.0) -> ChatOllama:
    """Initialize the Ollama language model.

    Args:
        model: The model name to use.
        temperature: Controls randomness of output (0 = deterministic).

    Returns:
        Initialized ChatOllama instance.
    """
    return ChatOllama(
        model=model,
        temperature=temperature,
    )


def generate_tldr(LLM_MODEL: str, job_ad_text: str, BOT_INSTRUCTIONS: str) -> str:
    """Generate a TLDR version of a job advertisement.

    Args:
        llm: Initialized language model.
        job_ad_text: The full job advertisement text.

    Returns:
        The summarized version of the job ad.
    """

    llm = initialize_llm(model=LLM_MODEL)

    messages = [
        SystemMessage(content=BOT_INSTRUCTIONS),
        HumanMessage(content=job_ad_text),
    ]

    response: BaseMessage = llm.invoke(messages)
    if not isinstance(response, AIMessage):
        raise ValueError("Unexpected response type from LLM")
    content = response.content
    match content:
        case str(content):
            return content
        case _:
            return "failed"


def load_file(file_path: str) -> str:
    """
    Load the content of a file as a string.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file.
    """

    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' does not exist.")
        exit(1)

    content = path.read_text(encoding="utf-8")
    words = content.split()
    if len(words) < 10:
        print("Error: The file contains less than 10 words.")
        exit(1)

    return content


def generate_professional_profile(
    LLM_MODEL: str, job_ad_text: str, CV: str, BOT_INSTRUCTIONS: str
) -> str:
    """Generate a professional profile paragraph for cv.

    Args:
        TODO

    Returns:
        The summarized version of the professional profile.
    """

    cv = f"""
        ***THIS IS THE END OF THE JOB AD***

        When writing the professional profile paragraph don't lie about the skills that i don't have. Here is the information about me, my skills and work experience: 
        {load_file(CV)}
    """

    llm = initialize_llm(model=LLM_MODEL)

    combined_text = f"""
        {job_ad_text}
        {cv}
    """

    messages = [
        SystemMessage(content=BOT_INSTRUCTIONS),
        HumanMessage(content=combined_text),
    ]

    response: BaseMessage = llm.invoke(messages)
    if not isinstance(response, AIMessage):
        raise ValueError("Unexpected response type from LLM")
    content = response.content
    match content:
        case str(content):
            return content
        case _:
            return "failed"


def main(
    LLM_MODEL: str, CV: str, TLDR_BOT_INSTRUCTIONS: str, PROFILE_BOT_INSTRUCTIONS: str
) -> None:
    try:

        st.set_page_config(
            page_title="LLM Job tools",
            layout="wide",
            initial_sidebar_state="auto",
        )

        # Initialize session state for prompt
        if "prompt" not in st.session_state:
            st.session_state.prompt = ""

        # Split view into two columns (User input and LLM output)
        col1, col2 = st.columns(2)

        with col1:
            _ = st.subheader("Your Input")
            prompt = st.text_area(
                "Paste the job advertisement here:",
                height=500,
                value=st.session_state.prompt,
                key="text_area",
            )

            spacer, button_col1, button_col2, button_col3 = st.columns([9, 4, 3, 3])

            with spacer:
                pass  # Empty space to push buttons right

            with button_col1:
                if st.button("Gen Profile", use_container_width=True):
                    if st.session_state.prompt == "":
                        pass
                    else:
                        if prompt:
                            full_response = generate_professional_profile(
                                LLM_MODEL, prompt, CV, PROFILE_BOT_INSTRUCTIONS
                            )
                            # st.session_state.response = full_response + + "\n\n---\n\n" + st.session_state.response
                            st.session_state.response = f"{full_response}\n\n### Previous Responses\n\n{st.session_state.response}"
                            st.rerun()

            with button_col2:
                if st.button("Paste", use_container_width=True):
                    try:
                        clipboard_content = pyperclipfix.paste()
                        st.session_state.prompt = clipboard_content
                        if st.session_state.prompt:
                            full_response = generate_tldr(
                                LLM_MODEL,
                                st.session_state.prompt,
                                TLDR_BOT_INSTRUCTIONS,
                            )
                            st.session_state.response = full_response
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to paste from clipboard: {str(e)}")

            with button_col3:
                if st.button("Send", use_container_width=True):
                    if prompt:
                        full_response = generate_tldr(
                            LLM_MODEL, prompt, TLDR_BOT_INSTRUCTIONS
                        )
                        st.session_state.response = full_response
                        st.rerun()

        with col2:
            _ = st.subheader("Assistant Response")

            if "response" in st.session_state:
                _ = st.markdown(st.session_state.response)

    except Exception as e:
        _ = st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    TLDR_BOT_INSTRUCTIONS = """
    You are a TLDR Bot, designed to condense lengthy job advertisements. 
    Output these sections from the job ad as a list: 
    - Languages and tools required, 
    - required skills, 
    - brief summary about the job.
    """

    PROFILE_BOT_INSTRUCTIONS = """
    You need to assist in writing professional profile paragraphs for a resume (CV), the text should be written in third person. The professional profile paragraph that you will write, should be: concise, about 50 words long, inteded to highlight key skills, experiences, interests in learning and abilities relevant to the job application. Don't use the term 'proven track record'. Output just the professional profile paragraph without double quotes.
    """

    # """
    # You need to assist in writing professional profile paragraphs for resume (CV). The professional profile paragraph that you will write, should be relevant for the position: concise, about 50 words long, inteded to highlight skills, experiences, interests in learning what the person is lacking. Don't use the term 'proven track record'. Output just the professional profile paragraph without double quotes.
    # """

    CV = "src/INPUT.txt"
    LLM_MODEL = "llama3.2:3b"

    main(LLM_MODEL, CV, TLDR_BOT_INSTRUCTIONS, PROFILE_BOT_INSTRUCTIONS)
