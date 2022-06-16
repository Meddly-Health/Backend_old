import datetime
import json
import random
import string

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message


class LoggingMiddleware(BaseHTTPMiddleware):
    logs = []

    def __init__(self, app):
        super().__init__(app)

    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    async def dispatch(self, request, call_next):
        await self.set_body(request)
        try:
            json_body = await request.json()
        except json.decoder.JSONDecodeError:
            json_body = None

        log = {
            "request": {
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "method": request.method,
                "path": request.url.path,
                "query_string": request.url.query,
                "body": json_body,
                "IP": request.client.host,
            },
            "response": {},
        }

        exception = None
        try:
            response = await call_next(request)
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            log["response"]["status"] = response.status_code
            try:
                log["response"]["body"] = json.loads(response_body[0].decode())
            except json.decoder.JSONDecodeError:
                log["response"]["body"] = response_body[0].decode()
            return response
        except Exception as e:
            exception = e
            log["response"]["status"] = 500
            log["response"]["error"] = str(e)
            return JSONResponse(status_code=500, content={"error": str(e)})
        finally:
            if request.url.path not in ["/docs", "/openapi.json", "/test/logs"]:
                LoggingMiddleware.logs.append(log)
                if len(LoggingMiddleware.logs) > 150:
                    LoggingMiddleware.logs.pop(0)
            if exception is not None:
                raise exception
