import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
FRONTEND_REPO = os.getenv("FRONTEND_REPO")  # e.g. "yourusername/city-time-viewer-frontend"
BACKEND_REPO = os.getenv("BACKEND_REPO")    # e.g. "yourusername/city-time-viewer-backend"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def fetch_commits(repo):
    since = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"  # last 24 hours
    url = f"https://api.github.com/repos/{repo}/commits?since={since}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch commits from {repo}")
        return []
    return response.json()

def format_commits(commits):
    formatted = ""
    for commit in commits:
        message = commit["commit"]["message"].split("\n")[0]
        author = commit["commit"]["author"]["name"]
        formatted += f"- {message} ({author})\n"
    return formatted if formatted else "- No updates.\n"

def write_log(frontend_commits, backend_commits):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log = f"# 📔 Mascot Log – {today}\n\n"
    log += "## 🌸 Aoyuki (Frontend)\n"
    log += format_commits(frontend_commits) + "\n"
    log += "## 🌙 Madison (Backend)\n"
    log += format_commits(backend_commits)

    with open("latest_updates.md", "w", encoding='utf-8') as f:
        f.write(log)

def main():
    frontend = fetch_commits(FRONTEND_REPO)
    print(FRONTEND_REPO)
    backend = fetch_commits(BACKEND_REPO)
    print(BACKEND_REPO)
    write_log(frontend, backend)

if __name__ == "__main__":
    main()
