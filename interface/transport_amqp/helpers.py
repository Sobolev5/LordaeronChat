import orjson
import datetime
import aiormq.abc
from pydantic import ValidationError
from simple_print import sprint
from functools import wraps
from settings import DEBUG


def validate_schema(schema):
    def wrap(func):
        @wraps(func)
        async def wrapped(message: aiormq.abc.DeliveredMessage):
            await message.channel.basic_ack(message.delivery.delivery_tag)

            if DEBUG:
                sprint(f"{func.__name__} -> basic_ack [OK] {datetime.datetime.now().time()}", c="green", p=1)

            request = None
            response = None
            error = None

            try:
                request = orjson.loads(message.body)
                request = schema.validate(request).dict()
            except ValidationError as error_message:
                error = f"Validation Error. Body={message.body} error={error_message}"
            except Exception as error_message:
                error = f"Error. Body={message.body} error={error_message}"

            if not error:             
                try:
                    if DEBUG:
                        sprint(f"{func.__name__} -> Request {request}", c="green", p=1, i=4)                         
                    response = await func(request)
                except Exception as error_message:
                    error = f"Error response from function. Body={message.body} error={error_message}"

            if DEBUG:
                if error:
                    sprint(error, c="red", p=1, i=4)
                else:
                    sprint(f"{func.__name__} -> complete [OK]", c="green", p=1, i=4)
                    sprint(f"{func.__name__} -> response {response}", c="green", p=1, i=4)

            return response
        return wrapped
    return wrap