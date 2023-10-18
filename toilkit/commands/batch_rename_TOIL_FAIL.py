import os
import shutil
import tarfile

def batch_rename_TOIL_FAIL(args):
    # Create a directory for renamed files in the specified directory
    renamed_dir = os.path.join(args.dir, "renamed")
    os.makedirs(renamed_dir, exist_ok=True)

    for file in os.listdir(args.dir):
        file_path = os.path.join(args.dir, file)
        if file.startswith("FAIL.") and file.endswith(".tar.gz"):
            print(f"Processing file: {file}")

            # Extract the UUID from the file name
            new_name = file.split(".")[1]
            new_path = os.path.join(args.dir, new_name)
            
            # Unzipping the file
            print(f"\tExtracting file: {file}")
            with tarfile.open(file_path, "r:gz") as tar:
                tar.extractall(path=args.dir)

            # Renaming the FAIL.UUID_X folder that got extracted
            extracted_folder = os.path.join(args.dir, file.replace(".tar.gz", ""))  
            print(f"\tRenaming folder: {extracted_folder} to {new_path}")
            os.rename(extracted_folder, new_path)

            # Create a new tar.gz archive as UUID_X.tar.gz
            print(f"\tCreating new archive: {new_name}.tar.gz")
            with tarfile.open(os.path.join(args.dir, new_name + ".tar.gz"), "w:gz") as tar:
                tar.add(new_path)

            # Remove the extracted folder
            print(f"\tRemoving extracted folder: {new_path}")
            shutil.rmtree(new_path)

            # Move the original file to the 'renamed' directory
            print(f"\tMoving original file: {file} to {os.path.join(renamed_dir, file)}")
            shutil.move(file_path, os.path.join(renamed_dir, file))