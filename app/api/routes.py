from fastapi import APIRouter, HTTPException
from app.agents.orchestrator import AgentOrchestrator
from app.schemas.requests import LayoutRequest, ThemeRequest, WorkflowRequest

router = APIRouter(prefix="/api/v1", tags=["PhotoTheme local mock"])
orchestrator = AgentOrchestrator()

@router.get("/health")
def health() -> dict:
    return {"status": "ok", "mode": "local-mock", "agents": orchestrator.available_agents()}

@router.post("/recommend-layout")
def recommend_layout(request: LayoutRequest) -> dict:
    try:
        return orchestrator.run("layout_recommendation", request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.post("/recommend-theme")
def recommend_theme(request: ThemeRequest) -> dict:
    try:
        return orchestrator.run("theme_recommendation", request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.post("/workflow")
def workflow(request: WorkflowRequest) -> dict:
    try:
        return orchestrator.run("creative_workflow", request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.get("/catalog/themes")
def themes() -> list[dict]:
    return orchestrator.catalog.themes

@router.get("/catalog/layouts")
def layouts() -> list[dict]:
    return orchestrator.catalog.layouts
