import os
import sys

if len(sys.argv) < 2:
    print("Error: Needs chap number or range")
    directory = "."

    for filename in os.listdir(directory):
        if filename.startswith("Chapter"):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"{file_path} has been deleted.")
            else:
                print(f"{file_path} is not a file and was not deleted.")
    sys.exit()

chap = int(sys.argv[1])
last = int(sys.argv[2]) + 1 if len(sys.argv) > 2 else chap + 1

for i in range(chap, last):

    file_path = "Chapter " + str(i) + ".txt"

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")
