import urllib.request
import json
import datetime
import os

workspace_dir = r"d:\deadshot file\computer_thesisZone_\finland 1"
output_file = os.path.join(workspace_dir, "real_cloud_metrics.json")

# Repository info
repo_owner = "pudelroshan26-sudo"
repo_name = "github_genkins_circleci"

print(f"Scraping cloud metrics for public repository {repo_owner}/{repo_name}...")

gha_runs = []
cci_runs = []

# 1. Fetch GitHub Actions workflow runs
github_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs?per_page=100"
req = urllib.request.Request(
    github_api_url,
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
)

try:
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode())
        runs = res_data.get("workflow_runs", [])
        print(f"Retrieved {len(runs)} workflow runs from GitHub Actions API.")
        
        for run in runs:
            if run.get("conclusion") == "success" or run.get("conclusion") == "failure":
                started = datetime.datetime.strptime(run["run_started_at"], "%Y-%m-%dT%H:%M:%SZ")
                updated = datetime.datetime.strptime(run["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
                duration = (updated - started).total_seconds()
                
                # Split duration roughly among projects based on workflow names/jobs
                path = run.get("path", "")
                project = "unknown"
                if "project_a" in path:
                    project = "project_a"
                elif "project_b" in path:
                    project = "project_b"
                elif "project_c" in path:
                    project = "project_c"
                
                gha_runs.append({
                    "id": run["id"],
                    "project": project,
                    "duration": duration,
                    "conclusion": run["conclusion"],
                    "run_number": run["run_number"]
                })
except Exception as e:
    print(f"Error reading GitHub Actions API: {e}")

# 2. Fetch CircleCI workflows
# CircleCI API v2 uses organization slug (e.g. gh/pudelroshan26-sudo)
circleci_api_url = f"https://circleci.com/api/v2/project/gh/{repo_owner}/{repo_name}/pipeline?branch=main"
req_cci = urllib.request.Request(
    circleci_api_url,
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
)

try:
    with urllib.request.urlopen(req_cci) as response:
        res_data = json.loads(response.read().decode())
        pipelines = res_data.get("items", [])
        print(f"Retrieved {len(pipelines)} pipelines from CircleCI API.")
        
        for pipe in pipelines:
            pipe_id = pipe["id"]
            # Fetch workflow details for each pipeline
            wf_url = f"https://circleci.com/api/v2/pipeline/{pipe_id}/workflow"
            req_wf = urllib.request.Request(
                wf_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            try:
                with urllib.request.urlopen(req_wf) as wf_resp:
                    wf_data = json.loads(wf_resp.read().decode())
                    for wf in wf_data.get("items", []):
                        if wf.get("status") in ["success", "failed"]:
                            created_str = wf.get("created_at")
                            stopped_str = wf.get("stopped_at")
                            duration = 0
                            if created_str and stopped_str:
                                created_t = datetime.datetime.strptime(created_str[:19], "%Y-%m-%dT%H:%M:%S")
                                stopped_t = datetime.datetime.strptime(stopped_str[:19], "%Y-%m-%dT%H:%M:%S")
                                duration = (stopped_t - created_t).total_seconds()
                            
                            # CircleCI has a single pipeline containing multiple workflows or jobs
                            # We can distribute or match based on workflow name
                            cci_runs.append({
                                "id": wf["id"],
                                "name": wf["name"],
                                "duration": duration,
                                "status": wf["status"],
                                "created_at": wf["created_at"]
                            })
            except Exception as e_wf:
                pass
except Exception as e:
    print(f"Error reading CircleCI API: {e}")

# Save the raw scraped metrics
scraped_data = {
    "github_actions_scraped": gha_runs,
    "circleci_scraped": cci_runs
}

with open(output_file, "w") as f:
    json.dump(scraped_data, f, indent=4)

print(f"\nSuccess! Cloud metrics saved to {output_file}")
