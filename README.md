# Job Advertisement Processing Tool

This is a Python script that utilizes `langchain_core` and `streamlit` libraries to process job advertisements using Ollama. The tool allows users to paste job ad text or import it from a clipboard and generate either a TLDR summary of the job ad or a professional profile paragraph for their CV.

## Features

- **TLDR Summary**: Summarizes lengthy job ads into concise sections, including required languages/tools, skills, and a brief job summary.
- **Professional Profile Paragraph**: Attempts to generate a professional profile paragraph using the information inserted into INPUT.txt
- **User Interface**: Built with Streamlit for an intuitive and user-friendly interface.

## Requirements

- Ollama running locally
- llama3.2:3b model downloaded

## Usage

1. Modify the src/INPUT.txt by adding your CV to make the LLM attempt to write a professional profile.

2. Start `ollama serve`

3. Run the script using UV, to start the graphical user interface:

   ```bash
   uv run streamlit run src/main.py
   ```
   
To make streamlit not share statistics:

   ```bash
   STREAMLIT_BROWSER_GATHER_USAGE_STATS=false uv run streamlit run src/main.py
   ```

4. The Streamlit app will open in your web browser.

5. Input or paste the text into the text field and press Send for it to be processed by the LLM.
Button actions:
   - **Send**: Sends the current text area content for processing.
   - **Paste**: Pastes content from your clipboard.
   - **Gen Profile**: Generates a professional profile paragraph for your CV (might fail if clipboard manager is not setup (ex: missing xclip or wl-clipboard), will not attempt if job advertisement was previously sent).

![Example](./Example.png) 
