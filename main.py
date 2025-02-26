from fastapi import FastAPI, Response, status

from graph_production import produce_scatter
from request_body import RequestBody

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.put("/graph/get1d", status_code = 200)
async def get_graph(request: RequestBody, response: Response):
    match request.type:
        case "line_graph":
            linegraph = produce_scatter(request)
            return linegraph
        case _:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"Graph type not recognised."}