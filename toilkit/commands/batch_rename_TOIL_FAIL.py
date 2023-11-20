import os
import shutil
import tarfile

def extract_and_rename(input_file, output_dir):
    with tarfile.open(input_file, "r:gz") as tar:
        tar.extractall(path=output_dir)

    uuid = os.path.basename(input_file).split('.')[1]
    extracted_folder = os.path.join(output_dir, 'FAIL.' + uuid)
    new_path = os.path.join(output_dir, uuid)

    os.rename(extracted_folder, new_path)

    return new_path, uuid

def re_archive_and_rename(input_dir, output_dir, uuid):
    new_archive_name = f"{uuid}.tar.gz"
    output_file = os.path.join(output_dir, new_archive_name)

    with tarfile.open(output_file, "w:gz") as new_tar:
        for root, _, files in os.walk(input_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, input_dir)
                updated_path = os.path.join(uuid, relative_path)
                new_tar.add(file_path, arcname=updated_path)

    return output_file

def batch_rename_TOIL_FAIL(args):
    renamed_dir = os.path.join(args.dir, "renamed")
    os.makedirs(renamed_dir, exist_ok=True)

    for file in os.listdir(args.dir):
        file_path = os.path.join(args.dir, file)

        if file.startswith("FAIL.") and file.endswith(".tar.gz"):
            print(f"Processing file: {file}")

            try:
                extracted_dir, uuid = extract_and_rename(file_path, args.dir)
                new_archive_file = re_archive_and_rename(extracted_dir, args.dir, uuid)

                # Clean up
                os.remove(file_path)
                shutil.rmtree(extracted_dir)
                shutil.move(new_archive_file, renamed_dir)

            except Exception as e:
                print(f"Error processing {file}: {str(e)}")
