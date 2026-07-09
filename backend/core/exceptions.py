from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from backend.core.responses import ErrorResponse
from backend.core.logger import logger
import uuid

def add_exception_handlers(app: FastAPI):
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        req_id = request.state.request_id if hasattr(request.state, "request_id") else str(uuid.uuid4())
        logger.warning(f"Validation Error [req_id: {req_id}]: {exc.errors()}")
        
        error_resp = ErrorResponse(
            error_code="VALIDATION_ERROR",
            message="The provided input is invalid.",
            details=exc.errors(),
            request_id=req_id
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_resp.model_dump()
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        req_id = request.state.request_id if hasattr(request.state, "request_id") else str(uuid.uuid4())
        logger.error(f"Database Error [req_id: {req_id}]: {str(exc)}")
        
        error_resp = ErrorResponse(
            error_code="DATABASE_ERROR",
            message="An internal database error occurred.",
            request_id=req_id
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_resp.model_dump()
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        req_id = request.state.request_id if hasattr(request.state, "request_id") else str(uuid.uuid4())
        logger.critical(f"Unhandled Exception [req_id: {req_id}]: {str(exc)}")
        
        error_resp = ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred.",
            request_id=req_id
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_resp.model_dump()
        )
