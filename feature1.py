import os
import shutil

# Define categories and associated keywords
categories = {
    'Plan': ['plan'],
    'Reports': ['report'],
    'Approval': ['approval'],
    'Specifications': ['specifications', 'specs'],
    'Drawings': ['drawing'],
    'Civil': ['civil'],
    'Electrical': ['electrical', 'electric'],
    'Landscape': ['landscape'],
    'Survey': ['survey'],
    'Rating': ['rating'],
    'Engineering': ['engineering'],
    'Property Details': ['property']
}

# Function to classify a file based on its name
def classify_file(file_name):
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in file_name.lower():
                return category
    return 'Others'

# Function to organize files into folders
def organize_files(source_dir, destination_dir):
    # Create destination directories if they don't exist
    for category in categories.keys():
        os.makedirs(os.path.join(destination_dir, category), exist_ok=True)
    
    # Iterate through files in the source directory
    for file_name in os.listdir(source_dir):
        source_file_path = os.path.join(source_dir, file_name)
        if os.path.isfile(source_file_path):
            # Classify the file
            category = classify_file(file_name)
            # Move the file to the corresponding category folder
            destination_file_path = os.path.join(destination_dir, category, file_name)
            shutil.move(source_file_path, destination_file_path)
            print(f"Moved '{file_name}' to '{category}' folder.")

# Example usage
if __name__ == "__main__":
    source_directory = "Dataset\Survey"
    destination_directory = "destination"
    organize_files(source_directory, destination_directory)
