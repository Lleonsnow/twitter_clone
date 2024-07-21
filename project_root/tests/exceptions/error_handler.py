from tests.test_schemas.pydantic_models import ErrorResponse


def error_handler(error: Exception) -> ErrorResponse:
    """Обработчик исключений."""
    error_type, error_message = error.__str__()
    return ErrorResponse(
        result=False, error_type=error_type, error_message=error_message
    )
