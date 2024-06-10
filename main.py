from fastapi import FastAPI

app= FastAPI()

# documentación:            $ https:127.0.0.1/docs
# para ejecutar el servidor $ uvicorn main:app --reload
# control - C para detener el servidor

@app.get("/")
async def root():
    return {"message":"Hello World"}

