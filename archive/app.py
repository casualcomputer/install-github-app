from flask import Flask, request, render_template, jsonify
import requests
import os
import subprocess

app = Flask(__name__)

DEEPSEEK_API_KEY = "YOUR_API_KEY"

def call_deepseek_api(prompt):
    """Calls DeepSeek API to generate an installation script."""
    url = "https://api.deepseek.com/generate"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": prompt, "max_tokens": 1000}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("text", "")
    return "# Failed to generate script using DeepSeek API"

def validate_script(script):
    """Checks if the script contains unrelated or malicious commands."""
    forbidden_keywords = ["rm -rf", "sudo", "curl", "wget", "chmod 777"]
    for keyword in forbidden_keywords:
        if keyword in script:
            return False
    return True

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_script():
    data = request.json
    repo_url = data.get("repo_url")
    os_choice = data.get("os_choice")

    if not repo_url:
        return jsonify({"error": "Missing GitHub repository URL"}), 400

    # Generate script using DeepSeek
    prompt = f"Generate an installation script for {repo_url} on {os_choice}."
    script_content = call_deepseek_api(prompt)

    # Validate script
    if not validate_script(script_content):
        return jsonify({"error": "Generated script contains potentially unsafe commands"}), 400

    return jsonify({"script": script_content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
