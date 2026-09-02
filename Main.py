from File_Operations import createfile, readfile, updatefile, deletefile, listfiles, fileinfo 

while True:
    try:
        print("\nEnter 1 to create file.")
        print("Enter 2 to read file.")
        print("Enter 3 to update file.")
        print("Enter 4 to delete file.")
        print("Enter 5 to list files.")
        print("Enter 6 to display file information")
        print("Enter 7 to exit.")

        choice = int(input("\nEnter your choice: "))

        if choice == 1:
            createfile()

        elif choice == 2:
            readfile()

        elif choice == 3:
            updatefile()

        elif choice == 4:
            deletefile()

        elif choice == 5:
            listfiles()

        elif choice == 6:
            fileinfo()   

        elif choice == 7:
            print("Exiting...!")
            break

        else:
            print("Invalid choice please choose between 1 to 7.")

    except ValueError:
        print("Please enter a number between 1 and 7.")        
