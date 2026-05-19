import asyncio
import uvicorn
from src.api import app, engine

async def main():
    # Start the execution engine loop as a concurrent background task
    engine_task = asyncio.create_task(engine.start())
    
    # Configure and run the API server
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    
    await server.serve()
    
    # Clean up background tasks upon web server exit
    await engine.stop()
    await engine_task

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nApplication terminated manually.")
