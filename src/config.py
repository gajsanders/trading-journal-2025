import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

class Config:
    """
    Central configuration for Trading Journal Analytics Tool.
    """
    
    @staticmethod
    def get_openai_api_key():
        return os.getenv("OPENAI_API_KEY", "")
        
    @staticmethod
    def get_log_level():
        return os.getenv("LOG_LEVEL", "INFO")
        
    @staticmethod
    def get_workspace_root():
        return os.getenv("WORKSPACE_ROOT")
    
    @classmethod
    def validate(cls) -> tuple[bool, str]:
        """
        Validates the configuration and returns (is_valid, error_message).
        """
        workspace_root = cls.get_workspace_root()
        if workspace_root is None or workspace_root.strip() == "":
            return False, "WORKSPACE_ROOT environment variable is not set. Please set it to the project root directory."
        
        workspace_path = Path(workspace_root)
        if not workspace_path.exists():
            return False, f"WORKSPACE_ROOT path '{workspace_root}' does not exist. Please set it to a valid directory."
            
        if not workspace_path.is_dir():
            return False, f"WORKSPACE_ROOT path '{workspace_root}' is not a directory. Please set it to a valid directory path."
            
        return True, ""

# Create a config instance for backward compatibility
config = Config() 