import datetime
import json
import random
import string

import starlette.responses
from fastapi import Request
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message
from fastapi.responses import JSONResponse


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
                "IP": request.client.host
            },
            "response": {
            }
        }

        exception = None
        try:
            response = await call_next(request)
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            log["response"]['status'] = response.status_code
            try:
                log["response"]['body'] = json.loads(response_body[0].decode())
            except json.decoder.JSONDecodeError:
                log["response"]['body'] = response_body[0].decode()
            return response
        except Exception as e:
            exception = e
            log["response"]['status'] = 500
            log["response"]['error'] = str(e)
            return JSONResponse(status_code=500, content={"error": str(e)})
        finally:
            if request.url.path not in ["/docs", "/openapi.json", "/test/logs"]:
                LoggingMiddleware.logs.append(log)
                if len(LoggingMiddleware.logs) > 150:
                    LoggingMiddleware.logs.pop(0)
            if exception is not None:
                raise exception


async def generate_code(db):
    """
    Generates a 10-character code and checks that it does not exist in the database
    """

    async def generate():
        generated_code = []
        for k in [3, 4, 3]:
            generated_code.append("".join(random.choices(string.ascii_uppercase, k=k)))
        generated_code = "-".join(generated_code).upper()
        return generated_code

    async def is_repeated(code_to_check):
        code_is_repeated = await db["user"].find_one({"invitation": code_to_check})
        return code_is_repeated is not None

    code = await generate()
    while await is_repeated(code):
        code = await generate()

    return code
