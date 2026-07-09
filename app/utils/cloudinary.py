import os
from pathlib import Path

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


def upload_txt_file(file_path: str, folder: str = "agent_docs") -> str:
    try:
        # Convert string to Path object to verify extension
        path = Path(file_path)
        
        result = cloudinary.uploader.upload(
            str(path.resolve()),
            resource_type="raw",      # Required for non-media text files
            folder=folder,
            use_filename=True,        # Retains the file extension (.txt)
            unique_filename=True,     # Prevents overwriting duplicate names
        )
        return result["secure_url"]
    except Exception as e:
        print(f"Cloudinary Upload Error Details: {str(e)}") # Force log the actual API error
        raise e
    finally:
        # DO NOT unlink here if you need to use state["file_path"] later in your graph
        path = Path(file_path)
        if path.exists():
            path.unlink()
        pass 
