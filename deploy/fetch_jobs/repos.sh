#!/bin/bash

set -x

# Define file paths
REPO_LIST_FILE="$WORKSPACE/github_repos.txt"
BRANCHES_LIST_FILE="$WORKSPACE/github_branches.json"

# Fetch repositories
curl -s -H "Accept: application/vnd.github+json" \
     -H "Authorization: Bearer $TOKEN" \
     -H "X-GitHub-Api-Version: 2022-11-28" \
     "https://api.github.com/user/repos?per_page=100" | jq -r '.[].clone_url' > "$REPO_LIST_FILE"

echo "Repositories saved to $REPO_LIST_FILE"

# Initialize JSON object
echo "{" > "$BRANCHES_LIST_FILE"

while read -r repo; do
    # Extract repository name and owner
    repo_name=$(basename "$repo" .git)  # Extract repo name
    repo_owner=$(echo "$repo" | awk -F '/' '{print $(NF-1)}')  # Extract repo owner

    # Construct GitHub API URL correctly
    branchesApiUrl="https://api.github.com/repos/$repo_owner/$repo_name/branches"

    echo "Fetching branches from: $branchesApiUrl"

    # Fetch branches and ensure proper JSON array format
    branches=$(curl -s -H "Accept: application/vnd.github+json" \
         -H "Authorization: Bearer $TOKEN" \
         "$branchesApiUrl" | jq -r '[.[].name]')

    # Handle empty branch list
    if [[ "$branches" == "[]" ]]; then
        branches='["main"]'
    fi

    # Append to JSON
    echo "\"$repo_name\": $branches," >> "$BRANCHES_LIST_FILE"

done < "$REPO_LIST_FILE"

# Remove last comma and close JSON object properly
sed -i '$ s/,$//' "$BRANCHES_LIST_FILE"
echo "}" >> "$BRANCHES_LIST_FILE"

echo "Branches saved to $BRANCHES_LIST_FILE"
