import os
import requests
import sys

SONAR_HOST_URL = os.environ["SONAR_HOST_URL"]
SONAR_TOKEN = os.environ["SONAR_TOKEN"]
PROJECT_KEY = os.environ["SONAR_PROJECT_KEY"]

def get_quality_gate_status():
    url = f"{SONAR_HOST_URL}api/qualitygates/project_status?projectKey={PROJECT_KEY}"
    resp = requests.get(url, auth=(SONAR_TOKEN, ""))
    resp.raise_for_status()
    return resp.json()["projectStatus"]["status"]

def main():
    status = get_quality_gate_status()
    if status == "OK":
        print("✅ Quality Gate: Passed")
        sys.exit(0)
    else:
        print("❌ Quality Gate: Failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
