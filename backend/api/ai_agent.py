from fastapi import APIRouter
from pydantic import BaseModel
import httpx
from backend.models.schemas.schemas import ScoreRequests, ScoreResponse

router = APIRouter(prefix="/api/ai", tags=["AI Agent"])


@router.post("/score", response_model=ScoreResponse)
async def get_score(req: ScoreRequests):
    try:
        async with httpx.AsyncClient() as client:
            # response = await  client.post("http://127.0.0.1:8080/score", json=req.dict())
            response = await client.post("http://host.docker.internal:8080/score", json=req.dict())

            response.raise_for_status()

            raw = response.json()
            score = raw.get("score", "Something went wrong. No score returned.")
            print(f"Score : {score}")
            return {"score": score}


    except httpx.HTTPError as e:
        return {"score": f"Something wrong with ai: {str(e)}"}
    except Exception as e:
        print(f"General error: {str(e)}")
        return {"score": f"Something wrong with ai: {str(e)}"}
