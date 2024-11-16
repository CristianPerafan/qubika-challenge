from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def chunk_text(documents: list[Document]) -> list[Document]:
    """
    Chunk text of documents
    Args:
        documents (list[Document]): list of documents
    Returns:
        list[str]: list of chunks
    """

    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, # Size of each chunk in characters
        chunk_overlap=100, # Overlap between chunks in characters
        length_function=len, # Function to calculate the length of the text
        add_start_index=True, # Add start index to the chunks
    )

    chunks = text_splitter.split_documents(documents)

    return chunks