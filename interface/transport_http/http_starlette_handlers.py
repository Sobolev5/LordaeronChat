from src import methods


async def main(request):
    response = await methods.main(request)
    return response


async def check_socket_send(request):
    response = await methods.check_socket_send(request)
    return response    


async def check_carrot_call(request):
    response = await methods.check_carrot_call(request)
    return response    