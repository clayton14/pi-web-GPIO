from fastapi import Depends, FastAPI, HTTPException, Request
import RPi.GPIO as GPIO
from pydantic import BaseModel, Field
from typing import List
import uvicorn
import asyncio
from config.db import engine, SessionLocal
from sqlalchemy.orm import session
from thing import ThingModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


# TODO - mDNS responder config
# TODO - add on/off date and times for 'Things' (e.g light on every monday @ 6pm)
# TODO - create front end app
# TODO - voice activation client in JS

app = FastAPI(title="Power Controll")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# valid list of GPIO pins to use
GPIOs = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
         12, 13, 16, 17, 18, 19, 20, 21,
         22, 23, 24, 25, 26, 27]

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
    board_pin: int = Field(..., gt=1, lt=30)
    status: bool = False

#####################################API#####################################


@app.get("/")
async def root(req: Request, db: session = Depends(get_db)):
    # # responce = db.query(ThingModel).all()
    # return templates.TemplateResponse("index.html", {"request": req,
    #                                                  "x": db.query(ThingModel).all()}
    #                                   )
    return db.query(ThingModel).all()


# Template test
@app.get("/test/", response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/things/")
async def create_thing(thing: Thing, db: session = Depends(get_db)):
    """
    Creat a thing model and add to database
    """
    thing_model = ThingModel()
    thing_model.name = thing.name
    thing_model.board_pin = thing.board_pin
    thing_model.status = thing.status
    db.add(thing_model)
    db.commit()

    return thing


@app.put("/things/")
async def update_thing(id: int, thing: Thing, db: session = Depends(get_db)):
    thing_model = db.query(ThingModel).filter(
        ThingModel.thing_id == id).first()  # check to see if the item exisits
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


@app.put("/status/{id}/{status}")
async def update_status(id: int, status: bool, db:  session = Depends(get_db)):
    thing_model = db.query(ThingModel).filter(
        ThingModel.thing_id == id).first()  # check to see if the item exisits
    if thing_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {id}: Does not exist"
        )
    # turn on or off the pins in the rasbperry pi
    if (thing_model.thing_id == id):
        thing_model.status = int(status)
        GPIO.setup(thing_model.board_pin, GPIO.OUT)
        GPIO.output(thing_model.board_pin, not status)

    db.add(thing_model)
    db.commit()

    return status


@app.delete("/things/{id}")
async def delete_thing(id: int, db: session = Depends(get_db)):
    thing_model = db.query(ThingModel).filter(
        ThingModel.thing_id == id).first()  # check to see if the item exisits
    if thing_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {id}: Does not exist"
        )

    GPIO.setup(thing_model.board_pin, GPIO.OUT)
    GPIO.output(thing_model.board_pin, False)

    db.query(ThingModel).filter(ThingModel.thing_id == id).delete()
    db.commit()

    return f"{thing_model.name} has been deleted"


async def main():
    config = uvicorn.Config("server:app", port=8000,
                            log_level="info", host="0.0.0.0")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
