import streamlit as st
import subprocess
from script_generator import (
    generate_installation_script,
)  # Assumes this returns the script content

import sys
import os

# Ensure Python finds the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.title("LLM-Based Installation Script Generator")

# Input fields for GitHub repo URL and OS selection.
repo_url = st.text_input("Enter GitHub Repo URL:")
os_choice = st.selectbox("Select OS:", ["Linux", "macOS", "Windows"])

# Informational message about potential data path requirements.
st.info(
    """
    **Important Notice:**
    
    Some installation scripts may require you to provide data paths, store pre-existing data, or adjust settings manually. 
    Please review the generated script carefully before running it.
    """
)

# User confirmation before enabling script execution
user_confirmation = st.checkbox(
    "I acknowledge that I have reviewed the potential data requirements."
)

if st.button("Generate Script"):
    if not repo_url:
        st.error("Please enter a GitHub repository URL.")
    else:
        # Generate the installation script
        script_content = generate_installation_script(repo_url, os_choice)

        # Display the generated script in a text area.
        st.text_area("Generated Script:", script_content, height=300)

        # Heuristic warning if script might require manual data input
        if "data" in script_content.lower() or "path" in script_content.lower():
            st.warning(
                "The generated script appears to reference data paths or data storage. "
                "Please review these sections carefully."
            )

        if user_confirmation:
            file_ext = "sh" if os_choice != "Windows" else "bat"
            file_name = f"install_script.{file_ext}"

            # Use st.download_button for downloading the script
            st.download_button(
                label="Download Script",
                data=script_content,
                file_name=file_name,
                mime="text/plain",
            )

            # Disable execution for security reasons
            if st.button("Run Script"):
                st.warning("For security reasons, script execution is disabled.")
        else:
            st.warning(
                "Please check the confirmation box above after reviewing the script to enable downloading."
            )
