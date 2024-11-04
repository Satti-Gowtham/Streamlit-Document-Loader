import streamlit as st
import os
from rag import (
    convert_to_md,
    load_docs,
    split_text,
    get_chunk_ids,
    add_data_to_db
)

# Constants
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'md'}
UPLOAD_DIR = 'uploaded_files'
MD_DIR = 'md_files'

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MD_DIR, exist_ok=True)

# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'processing' not in st.session_state:
    st.session_state.processing = False

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

st.title("File Upload and Embedding Creation")

# File uploader
uploaded_files = st.file_uploader("Upload files", type=ALLOWED_EXTENSIONS, accept_multiple_files=True, disabled=st.session_state.processing)

# Handle uploaded files
if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file not in st.session_state.uploaded_files:
            st.session_state.uploaded_files.append(uploaded_file)

# Button to write files to DB
if st.button("Write files to DB", disabled=st.session_state.processing):
    if not st.session_state.uploaded_files:
        st.error("No files uploaded. Please upload at least one file.")
    else:
        st.session_state.processing = True  # Set processing state to True
        with st.spinner("Processing files..."):
            # Process each uploaded file
            for uploaded_file in st.session_state.uploaded_files:
                # Save uploaded file
                file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Check for .md existence and convert if needed
                md_file_path = os.path.join(MD_DIR, f"{os.path.splitext(uploaded_file.name)[0]}.md")
                if not os.path.exists(md_file_path):
                    st.info(f"Creating MD version for: {uploaded_file.name}")
                    convert_to_md(UPLOAD_DIR, MD_DIR)
                
                # Delete the original PDF after conversion
                os.remove(file_path)

            # Load documents
            st.info("Loading documents...")
            documents = load_docs(MD_DIR)

            # Split text into chunks
            st.info("Splitting documents into chunks...")
            chunks = split_text(documents)

            # Assign chunk IDs
            st.info("Assigning chunk IDs...")
            chunks = get_chunk_ids(chunks)

            # Add data to the database
            st.info("Adding data to the database...")
            add_data_to_db(chunks)

            st.success("All files processed and added to the database successfully!")

            # Completion message
            st.balloons()  # Optional: Adds a nice balloon animation
            st.success("Upload to DB is complete! 🎉")

            # Reset uploaded files after processing
            st.session_state.uploaded_files = []
            st.session_state.processing = False  # Reset processing state

st.write("Upload .pdf, .doc, or .md files to proceed.")
