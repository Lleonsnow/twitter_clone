from http import HTTPStatus

from fastapi import Depends, File, UploadFile
from sqlalchemy.orm import Session
from tests.conftest import app
from tests.exceptions.error_handler import error_handler
from tests.exceptions.models import ErrorMediaType
from tests.test_db.db import get_session
from tests.test_schemas.pydantic_models import ErrorResponse, MediaResponse
from tests.test_schemas.validators import validate_api_key
from tests.test_services.test_logic_media import save_media


@app.post("/medias", response_model=MediaResponse)
def create_like(
    file: UploadFile = File(...),
    _: str = Depends(validate_api_key),
    db: Session = Depends(get_session),
) -> MediaResponse | ErrorResponse:
    """Сохранение медиафайла в базу данных."""
    if file.content_type != "image/png":
        return error_handler(
            ErrorMediaType(
                message="Bad MediaType",
                status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            )
        )
    media_id = save_media(file.file, file.filename, db)
    return MediaResponse(result=True, media_id=media_id)


# @app.get("/{path:path}", response_class=FileResponse)
# def get_media_by_id(
#     path: str,
# ) -> MediaResponse | ErrorResponse:
#     """Получение медиафайла по местоположению в локальной папке."""
#
#     return FileResponse(path)
