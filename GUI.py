import pathlib
import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="File Management System", page_icon="📁", layout="wide")

# ---------- Minimal custom CSS ----------
# This just adds a bit of spacing/rounding to make cards and buttons look
# cleaner. Nothing here changes how the app behaves - purely cosmetic.
st.markdown(
    """
    <style>
        /* Add a little breathing room around the main content */
        .block-container {
            padding-top: 2rem;
        }
        /* Rounded, slightly larger buttons */
        div.stButton > button {
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
        }
        /* Style the metric cards in the dashboard header */
        div[data-testid="stMetric"] {
            background-color: rgba(120, 120, 120, 0.08);
            border-radius: 10px;
            padding: 0.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Helper functions (pure UI helpers, no logic changes) ----------

def get_file_list():
    """Return a list of file names (not folders) in the current directory."""
    try:
        return sorted(
            [item.name for item in pathlib.Path.cwd().iterdir() if item.is_file()]
        )
    except OSError:
        return []


def human_readable_size(num_bytes):
    """Convert a byte count into a readable string like '12.3 KB'."""
    size = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


# ---------- Header / Dashboard ----------
st.title("📁 File Management System")
st.caption("A simple, beginner-friendly Streamlit GUI for managing your files.")

all_files = get_file_list()
total_size = 0
for name in all_files:
    try:
        total_size += pathlib.Path(name).stat().st_size
    except OSError:
        pass

col1, col2, col3 = st.columns(3)
col1.metric("📄 Total Files", len(all_files))
col2.metric("💾 Total Size", human_readable_size(total_size) if all_files else "0 B")
col3.metric("📂 Current Folder", pathlib.Path.cwd().name)

st.divider()

# ---------- Sidebar ----------
st.sidebar.title("📁 Navigation")
st.sidebar.markdown("Use the tabs on the main page to manage your files.")

st.sidebar.divider()
st.sidebar.subheader("Working Directory")
st.sidebar.code(str(pathlib.Path.cwd()), language=None)

st.sidebar.divider()
st.sidebar.subheader("Quick Stats")
st.sidebar.write(f"**Files found:** {len(all_files)}")
st.sidebar.write(f"**Total size:** {human_readable_size(total_size) if all_files else '0 B'}")

st.sidebar.divider()
st.sidebar.caption("💡 Tip: switch tabs to Create, Read, Update, Delete, List, or Info.")

# Organize everything into tabs, same 6 features as the CLI menu
tab_create, tab_read, tab_update, tab_delete, tab_list, tab_info = st.tabs(
    ["➕ Create", "📖 Read", "✏️ Update", "🗑️ Delete", "📋 List Files", "ℹ️ File Info"]
)

# ---------------------------------------------------------
# 1. CREATE FILE
# ---------------------------------------------------------
with tab_create:
    st.subheader("➕ Create a New File")
    st.caption("Create an empty file, or create one with content already inside.")

    with st.container(border=True):
        file_name = st.text_input("File name (with extension)", key="create_name")
        add_content = st.checkbox("Add content while creating", key="create_add_content")

        content = ""
        if add_content:
            content = st.text_area("Enter content to write in your file", key="create_content")

        create_clicked = st.button("Create File", key="create_btn", type="primary")

    if create_clicked:
        if not file_name.strip():
            st.warning("⚠️ Please enter a file name.")
        else:
            try:
                path = pathlib.Path(file_name)

                if path.exists():
                    st.error("❌ This file already exists!")
                else:
                    if add_content:
                        with open(file_name, "w") as f:
                            f.write(content)
                        st.success(f"✅ File **{file_name}** created successfully!")
                    else:
                        with open(file_name, "x") as f:
                            pass
                        st.success(f"✅ Empty file **{file_name}** created successfully!")
            except Exception as error:
                st.error(f"❌ An error occurred as {error}")

# ---------------------------------------------------------
# 2. READ FILE
# ---------------------------------------------------------
with tab_read:
    st.subheader("📖 Read File Contents")
    st.caption("Pick a file from the list below (or type a name) to view its content.")

    with st.container(border=True):
        files = get_file_list()
        if files:
            # Dropdown of existing files, with an option to type a name manually
            options = ["(type a file name manually)"] + files
            selection = st.selectbox("Select a file", options, key="read_select")
            if selection == "(type a file name manually)":
                file_name = st.text_input("File name (with extension)", key="read_name")
            else:
                file_name = selection
        else:
            st.info("No files found in this directory yet.")
            file_name = st.text_input("File name (with extension)", key="read_name")

        read_clicked = st.button("Read File", key="read_btn", type="primary")

    if read_clicked:
        if not file_name.strip():
            st.warning("⚠️ Please enter a file name.")
        else:
            try:
                path = pathlib.Path(file_name)
                if path.is_file():
                    with open(file_name) as f:
                        file_content = f.read()
                    st.success(f"✅ **{file_name}** read successfully!")
                    st.text_area("File content", value=file_content, height=250, disabled=True)
                else:
                    st.error("❌ Given file does not exist.")
            except Exception as error:
                st.error(f"❌ An error occurred as {error}")

# ---------------------------------------------------------
# 3. UPDATE FILE (rename / append / replace)
# ---------------------------------------------------------
with tab_update:
    st.subheader("✏️ Update a File")
    st.caption("Rename a file, append new content, or fully replace its content.")

    update_choice = st.radio(
        "What would you like to do?",
        ["Rename file", "Append content", "Replace content"],
        key="update_choice",
        horizontal=True,
    )

    with st.container(border=True):
        file_name = st.text_input("File name (with extension)", key="update_name")

        # --- Rename ---
        if update_choice == "Rename file":
            new_file_name = st.text_input("New file name (with extension)", key="update_new_name")
            rename_clicked = st.button("Rename", key="rename_btn", type="primary")

            if rename_clicked:
                try:
                    path = pathlib.Path(file_name)
                    if path.is_file():
                        new_path = pathlib.Path(new_file_name)
                        if new_path.exists():
                            st.error("❌ This file already exists!")
                        else:
                            path.rename(new_file_name)
                            st.success(f"✅ File renamed to **{new_file_name}** successfully!")
                    else:
                        st.error("❌ The file you wanted to rename does not exist.")
                except Exception as error:
                    st.error(f"❌ An error occurred as {error}")

        # --- Append ---
        elif update_choice == "Append content":
            append_content = st.text_area("Content to append", key="append_content")
            append_clicked = st.button("Append", key="append_btn", type="primary")

            if append_clicked:
                try:
                    path = pathlib.Path(file_name)
                    if path.is_file():
                        with open(file_name, "a") as f:
                            f.write("\n" + append_content)
                        st.success(f"✅ Content appended to **{file_name}** successfully!")
                    else:
                        st.error("❌ Given file does not exist!")
                except Exception as error:
                    st.error(f"❌ An error occurred as {error}")

        # --- Replace ---
        elif update_choice == "Replace content":
            replace_content = st.text_area("New content (this will overwrite the file)", key="replace_content")
            replace_clicked = st.button("Replace", key="replace_btn", type="primary")

            if replace_clicked:
                try:
                    path = pathlib.Path(file_name)
                    if path.is_file():
                        with open(file_name, "w") as f:
                            f.write(replace_content)
                        st.success(f"✅ Content replaced in **{file_name}** successfully!")
                    else:
                        st.error("❌ Given file does not exist.")
                except Exception as error:
                    st.error(f"❌ An error occurred as {error}")

# ---------------------------------------------------------
# 4. DELETE FILE (with confirmation) - visually flagged as destructive
# ---------------------------------------------------------
with tab_delete:
    st.subheader("🗑️ Delete a File")
    st.error("⚠️ This action is permanent and cannot be undone. Please double-check before confirming.")

    with st.container(border=True):
        files = get_file_list()
        if files:
            options = ["(type a file name manually)"] + files
            selection = st.selectbox("Select a file to delete", options, key="delete_select")
            if selection == "(type a file name manually)":
                file_name = st.text_input("File name (with extension)", key="delete_name")
            else:
                file_name = selection
        else:
            st.info("No files found in this directory yet.")
            file_name = st.text_input("File name (with extension)", key="delete_name")

        confirm = st.checkbox("Yes, I confirm I want to permanently delete this file", key="delete_confirm")
        delete_clicked = st.button("🗑️ Delete File", key="delete_btn", type="primary")

    if delete_clicked:
        if not file_name.strip():
            st.warning("⚠️ Please enter a file name.")
        elif not confirm:
            st.warning("⚠️ Please check the confirmation box before deleting.")
        else:
            try:
                path = pathlib.Path(file_name)
                if path.is_file():
                    path.unlink()
                    st.success(f"✅ File **{file_name}** deleted successfully!")
                else:
                    st.error("❌ Given file does not exist.")
            except Exception as error:
                st.error(f"❌ An error occurred as {error}")

# ---------------------------------------------------------
# 5. LIST FILES
# ---------------------------------------------------------
with tab_list:
    st.subheader("📋 Files in Current Directory")

    if st.button("🔄 Refresh List", key="list_btn", type="primary"):
        st.session_state["show_file_table"] = True

    if st.session_state.get("show_file_table"):
        files = get_file_list()
        if files:
            st.write(f"Found **{len(files)}** file(s):")

            # Header row for the "table"
            h1, h2, h3 = st.columns([3, 1, 1])
            h1.markdown("**File Name**")
            h2.markdown("**Type**")
            h3.markdown("**Size**")

            for name in files:
                path = pathlib.Path(name)
                extension = path.suffix if path.suffix else "—"
                try:
                    size = human_readable_size(path.stat().st_size)
                except OSError:
                    size = "—"

                c1, c2, c3 = st.columns([3, 1, 1])
                c1.write(f"📄 {name}")
                c2.write(extension)
                c3.write(size)
        else:
            st.info("No files found in this directory.")

# ---------------------------------------------------------
# 6. FILE INFORMATION
# ---------------------------------------------------------
with tab_info:
    st.subheader("ℹ️ File Information")
    st.caption("Select a file to see its size and timestamps.")

    with st.container(border=True):
        files = get_file_list()
        if files:
            options = ["(type a file name manually)"] + files
            selection = st.selectbox("Select a file", options, key="info_select")
            if selection == "(type a file name manually)":
                file_name = st.text_input("File name (with extension)", key="info_name")
            else:
                file_name = selection
        else:
            st.info("No files found in this directory yet.")
            file_name = st.text_input("File name (with extension)", key="info_name")

        info_clicked = st.button("Get Info", key="info_btn", type="primary")

    if info_clicked:
        if not file_name.strip():
            st.warning("⚠️ Please enter a file name.")
        else:
            try:
                path = pathlib.Path(file_name)
                if path.is_file():
                    stats = path.stat()
                    st.success(f"✅ File **{file_name}** found! Here is its information:")

                    i1, i2 = st.columns(2)
                    i1.metric("Size", human_readable_size(stats.st_size))
                    i2.metric("Extension", path.suffix if path.suffix else "—")

                    st.write(f"**Last modified (timestamp):** {stats.st_mtime}")
                    st.write(f"**Created (timestamp):** {stats.st_ctime}")

                    with st.expander("Show raw stat() output"):
                        st.code(str(stats))
                else:
                    st.error("❌ Given file does not exist!")
            except Exception as error:
                st.error(f"❌ An error occurred as {error}")
