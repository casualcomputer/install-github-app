import os


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
