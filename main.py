from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from scraper.methods.google_maps import scrape_google_maps
from scraper.methods.jobs_scrapper import scrape_jobs


app = FastAPI()

@app.post("/gmaps-scrapper")
async def googleMapsUrl(req: dict):
    try:
        google_maps_url = req.get("googleMapsUrl")
        results = await scrape_google_maps(google_maps_url)
        return JSONResponse(content=results)
    except Exception as e:
        print('Error occurred:', e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/jobs")
async def jobs():
    links = await scrape_jobs()
    return JSONResponse(content=links)

