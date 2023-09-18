import requests
import json

# Your GitHub personal access token
access_token = "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"

# The GitHub repository information
repository_owner = "jdhzzz"
repository_name = "commit-diff-api"

# The two commit SHA hashes
commit_sha1 = "88e0ecb"
commit_sha2 = "d036443"

# GraphQL API endpoint
url = "https://api.github.com/graphql"

# GraphQL query to get the difference between two commits
query = f"""
{{
  repository(owner: "{repository_owner}", name: "{repository_name}") {{
    commit: object(oid: "{commit_sha1}") {{
      ... on Commit {{
        tree {{
          entries {{
            name
            object {{
              ... on Blob {{
                text
              }}
            }}
          }}
        }}
      }}
    }}
  }}
}}
"""

headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/vnd.github.v3+json",
}

# Make the GraphQL API request
response = requests.post(url, headers=headers, json={"query": query})

if response.status_code == 200:
    data = response.json()
    commit_data = data["data"]["repository"]["commit"]
    tree_entries = commit_data["tree"]["entries"]
    
    # Print the names and contents of the files changed in the commit
    for entry in tree_entries:
        file_name = entry["name"]
        file_content = entry["object"]["text"]
        print(f"File Name: {file_name}\nFile Content:\n{file_content}\n")
else:
    print(f"Failed to fetch data from GitHub. Status code: {response.status_code}")

