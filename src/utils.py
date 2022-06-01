import random
import string


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
