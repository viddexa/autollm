from collections import Counter
import hashlib
import logging
from pathlib import Path
from typing import Dict, Sequence, List, Tuple

from llama_index.schema import Document

from vectorstores.base import BaseVS

logger = logging.getLogger(__name__)


def get_md5(file_path: Path) -> str:
    """
    Compute the MD5 hash of a file.

    Parameters:
        file_path (Path): The path to the file.

    Returns:
        str: The MD5 hash of the file.
    """
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def check_for_changes(documents: Sequence[Document], vs: BaseVS) -> Tuple[Sequence[Document], List[str]]:
    """
    Check for file changes based on their hashes.

    Parameters:
        documents (Sequence[Document]): List of documents to check for changes.
        vs (BaseVS): The vector store to check for changes in.

    Returns:
        changed_documents (Sequence[Document]): List of documents that have changed.

        deleted_document_ids (List[str]): List of document ids that are deleted in local but present in vector store.
    """
    last_hashes, original_file_names, document_ids = vs.get_document_infos()
    deleted_document_ids = set(document_ids)
    
    changed_documents = []
    deleted_document_ids = []

    for doc in documents:
        file_path = str(Path(doc.metadata["original_file_path"]))
        current_hash = get_md5(Path(file_path))

        # Add
        if file_path not in original_file_names:
            changed_documents.append(doc)
        # Update
        elif current_hash not in last_hashes:
            changed_documents.append(doc)

        # remove from deleted set
        deleted_document_ids.remove(doc.id_)
        
    deleted_document_ids = list(deleted_document_ids)

    logger.info(f"Found {len(changed_documents)} changed documents.")
    logger.info(f"Found {len(deleted_document_ids)} locally deleted documents still present in vector store.")

    return changed_documents, deleted_document_ids
