import streamlit as st
import subprocess
from script_generator import generate_installation_script

import sys
import os
import re

# Ensure Python finds the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.title("LLM-Based Installation Script Generator")

repo_url = st.text_input("Enter GitHub Repo URL:")
os_choice = st.selectbox("Select OS:", ["Linux", "macOS", "Windows"])

if st.button("Generate Script"):
    if not repo_url:
        st.error("Please enter a GitHub repository URL.")
    else:
        generated_codes = generate_installation_script(repo_url, os_choice)
        script_content = generated_codes[1]

        # Extract only the script code blocks
        extracted_code_blocks = re.findall(
            r"```(?:[a-zA-Z]+)?\n(.*?)```", script_content, re.DOTALL
        )

        # Join all extracted code blocks into a single script
        script_content = (
            "\n\n".join(extracted_code_blocks)
            if extracted_code_blocks
            else "No script found."
        )

        # Display the script in the text area
        st.text_area("Generated Script:", script_content, height=300)

        # Save Script button
        file_ext = "sh" if os_choice != "Windows" else "bat"
        file_path = f"install_script.{file_ext}"

        st.download_button(
            label="Download Script",
            data=script_content,
            file_name=generated_codes[0],
            mime="text/plain",
        )

        # Run Script button (disabled for safety)
        if st.button("Run Script"):
            st.warning("For security reasons, script execution is disabled.")
