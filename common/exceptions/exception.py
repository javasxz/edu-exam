from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

def handler(exc, context):
    """
    Custom exception handler.
    - Handles nested field errors in ValidationError
    - Deduplicates repeated error messages
    - Normalizes token exceptions
    """

    errors = []
    response = exception_handler(exc, context)

    if response is None:
        return response

    if isinstance(response.data, list):
        response.data = {"detail": response.data}

    if isinstance(response.data.get("detail"), list):
        message = " ".join(response.data.get("detail"))
    else:
        message = response.data.get("detail")

    # ValidationError case (handle nested fields)
    if isinstance(exc, ValidationError):

        def flatten_errors(error_dict, parent_key=""):
            """Recursively flatten nested error dicts/lists into field + message pairs."""
            flat = []
            if isinstance(error_dict, dict):
                for field, value in error_dict.items():
                    full_key = f"{parent_key}.{field}" if parent_key else field
                    flat.extend(flatten_errors(value, full_key))
            elif isinstance(error_dict, list):
                for idx, value in enumerate(error_dict):
                    if isinstance(value, (dict, list)):
                        full_key = f"{parent_key}[{idx}]"
                        flat.extend(flatten_errors(value, full_key))
                    else:
                        flat.append({"field": parent_key, "detail": str(value)})
            else:
                flat.append({"field": parent_key, "detail": str(error_dict)})
            return flat

        errors = flatten_errors(response.data)

        # Collect unique messages only
        unique_messages = list({err["detail"] for err in errors})

        # If all messages are the same, just use one
        if len(unique_messages) == 1:
            message = unique_messages[0]
        else:
            message = "\n".join(unique_messages)

    # Token exception (403 forbidden)
    if response.status_code == 403:
        try:
            message = response.data.get("messages")[0].get("message")
            errors.append(
                {
                    "field": "token",
                    "detail": message
                }
            )
        except Exception:
            pass

    response.data["detail"] = message
    response.data["errors"] = errors

    return response
