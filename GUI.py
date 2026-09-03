"""
GUI.py - Streamlit-based GUI for the File Management System

NOTE ON DESIGN:
The functions in File_Operations.py (createfile, readfile, updatefile, etc.)
use Python's input() to get data from the terminal. Streamlit apps don't
work that way - there's no terminal loop, and every button click reruns
the whole script. Because of that, those functions can't be imported and
called directly here.

To stay as close as possible to the original project, this file uses the
SAME logic (pathlib, same checks, same success/error messages) as
File_Operations.py, just rewritten to read values from Streamlit widgets
instead of input(). Main.py and File_Operations.py are left completely
unchanged, so your original command-line program still works exactly
as before.
"""

import pathlib
import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="File Management System", page_icon="📁", layout="wide")

st.title("📁 File Management System")
st.caption("A simple Streamlit GUI for creating, reading, updating, deleting, and inspecting files.")

# Sidebar - just shows the current working directory for context
st.sidebar.header("Current Directory")
st.sidebar.code(str(pathlib.Path.cwd()))
st.sidebar.caption("All files are created/read relative to this folder.")

# Organize everything into tabs, same 6 features as the CLI menu
tab_create, tab_read, tab_update, tab_delete, tab_list, tab_info = st.tabs(
    ["➕ Create", "📖 Read", "✏️ Update", "🗑️ Delete", "📋 List Files", "ℹ️ File Info"]
)

# ---------------------------------------------------------
# 1. CREATE FILE
# ---------------------------------------------------------
with tab_create:
    st.subheader("Create a New File")

    file_name = st.text_input("File name (with extension)", key="create_name")
    add_content = st.checkbox("Add content while creating", key="create_add_content")

    content = ""
    if add_content:
        content = st.text_area("Enter content to write in your file", key="create_content")

    if st.button("Create File", key="create_btn"):
        if not file_name.strip():
            st.warning("Please enter a file name.")
        else:
            try:
                path = pathlib.Path(file_name)

                if path.exists():
                    st.error("This file already exists!")
                else:
                    if add_content:
                        with open(file_name, "w") as f:
                            f.write(content)
                        st.success("File created successfully!")
                    else:
                        with open(file_name, "x") as f:
                            pass
                        st.success("Empty file created successfully!")
            except Exception as error:
                st.error(f"An error occurred as {error}")

# ---------------------------------------------------------
# 2. READ FILE
# ---------------------------------------------------------
with tab_read:
    st.subheader("Read File Contents")

    file_name = st.text_input("File name (with extension)", key="read_name")

    if st.button("Read File", key="read_btn"):
        if not file_name.strip():
            st.warning("Please enter a file name.")
        else:
            try:
                path = pathlib.Path(file_name)
                if path.is_file():
                    with open(file_name) as f:
                        file_content = f.read()
                    st.success("File read successfully!")
                    st.text_area("File content", value=file_content, height=250, disabled=True)
                else:
                    st.error("Given file does not exist.")
            except Exception as error:
                st.error(f"An error occurred as {error}")

# ---------------------------------------------------------
# 3. UPDATE FILE (rename / append / replace)
# ---------------------------------------------------------
with tab_update:
    st.subheader("Update a File")

    update_choice = st.radio(
        "What would you like to do?",
        ["Rename file", "Append content", "Replace content"],
        key="update_choice",
    )

    file_name = st.text_input("File name (with extension)", key="update_name")

    # --- Rename ---
    if update_choice == "Rename file":
        new_file_name = st.text_input("New file name (with extension)", key="update_new_name")

        if st.button("Rename", key="rename_btn"):
            try:
                path = pathlib.Path(file_name)
                if path.is_file():
                    new_path = pathlib.Path(new_file_name)
                    if new_path.exists():
                        st.error("This file already exists!")
                    else:
                        path.rename(new_file_name)
                        st.success("File renamed successfully!")
                else:
                    st.error("The file you wanted to rename does not exist.")
            except Exception as error:
                st.error(f"An error occurred as {error}")

    # --- Append ---
    elif update_choice == "Append content":
        append_content = st.text_area("Content to append", key="append_content")

        if st.button("Append", key="append_btn"):
            try:
                path = pathlib.Path(file_name)
                if path.is_file():
                    with open(file_name, "a") as f:
                        f.write("\n" + append_content)
                    st.success("Content appended successfully!")
                else:
                    st.error("Given file does not exist!")
            except Exception as error:
                st.error(f"An error occurred as {error}")

    # --- Replace ---
    elif update_choice == "Replace content":
        replace_content = st.text_area("New content (this will overwrite the file)", key="replace_content")

        if st.button("Replace", key="replace_btn"):
            try:
                path = pathlib.Path(file_name)
                if path.is_file():
                    with open(file_name, "w") as f:
                        f.write(replace_content)
                    st.success("Content replaced successfully!")
                else:
                    st.error("Given file does not exist.")
            except Exception as error:
                st.error(f"An error occurred as {error}")

# ---------------------------------------------------------
# 4. DELETE FILE (with confirmation)
# ---------------------------------------------------------
with tab_delete:
    st.subheader("Delete a File")

    file_name = st.text_input("File name (with extension)", key="delete_name")
    confirm = st.checkbox("Yes, I confirm I want to delete this file", key="delete_confirm")

    if st.button("Delete File", key="delete_btn"):
        if not file_name.strip():
            st.warning("Please enter a file name.")
        elif not confirm:
            st.warning("Please check the confirmation box before deleting.")
        else:
            try:
                path = pathlib.Path(file_name)
                if path.is_file():
                    path.unlink()
                    st.success("File deleted successfully!")
                else:
                    st.error("Given file does not exist.")
            except Exception as error:
                st.error(f"An error occurred as {error}")

# ---------------------------------------------------------
# 5. LIST FILES
# ---------------------------------------------------------
with tab_list:
    st.subheader("Files in Current Directory")

    if st.button("Refresh List", key="list_btn"):
        try:
            files = [item.name for item in pathlib.Path.cwd().iterdir() if item.is_file()]
            if files:
                st.write(f"Found {len(files)} file(s):")
                for f in files:
                    st.text(f"📄 {f}")
            else:
                st.info("No files found in this directory.")
        except OSError:
            st.error("An error occurred while listing files.")

# ---------------------------------------------------------
# 6. FILE INFORMATION
# ---------------------------------------------------------
with tab_info:
    st.subheader("File Information")

    file_name = st.text_input("File name (with extension)", key="info_name")

    if st.button("Get Info", key="info_btn"):
        if not file_name.strip():
            st.warning("Please enter a file name.")
        else:
            try:
                path = pathlib.Path(file_name)
                if path.is_file():
                    stats = path.stat()
                    st.success("File found! Here is its information:")
                    st.write(f"**Size:** {stats.st_size} bytes")
                    st.write(f"**Last modified (timestamp):** {stats.st_mtime}")
                    st.write(f"**Created (timestamp):** {stats.st_ctime}")
                    with st.expander("Show raw stat() output"):
                        st.code(str(stats))
                else:
                    st.error("Given file does not exist!")
            except Exception as error:
                st.error(f"An error occurred as {error}")