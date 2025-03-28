from google.cloud import documentai_v1 as documentai
import os
from dotenv import load_dotenv
from typing import Union, BinaryIO, Any
import io


load_dotenv()

project_id = os.getenv("gcp_project_id")
location = os.getenv("gcp_location")
processor_id = os.getenv("gcp_processor_id")    

client = documentai.DocumentProcessorServiceClient()
name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

def extract_text_from_image(file_input: Union[str, bytes, BinaryIO, Any]) -> str:
    """
    Extract text from an image using Google Document AI.
    
    Args:
        file_input: Can be one of:
            - A file path (str)
            - Bytes object containing the file data
            - A file-like object (has read() method)
            - A framework-specific file upload object
    
    Returns:
        Extracted text from the image
    """
    # Handle different input types
    if isinstance(file_input, str):
        # Assume it's a file path
        with open(file_input, "rb") as f:
            file_content = f.read()
    elif isinstance(file_input, bytes):
        # Raw bytes
        file_content = file_input
    elif hasattr(file_input, 'read'):
        # File-like object
        file_content = file_input.read()
        # If read() returns a string instead of bytes, encode it
        if isinstance(file_content, str):
            file_content = file_content.encode('utf-8')
    elif hasattr(file_input, 'file'):
        # Framework file upload object (like Flask's FileStorage)
        file_content = file_input.file.read()
    elif hasattr(file_input, 'filename') and hasattr(file_input, 'stream'):
        # Another common pattern in web frameworks
        file_content = file_input.stream.read()
    else:
        # Try a generic approach for framework-specific file objects
        try:
            # Try to get raw bytes from the object in some way
            if hasattr(file_input, 'body'):
                file_content = file_input.body
            elif hasattr(file_input, 'value'):
                file_content = file_input.value
            else:
                file_content = bytes(file_input)
        except:
            raise ValueError("Unsupported file input type. Please provide a file path, bytes, or file-like object.")

    # Process with Document AI
    raw_document = documentai.RawDocument(content=file_content, mime_type="image/png")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    return result.document.text

