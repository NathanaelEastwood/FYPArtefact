from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.graph_production import generate_line_graph, generate_bar_chart, generate_pie_chart, generate_scatter_plot
from app.request_body import RequestBodyOneDimensional, RequestBodyTwoDimensional

app = FastAPI()

# Add CORS middleware with more permissive settings for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]  # Expose all headers to the browser
)

@app.put("/graph/get1d", status_code = 200)
async def get_graph(request: RequestBodyOneDimensional, response: Response):
    match request.type:
        case "line_graph":
            success = generate_line_graph(request)
            if success:
                return FileResponse("example.svg", media_type="image/svg+xml")
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"error": "Failed to generate line graph"}
        case "bar_chart":
            success = generate_bar_chart(request)
            if success:
                return FileResponse("example.svg", media_type="image/svg+xml")
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"error": "Failed to generate bar chart"}
        case "pie_chart":
            success = generate_pie_chart(request)
            if success:
                return FileResponse("example.svg", media_type="image/svg+xml")
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"error": "Failed to generate pie chart"}
        case _:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": "Graph type not recognised"}

@app.put("/graph/get2d", status_code = 200)
async def get_graph(request: RequestBodyTwoDimensional, response: Response):
    match request.type:
        case "scatter_graph":
            success = generate_scatter_plot(request)
            if success:
                return FileResponse("example.svg", media_type="image/svg+xml")
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"error": "Failed to generate scatter plot"}
        case _:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": "Graph type not recognised"}