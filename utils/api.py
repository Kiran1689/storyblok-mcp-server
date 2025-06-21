import json
from typing import Any, Dict, Optional
import httpx
from config import API_ENDPOINTS, Config

cfg = Config()

class APIError(Exception):
    """
    Custom exception for API errors, providing status code, details, and context.
    """
    def __init__(self, status_code: int, status_text: str, details: Any, context: Dict[str, Any]):
        """
        Initialize APIError.
        Args:
            status_code (int): HTTP status code.
            status_text (str): HTTP status text.
            details (Any): Error details from the response.
            context (Dict[str, Any]): Additional context for debugging.
        """
        super().__init__(f"{status_code} {status_text}: {details}")
        self.status_code = status_code
        self.details = details
        self.context = context

def _handle_response(response: httpx.Response, endpoint: str) -> Any:
    """
    Handle HTTPX response, raising APIError on error responses.
    Args:
        response (httpx.Response): The HTTPX response object.
        endpoint (str): The API endpoint called.
    Returns:
        Any: Parsed JSON response if successful.
    Raises:
        APIError: If the response indicates an error.
    """
    if response.is_error:
        try:
            error_details = response.json()
        except ValueError:
            error_details = response.text

        suggested_fix = "Unknown error, please check the details."
        if response.status_code == 401:
            suggested_fix = "Check if the API token is correct and has not expired."
        elif response.status_code == 403:
            suggested_fix = "Check token permissions."
        elif response.status_code == 404:
            suggested_fix = "Resource not found. Check endpoint and ID."
        elif response.status_code == 204:
            suggested_fix = "No content returned. This is not an error, but a valid response for some operations."

        context = {
            "endpoint": endpoint,
            "space_id": cfg.space_id,
            "suggested_fix": suggested_fix
        }
        raise APIError(response.status_code, response.reason_phrase, error_details, context)
    return response.json()

def get_management_headers() -> Dict[str, str]:
    """
    Build headers for Storyblok Management API requests.
    Returns:
        Dict[str, str]: Headers including Authorization and Content-Type.
    """
    return {
        "Authorization": cfg.management_token,
        "Content-Type": "application/json",
    }

def build_management_url(path: str) -> str:
    """
    Construct a full Management API URL for a given path.
    Args:
        path (str): The API path (e.g., '/stories').
    Returns:
        str: Full URL for the Management API endpoint.
    """
    return f"{API_ENDPOINTS['MANAGEMENT']}/spaces/{cfg.space_id}{path}"


def create_pagination_params(page: int = 1, per_page: int = 25) -> Dict[str, Any]:
    """
    Create pagination parameters for API requests.
    Args:
        page (int): Page number (default 1).
        per_page (int): Items per page (max 100, default 25).
    Returns:
        Dict[str, Any]: Pagination parameters.
    """
    return {"page": page, "per_page": min(per_page, 100)}

def add_optional_params(params: Dict[str, Any], options: Dict[str, Optional[Any]]) -> None:
    """
    Add optional parameters to a params dictionary if they are not None.
    Args:
        params (Dict[str, Any]): The base parameters dictionary to update.
        options (Dict[str, Optional[Any]]): Optional parameters to add if present.
    """
    for k, v in options.items():
        if v is not None:
            params[k] = v
