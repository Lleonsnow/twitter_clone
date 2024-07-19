from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from project_root.tests.conftest import app
from project_root.tests.test_db.db import get_session
from project_root.tests.test_schemas.pydantic_models import BasicResponse
from project_root.tests.test_schemas.validators import validate_api_key
from project_root.tests.test_services.test_logic_like import set_user_like_to_db, set_user_unlike_to_db
from project_root.tests.exceptions.models import ModelException


@app.post("/tweets/{tweet_id}/likes", response_model=BasicResponse)
def create_like(tweet_id: int, _: str = Depends(validate_api_key),
                db: Session = Depends(get_session)) -> BasicResponse | ModelException:
    response = set_user_like_to_db(tweet_id, db)
    return JSONResponse(content=response.dict(), status_code=int(response.error_message)) \
        if response else BasicResponse(result=True, status_code=200)


@app.delete("/tweets/{tweet_id}/likes", response_model=BasicResponse)
def delete_like(tweet_id: int, _: str = Depends(validate_api_key),
                db: Session = Depends(get_session)) -> BasicResponse | ModelException:
    result = set_user_unlike_to_db(tweet_id, db)
    return JSONResponse(content=result.dict(), status_code=int(result.error_message)) \
        if result else BasicResponse(result=True, status_code=200)
