from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def get_root():
    return {"This is home route"}
