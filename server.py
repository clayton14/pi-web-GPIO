import imp
from fastapi  import Depends, FastAPI, HTTPException, APIRouter
import RPi.GPIO as GPIO
from pydantic import BaseModel, Field
from typing import List
import pydantic
import uvicorn
import asyncio
from config.db import engine, SessionLocal
from sqlalchemy.orm import session
from thing import ThingModel
app = FastAPI(title="Power Controll")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

ThingModel.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    except:
        print("[ERROR] DB Shat")
    finally:
        db.close()


class Thing(BaseModel):
    name: str
    board_pin: int = Field(..., gt=1, lt=40)
    status: bool = False



#using depedency injection
@app.get("/")
async def root(db: session = Depends(get_db)):
    return db.query(ThingModel).all()


@app.post("/")
async def create_thing(thing: Thing, db: session = Depends(get_db)):
    """
    Creat a thing model and add to database
    """
    thing_model = ThingModel
    thing_model.name = thing.name
    thing_model.board_pin = thing.board_pin
    thing_model.status = thing.status
    db.add(thing_model)
    db.commit()

    return thing


@app.put("/")
async def update_thing(id: int, thing: Thing, db: session = Depends(get_db)):
    thing_model = db.query(ThingModel).filter(ThingModel.thing_id == id).first()
    if thing_model is None:
        raise HTTPException(
            status_code=404, 
            detail="Thing not found"
        )
    thing_model.name = thing.name
    thing_model.board_pin = thing.board_pin
    thing_model.status = thing.status
    db.add(thing_model)
    db.commit()
    return thing



# @app.delete("/")
# async def delete_thing(id: int, thing: Thing):
#     try:
#         obj = thing_list.pop(id)
#         return obj
#     except:
#         raise HTTPException(status_code=404, detail="Thing not found")


@app.get("/pin_test/{num}/{status}")
async def avivate_pin(num: int, status: int):
    try:
        GPIO.setup(num, GPIO.OUT)
        GPIO.output(num, status)
        print(num)
        return f"testing pin {num}"
    except:
         raise HTTPException(status_code=500, detail="Invalid rpi pin")




async def main():
    config = uvicorn.Config("server:app", port=8000, log_level="info", host="0.0.0.0", reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())