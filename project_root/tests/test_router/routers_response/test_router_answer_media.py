from fastapi import Depends, UploadFile, File
from http import HTTPStatus
from sqlalchemy.orm import Session
from project_root.tests.conftest import app
from project_root.tests.test_db.db import get_session
from project_root.tests.test_schemas.pydantic_models import MediaResponse
from project_root.tests.test_schemas.validators import validate_api_key
from project_root.tests.test_services.test_logic_media import save_media
from project_root.tests.exceptions.error_handler import error_handler
from project_root.tests.exceptions.models import ErrorMediaType
from project_root.tests.test_schemas.pydantic_models import ErrorResponse


@app.post("/medias", response_model=MediaResponse)
def create_like(file: UploadFile = File(...), _: str = Depends(validate_api_key),
                db: Session = Depends(get_session)) -> MediaResponse | ErrorResponse:
    if file.content_type != "image/png":
        return error_handler(ErrorMediaType(message="Bad MediaType", status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE))
    media_id = save_media(file.file, file.filename, db)
    return MediaResponse(result=True, media_id=media_id)
