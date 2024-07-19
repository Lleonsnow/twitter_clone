from fastapi import Depends
from sqlalchemy.orm import Session
from project_root.tests.conftest import app
from project_root.tests.test_schemas.pydantic_models import UserSchema, BasicResponse
from project_root.tests.test_db.db import get_session
from project_root.tests.test_services.test_logic_user import create_user_to_db, get_user_by_id
from project_root.tests.test_db.base_models import User
from project_root.tests.test_schemas.validators import validate_api_key


@app.post("/user/me", response_model=BasicResponse)
def route_create_user(_: str = Depends(validate_api_key), db: Session = Depends(get_session)) -> BasicResponse:
    create_user_to_db(db)
    return BasicResponse(result=True, status_code=200)


@app.get("/user/{user_id}", response_model=UserSchema)
def route_get_user_by_id(user_id: int, _: str = Depends(validate_api_key), db: Session = Depends(get_session)) -> User:
    user = get_user_by_id(user_id, db)
    return user
