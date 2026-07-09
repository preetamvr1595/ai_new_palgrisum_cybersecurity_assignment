import uuid
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from backend.core.logger import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate Request ID
        request_id = str(uuid.uuid4())
        
        # Attach to request state so downstream functions can use it
        request.state.request_id = request_id
        
        # Log incoming
        start_time = time.time()
        logger.info(f"Incoming Request: {request.method} {request.url.path} [req_id: {request_id}]")
        
        try:
            response = await call_next(request)
            
            # Add request ID to response header
            response.headers["X-Request-ID"] = request_id
            
            process_time = time.time() - start_time
            logger.info(
                f"Completed Request: {request.method} {request.url.path} "
                f"- Status: {response.status_code} "
                f"- Time: {process_time:.4f}s [req_id: {request_id}]"
            )
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Failed Request: {request.method} {request.url.path} "
                f"- Time: {process_time:.4f}s [req_id: {request_id}] - Error: {str(e)}"
            )
            # Re-raise to let the global exception handler catch it
            raise e
