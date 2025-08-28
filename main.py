from app import app, settings
import uvicorn

if __name__ == '__main__':
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
