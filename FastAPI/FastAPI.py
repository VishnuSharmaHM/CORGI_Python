from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import FastAPI_Exec as F
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates=Jinja2Templates(directory='../HtmlDirectory')
app.mount('/static',StaticFiles(directory='../Static'),name="Static")

class Item(BaseModel):
    Privacy_level: int
    Precision_level: int
    Real_location: list[float]
    Target_location: list[int]

@app.get("/home/{user_name}",response_class=HTMLResponse)
def write_home(request:Request):
    return templates.TemplateResponse('TACO_UI.html',{'request':request})

@app.post("/submitform",response_class=HTMLResponse)
async def handle_form(request:Request,Address:str=Form(...),Precision_level:int=Form(...),Privacy_level:int=Form(...),
                      longitude:float=Form(...),latitude:float=Form(...)):
    # # templates.TemplateResponse('TACO_UI.html', {'request': request})
    print("Entered Address",Address)
    Item.Privacy_level=Privacy_level
    Item.Precision_level=Precision_level
    Item.Real_location=[latitude,longitude]
    Item.Target_location=[3]

    real_location_coordinates,lattitude,longitude,weight=F.Fast_API(Item)
    return templates.TemplateResponse('HeatMap.html', {'request': request,'Privacy_level': Privacy_level,"Precision_level":Precision_level,
                                                       'Real_location':real_location_coordinates,"tree_lattitude":lattitude,
                                                       "tree_longitude":longitude,"tree_weight":weight})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")