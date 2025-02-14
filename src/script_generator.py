from api_handler import call_gemini_api


# def generate_installation_script(repo_url, os_choice):
#     """Generates an installation script based on OS and repo contents."""
#     prompt = f"""
#     Generate a step-by-step installation script for {repo_url} on {os_choice}.
#     - Check for requirements.txt or environment.yml and install dependencies.
#     - If Dockerfile exists, build and run the container.
#     - Ensure the script is secure and follows best practices.
#     - Include detailed comments explaining each step.
#     """
#     return call_gemini_api(prompt)


# def generate_installation_script(repo_url, os_choice):
#     """
#     Generates an installation script based on the OS and repository contents.
#     Returns:
#         tuple: (file_name, script_content)
#     """

#     # Map operating system to the appropriate file extension.
#     file_extension = {
#         "Linux": "sh",
#         "macOS": "sh",
#         "Windows": "ps1",  # Use PowerShell for Windows.
#     }.get(
#         os_choice, "sh"
#     )  # Default to shell script.

#     file_name = f"install_script.{file_extension}"

#     # Generalized prompt template with placeholders for dynamic insertion.
#     prompt_template = """
#     Generate an installation script for the repository located at {repo_url} on {os_choice}.
#     The script should follow these guidelines:

#     1. **Dependency Checks**:
#        - Detect if a `requirements.txt` exists and run: `pip install -r requirements.txt`.
#        - If an `environment.yml` is present, execute: `conda env create -f environment.yml`.
#        - If a `Dockerfile` is found, build the Docker image.
#        - If a `docker-compose.yml` exists, ensure proper setup using docker-compose commands.

#     2. **User Configuration**:
#        - Prompt the user for configuration parameters such as:
#          - Storage paths or directories.
#          - Database credentials or any other sensitive parameters.
#        - Provide default values where applicable.
#        - Validate that necessary directories exist and have proper permissions.

#     3. **Error Handling and Robustness**:
#        - For shell scripts (Linux/macOS), include `set -e` to exit on errors.
#        - For Windows (PowerShell), implement Try-Catch blocks to handle exceptions.
#        - Ensure the script gracefully handles being re-run (idempotence).

#     4. **Security and Best Practices**:
#        - Include comments that explain each step clearly.
#        - Implement permission checks (e.g., use `chmod +x` for executables).
#        - Handle sensitive information securely (avoid plain-text credentials).
#        - If elevated privileges are required, provide clear instructions or prompts.

#     5. **Final Execution Instructions**:
#        - Conclude the script with instructions or a summary of what was executed.
#        - Ensure that the script works correctly whether the repository is freshly cloned or already exists.

#     Format the script appropriately for {os_choice}, ensuring the correct syntax and conventions for the target environment.
#     """

#     # Populate the template with dynamic values.
#     prompt = prompt_template.format(repo_url=repo_url, os_choice=os_choice)

#     # Call the LLM API (or your preferred service) to generate the script content.
#     script_content = call_gemini_api(prompt)

#     # Return the generated file name and script content.
#     return file_name, script_content

import time


def call_gemini_api_streaming(prompt):
    # This is a dummy example to simulate streaming.
    # Replace this with your actual LLM streaming API integration.
    full_response = call_gemini_api(prompt)  # get the full response from your LLM
    chunk_size = 100  # Adjust chunk size as needed.
    for i in range(0, len(full_response), chunk_size):
        yield full_response[i : i + chunk_size]
        time.sleep(0.1)  # simulate network latency/delay


def generate_installation_script(repo_url, os_choice):
    """
    Generates an installation script based on the OS and repository contents.
    Returns:
        tuple: (file_name, script_generator)
               file_name (str): the name for the script file.
               script_generator (generator): yields chunks of script content.
    """

    # Map operating system to the appropriate file extension.
    file_extension = {
        "Linux": "sh",
        "macOS": "sh",
        "Windows": "ps1",  # Use PowerShell for Windows.
    }.get(
        os_choice, "sh"
    )  # Default to shell script.

    file_name = f"install_script.{file_extension}"

    # Generalized prompt template with placeholders for dynamic insertion.
    prompt_template = """
    Generate an installation script for the repository located at {repo_url} on {os_choice}.
    The script should follow these guidelines (upon execution, the script shouldn't close):

    1. **Dependency Checks**:
       - If a `Dockerfile` is found, build the Docker image.
              - If a `docker-compose.yml` exists, ensure proper setup using docker-compose commands.
       - Else if , detect if a `requirements.txt` exists and run: `pip install -r requirements.txt`.
       - Else if, f an `environment.yml` is present, execute: `conda env create -f environment.yml`.
       - Else: examine documentations and provide instructions for manual setup (Assuming users have none of the envirnonment set-up already).

    2. **User Configuration**:
       - Prompt the user for configuration parameters such as:
         - Storage paths or directories.
         - Database credentials or any other sensitive parameters.
       - Provide default values where applicable.
       - Validate that necessary directories exist and have proper permissions.

    3. **Error Handling and Robustness**:
       - For shell scripts (Linux/macOS), include `set -e` to exit on errors.
       - For Windows (PowerShell), implement Try-Catch blocks to handle exceptions.
       - Ensure the script gracefully handles being re-run (idempotence).

    4. **Security and Best Practices**:
       - Include comments that explain each step clearly.
       - Implement permission checks (e.g., use `chmod +x` for executables).
       - Handle sensitive information securely (avoid plain-text credentials).
       - If elevated privileges are required, provide clear instructions or prompts.

    5. **Final Execution Instructions**:
       - Conclude the script with instructions or a summary of what was executed.
       - Ensure that the script works correctly whether the repository is freshly cloned or already exists.

    Format the script appropriately for {os_choice}, ensuring the correct syntax and conventions for the target environment.
    """

    # Populate the template with dynamic values.
    prompt = prompt_template.format(repo_url=repo_url, os_choice=os_choice)

    # Define a streaming generator that yields chunks from the LLM.
    def script_stream():
        # call_gemini_api_streaming should yield chunks of text as they arrive.
        # You need to implement this function to interface with your streaming LLM API.
        for chunk in call_gemini_api_streaming(prompt):
            yield chunk

    # Return both the file name and the generator.
    return file_name, script_stream()
