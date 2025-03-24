from fastapi import FastAPI, Response, status

from graph_production import generate_line_graph, generate_scatter_plot, generate_bar_chart
from request_body import RequestBodyOneDimensional, RequestBodyTwoDimensional

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.put("/graph/get1d", status_code = 200)
async def get_graph(request: RequestBodyOneDimensional, response: Response):
    match request.type:
        case "line_graph":
            linegraph = generate_line_graph(request)
            return linegraph
        case "bar_chart":
            bar_chart = generate_bar_chart(request)
            return bar_chart
        case _:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"Graph type not recognised."}

@app.put("/graph/get2d", status_code = 200)
async def get_graph(request: RequestBodyTwoDimensional, response: Response):
    match request.type:
        case "scatter_graph":
            scatter_graph = generate_scatter_plot(request)
            return scatter_graph
        case _:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"Graph type not recognised."}