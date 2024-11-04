from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents import Document
import glob, os, pymupdf4llm, pathlib

DB_PATH = os.getenv(DB_PATH)

def convert_to_md(path:str, outDir: str):
    pdf_files = glob.glob(f'{path}/*.pdf', recursive=True)
    
    for pdf in pdf_files:
        md_text = pymupdf4llm.to_markdown(pdf)
        pathlib.Path(f'{outDir}/{os.path.splitext(os.path.basename(pdf))[0]}.md').write_bytes(md_text.encode())

def load_docs(path: str):
    loader = DirectoryLoader(path, glob='*.md')
    documents = loader.load()

    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True
    )

    chunks = text_splitter.split_documents(documents)
    print(f'Split {len(documents)} documents into {len(chunks)} chunks')

    return chunks

def get_chunk_ids(chunks: list[Document]):
    for chunk in chunks:
        source = chunk.metadata.get('source')
        chunk_idx = chunk.metadata.get('start_index')
        currp_id = f'{source}:{chunk_idx}'

        chunk.metadata['id'] = currp_id

    return chunks


def get_embedding_function():
    embeddings = OllamaEmbeddings(
        model='nomic-embed-text',
        base_url=os.getenv('OLLAMA_BASE_URL')
    )

    return embeddings

def add_data_to_db(chunks: list[Document]):
    db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=get_embedding_function()
    )

    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")


