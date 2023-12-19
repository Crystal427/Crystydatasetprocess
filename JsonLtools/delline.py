import os

def remove_first_six_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines[6:])

def main(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            remove_first_six_lines(file_path)
            print(f"Processed {file_path}")

if __name__ == "__main__":
    directory_path = input("Enter the directory path: ").strip()
    main(directory_path)

