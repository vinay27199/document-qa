import streamlit as st
from openai import OpenAI


# Show title and description.
st.title("MY Document Question Answering")
st.write(
    "Upload a document below and ask for a summary – GPT will summarize! "
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.secrets["openai_api_key"]

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    try:
        # Create an OpenAI client and validate the API key.
        client = OpenAI(api_key=openai_api_key)
        # Make a simple API call to validate the key.
        client.models.list()
        st.success("API key is valid!", icon="✅")

        # Let the user upload a file via `st.file_uploader`.
        uploaded_file = st.file_uploader(
            "Upload a document (.txt or .md)", type=("txt", "md")
        )

        st.sidebar.title("Summary Options")
        summary_option = st.sidebar.radio(
            "Choose a summary format:",
            (
                "Summarize the document in 100 words",
                "Summarize the document in 2 connecting paragraphs",
                "Summarize the document in 5 bullet points",
            ),
            index=0
        )
        # Checkbox to select between basic and advanced model
        use_advanced_model = st.sidebar.checkbox("Use Advanced Model (gpt-4o)")

        # Model selection based on checkbox
        model_choice = "gpt-4o" if use_advanced_model else "gpt-4o-mini"

        if uploaded_file and summary_option:
            # Process the uploaded file and question.
            if 'document' not in st.session_state:
                st.session_state['document']=uploaded_file.read().decode()
            

            # Define the system instruction based on the selected summary option.
            if summary_option == "Summarize the document in 100 words":
                summary_instruction = "Summarize the document in exactly 100 words."
            elif summary_option == "Summarize the document in 2 connecting paragraphs":
                summary_instruction = "Summarize the document in two connecting paragraphs."
            elif summary_option == "Summarize the document in 5 bullet points":
                summary_instruction = "Summarize the document in 5 concise bullet points."

        if uploaded_file and summary_option:
            # Process the uploaded file and question.
            document = uploaded_file.read().decode()
            messages = [
                {
                    "role": "user",
                    "content": f"Here's a document: {document}\n\n---\n\n {summary_instruction}",
                }
            ]

            # Generate an answer using the OpenAI API.
            stream = client.chat.completions.create(
                model=model_choice,
                messages=messages,
                stream=True,
            )

            # Stream the response to the app using `st.write_stream`.
            st.write_stream(stream)

    except Exception as e:
        st.error("Invalid API key. Please enter a valid OpenAI API key.", icon="❌")