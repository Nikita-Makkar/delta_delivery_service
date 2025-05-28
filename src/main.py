import uvicorn


def run_api() -> None:
    """
    Runs FastAPI application with Uvicorn server.
    """
    uvicorn.run(
        "delivery_service.entrypoints.fastapi:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    run_api()
