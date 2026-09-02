import pathlib

def createfile():
    file_name = input("Enter your file name with extension : ")

    try:
        path = pathlib.Path(file_name)

        if  path.exists():
            print("This file already exists!")

        else:

            print(f"\nEnter yes if you want to add data into {file_name}")
            print(f" Enter no if you want to create an empty file {file_name}\n")

            choice = input("Enter yes or no:").strip().lower()

            # to create a file having content 
            if choice == "yes" :
                 with open(file_name, "w") as f:
                  content = input("\nEnter content to write in your file\n--> ")
                  f.write(content)
                 print("File created successfully!")   

            # to create an empty file
            elif choice == "no":
                with open(file_name,"x") as f:
                    pass
                print("\nEmpty file created successfully!")
            else:
                print("\nInvalid choice please enter yes or no.")

    except Exception as error:
        print(f"An error occurred as {error}")

def readfile():
    file_name = input("\nEnter your file name with extension: ")

    try:
        path  = pathlib.Path(file_name)
        if path.is_file():
         with open(file_name) as f:
          content = f.read()
         print(f"\nYour file content is :\n {content}")

        else:
            print("\nGiven file does not exist.")   
        
    except Exception as error:
        print(f"An error occurred as {error}")     


def updatefile():
    try:        
        file_name = input("\nEnter your file name with extension: ")
        path = pathlib.Path(file_name)

        print("\nEnter 1 to rename your file.")
        print("Enter 2 to append content in your file.")
        print("Enter 3 to replace content in your file.")

        choice = int(input("\nEnter your choice:"))

        # to rename a file 
        if choice == 1:

            if path.is_file():

                new_file_name = input("\nEnter your new file name with extension: ")

                new_path = pathlib.Path(new_file_name)

                if new_path.exists():
                   print("This file already exists!")

                else:
                   path.rename(new_file_name) 
                   print("File renamed successfully!")

            else:
                print("\nThe file you wanted to rename does not exist.")

        # to append content in a file 
        elif choice == 2:

            if path.is_file():
                with open(file_name,"a") as f:
                    content = input("\nEnter content to update in file -->\n")
                    f.write("\n" + content) 
                print("Content appended successfully!")

            else: 
                print("Given file does not exist!")

        # to replace content or overwrite a file
        elif choice == 3:

            if path.is_file():
                with open(file_name,"w") as f:
                    content = input("\nEnter content to replace in file\n--> ")
                    f.write(content)
                print("Content replaced successfully!")

            else:
                print("Given file does not exist.")    

        else:
            print("Invalid choice please choose between 1, 2, and 3.")   

    except Exception as error:
        print(f"An error occurred as {error}")


def deletefile():
    try: 
         
        file_name = input("\nEnter your file name with extension:  ")
        path = pathlib.Path(file_name)

        if path.is_file():
            path.unlink()
            print("File deleted successfully!")
        else:
            print("\nGiven file does not exist.") 
               
    except Exception as error:
        print(f"An error occurred as {error}")


def listfiles():
    try :
        for item in pathlib.Path.cwd().iterdir():
            if item.is_file():
             print(item)
    except OSError:
        print("An error occurred while listing files.")         


def fileinfo():
    try:
        file_name = input("Enter your file name with extension: ")
        path = pathlib.Path(file_name)

        if path.is_file():
            print(f"\nFile information: \n {path.stat()}")
        else:
            print("\nGiven file does not exist!")
            
    except Exception as error:          
        print(f"An error occurred as {error}")
