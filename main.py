from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from scraper.google_maps.google_maps import scrape_google_maps


app = FastAPI()

@app.post("/")
async def post(req: dict):
    try:
        google_maps_url = req.get("googleMapsUrl")
        print(google_maps_url)

        results = await scrape_google_maps(google_maps_url)

        return JSONResponse(content=results)

    except Exception as e:
        print('Error occurred:', e)
        raise HTTPException(status_code=500, detail="Internal server error")
