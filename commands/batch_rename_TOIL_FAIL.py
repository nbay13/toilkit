import os
import subprocess

# Create a directory to store renamed files
os.makedirs("renamed", exist_ok=True)

# Loop through all files starting with "FAIL" and ending with ".tar.gz"
for file in os.listdir():
    if file.startswith("FAIL") and file.endswith(".tar.gz"):
        print(file)
        # Extract the UUID from the filename
        new_name = file.split(".")[1]
        # Extract the contents of the archive using subprocess
        subprocess.run(["tar", "-xvzf", file])
        # Rename the extracted directory
        subprocess.run(["mv", file.replace(".tar.gz", ""), new_name])
        # Create a new archive with the renamed directory using subprocess
        subprocess.run(["tar", "-czvf", new_name + ".tar.gz", new_name])
        # Clean up the extracted directory
        subprocess.run(["rm", "-r", new_name])
        # Move the original file to the renamed directory
        subprocess.run(["mv", file, "renamed"])
