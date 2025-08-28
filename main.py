from app import app, settings
import uvicorn

if __name__ == '__main__':
    uvicorn.run(app, port=settings.PORT)
