import streamlit as st
import os
import subprocess
from google import genai

# import google.generativeai as genai

# from google import genai

# import google.generativeai as genai

# Initialize Gemini Client
client = genai.Client(api_key="")


def extract_docker_instructions(repo_path):
    """Extracts Docker instructions from README if available, otherwise uses CMD from Dockerfile."""
    readme_path = os.path.join(repo_path, "README.md")
    dockerfile_path = os.path.join(repo_path, "Dockerfile")

    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        docker_commands = [line.strip() for line in lines if "docker" in line.lower()]
        if docker_commands:
            return "\n".join(docker_commands)

    if os.path.exists(dockerfile_path):
        with open(dockerfile_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        cmd_lines = [line.strip() for line in lines if "CMD" in line.upper()]
        return "\n".join(cmd_lines) if cmd_lines else ""

    return ""


def call_gemini_api(prompt):
    """Calls Google's Gemini API to generate an installation script based on the GitHub repo."""
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    return (
        response.text
        if response and hasattr(response, "text")
        else "# Failed to generate script using Gemini API"
    )


def validate_script(script):
    """Checks if the script contains unrelated or malicious commands."""
    forbidden_keywords = [
        "rm -rf /",
        "sudo",
        "curl",
        "wget",
        "chmod 777",
        "powershell",
        "Invoke-WebRequest",
    ]
    for keyword in forbidden_keywords:
        if keyword in script:
            return False
    return True


st.title("LLM-Based Installation Script Generator")
repo_url = st.text_input("Enter GitHub Repo URL:")
os_choice = st.selectbox("Select OS:", ["Linux", "macOS", "Windows"])

if st.button("Generate Script"):
    if not repo_url:
        st.error("Please enter a GitHub repository URL.")
    else:
        prompt = f"Generate a step-by-step installation script for {repo_url} on {os_choice}. Include detailed comments explaining each step. Ensure best practices for security and dependency management."
        script_content = call_gemini_api(prompt)

        if True: #not validate_script(script_content):
            st.error("Generated script contains potentially unsafe commands.")
        else:
            st.text_area("Generated Script:", script_content, height=300)

            if st.button("Save Script"):
                file_path = (
                    f"install_script_{os_choice.lower()}.sh"
                    if os_choice != "Windows"
                    else f"install_script_{os_choice.lower()}.bat"
                )
                with open(file_path, "w") as f:
                    f.write(script_content)
                st.success(f"Script saved as {file_path}")

            if st.button("Run Script"):
                temp_file = (
                    f"install_script.sh"
                    if os_choice != "Windows"
                    else "install_script.bat"
                )
                with open(temp_file, "w") as f:
                    f.write(script_content)
                os.chmod(temp_file, 0o755)
                if os_choice == "Windows":
                    subprocess.run(["cmd.exe", "/c", temp_file])
                else:
                    subprocess.run(["/bin/bash", temp_file])
                st.success("Script executed successfully.")
