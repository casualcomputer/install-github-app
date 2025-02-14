import streamlit as st
import sys
import os
import re

# Ensure the project root is in the Python path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the installation script generator.
# This function should return a tuple: (file_name, script_generator)
from script_generator import generate_installation_script

st.title("LLM-Based Installation Script Generator")

# User inputs for the repository URL and target OS.
repo_url = st.text_input("Enter GitHub Repo URL:")
os_choice = st.selectbox("Select OS:", ["Linux", "macOS", "Windows"])

if st.button("Generate Script"):
    if not repo_url:
        st.error("Please enter a GitHub repository URL.")
    else:
        # Create a placeholder to display streaming output.
        script_placeholder = st.empty()
        full_script_content = ""

        # Call the installation script generator.
        # It returns the desired file name and a generator that yields text chunks.
        file_name, script_generator = generate_installation_script(repo_url, os_choice)

        # Stream the output from the generator to the UI.
        with st.spinner("Generating installation script..."):
            for chunk in script_generator:
                full_script_content += chunk
                script_placeholder.text(full_script_content)

        # Optionally, if the LLM output uses markdown code blocks,
        # extract only the code blocks with a regex.
        extracted_code_blocks = re.findall(
            r"```(?:[a-zA-Z]+)?\n(.*?)```", full_script_content, re.DOTALL
        )
        script_code = (
            "\n\n".join(extracted_code_blocks)
            if extracted_code_blocks
            else full_script_content
        )

        # Display the final generated script in a text area.
        # st.text_area("Generated Script:", script_code, height=300)

        # Prepare a download button for the generated script.
        file_ext = "sh" if os_choice != "Windows" else "bat"
        download_file_name = f"install_script.{file_ext}"
        st.download_button(
            label="Download Script",
            data=script_code,
            file_name=download_file_name,
            mime="text/plain",
        )
