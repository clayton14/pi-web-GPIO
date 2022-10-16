from fastapi  import FastAPI, HTTPException, APIRouter
import RPi.GPIO as GPIO
from pydantic import BaseModel
from typing import List
import pydantic
import uvicorn
import asyncio
import json, time

class Thing(BaseModel):
    name: str
    board_pin: int
    status: bool



app = FastAPI(title="Power Controll")
# app = APIRouter()
# gpioList = [2, 3, 4, 17, 27, 22, 10, 9]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# for i in gpioList:
   
#     GPIO.output(i, GPIO.HIGH)

thing_list = []


@app.get("/")
async def root():
    return {"Message":"Hi"}


# @app.get("/pin_test/{num}/{status}")
# async def avivate_pin(num: int, status: int):
#     try:
#         GPIO.setup(num, GPIO.OUT)
#         GPIO.output(num, status)
#         print(num)
#         return f"testing pin {num}"
#     except:
#          raise HTTPException(status_code=500, detail="Invalid rpi pin")



@app.post("/thing/")
async def create_thing(thing: Thing):
    try:
        thing_list.append(thing)
        return thing
    except:
        raise HTTPException(status_code=404, detail="No things created")


@app.get("/thing/", response_model=List[Thing])
async def get_all_things():
    return thing_list


@app.get("/thing/{id}")
async def get_thing(id: int):
    try:
        return thing_list[id]
    except:
        raise HTTPException(status_code=404, detail="Thing not found")


@app.put("/thing/{id}")
async def update_thing(id: int, thing: Thing):
    try:
        thing_list[id] = thing
        return thing_list[id]
    except:
        raise HTTPException(status_code=404, detail="Thing not found")


@app.delete("/thing/{id}")
async def delete_thing(id: int, thing: Thing):
    try:
        obj = thing_list.pop(id)
        return obj
    except:
        raise HTTPException(status_code=404, detail="Thing not found")


async def main():
    config = uvicorn.Config("server:app", port=8000, log_level="info", host="0.0.0.0", reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())