from flask import Flask,request,Response
from botbuilder.core import BotFrameworkAdapter,BotFrameworkAdapterSettings,TurnContext,ConversationState,MemoryStorage
 
import asyncio
from pic_button import SampleAnimationCard

from aiohttp import web
from aiohttp.web import Request, Response, json_response

from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes


app = Flask(__name__)
loop = asyncio.get_event_loop()

botsettings = BotFrameworkAdapterSettings("053b477c-6f0b-4629-a12d-6bef846605ac","2da80739-ab3a-4fb1-8fa1-c4df64b087f2")
botadapter = BotFrameworkAdapter(botsettings)

CONMEMORY = ConversationState(MemoryStorage())
botdialog = SampleAnimationCard()

 

    

# Listen for incoming requests on /api/messages
async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    try:
        response = await botadapter.process_activity(activity, auth_header, botdialog.on_turn)
        if response:
            return json_response(data=response.body, status=response.status)
        return Response(status=201)
    except Exception as exception:
        raise exception


APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
