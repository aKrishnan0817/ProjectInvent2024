from typing import List
import os

def read_file_and_tokenize(file_path: str) -> List[str]:
    """
    Read a file and tokenize its contents into a list of strings.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        List of strings from the file
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            # Split by newlines and remove empty lines
            tokens = [line.strip() for line in content.split('\n') if line.strip()]
            return tokens
    except FileNotFoundError:
        print(f"Warning: File {file_path} not found")
        return []
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

def write_to_file(file_path: str, content: str) -> bool:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")
        return False

def get_file_path(relative_path: str) -> str:
    """
    Get the absolute path for a file relative to the project root.
    
    Args:
        relative_path: Path relative to project root
        
    Returns:
        Absolute path to the file
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, relative_path) 