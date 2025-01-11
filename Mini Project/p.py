import hashlib
import os
import csv

def get_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def load_malware_hashes(csv_file):
    malware_hashes = {}
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                malware_hashes[row['hash']] = row['malware_name']
    except Exception as e:
        print(f"Error reading CSV file {csv_file}: {e}")
    return malware_hashes

def check_file_for_malware(file_path, malware_hashes):
    file_hash = get_file_hash(file_path)
    if file_hash:
        if file_hash in malware_hashes:
            print(f"ALERT: {file_path} is infected with {malware_hashes[file_hash]}!")
        else:
            print(f"{file_path} is clean.")

def scan_directory(directory_path, malware_hashes):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            check_file_for_malware(file_path, malware_hashes)



if __name__ == "__main__":

    # Load known malware hashes from CSV
    malware_hashes = load_malware_hashes("malware_hashes.csv")

    # Specify the directory to scan
    directory_to_scan = r"F:\3rd Semester\Mini Project"  
    # directory_to_scan = r"D:\M.Sc\3rd Semester\Mini Project"  

    # Scan the directory for malware
    scan_directory(directory_to_scan, malware_hashes)
