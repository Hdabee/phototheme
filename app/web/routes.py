import logging
import uuid
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.agents.orchestrator import AgentOrchestrator
from app.editor.session_store import session_store
from app.renderer.collage_renderer import render_collage
from app.services.storage_service import OUTPUTS_DIR, UPLOADS_DIR, safe_image_upload

logger = logging.getLogger("phototheme")
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
orchestrator = AgentOrchestrator()


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"title": "PhotoTheme Atelier"})


@router.post("/web/upload")
async def upload(files: list[UploadFile] = File(...)):
    try:
        if not 1 <= len(files) <= 9:
            raise HTTPException(status_code=400, detail="Selectionnez entre 1 et 9 photos.")
        session_id = uuid.uuid4().hex
        paths = [
            await safe_image_upload(item, UPLOADS_DIR / f"{session_id}_{index}")
            for index, item in enumerate(files)
        ]
        states = session_store.create(session_id, paths)
        return {
            "session_id": session_id,
            "photos": [state.to_dict() for state in states],
            "story": session_store.get_story(session_id).to_dict(),
        }
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Erreur upload")
        return JSONResponse(status_code=500, content={"detail": f"Erreur serveur upload: {type(exc).__name__}: {exc}"})


@router.post("/web/photo/{session_id}/{photo_id}")
def update_photo(session_id: str, photo_id: str, update: dict):
    try:
        return session_store.update(session_id, photo_id, update).to_dict()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Erreur edition photo")
        return JSONResponse(status_code=500, content={"detail": f"Erreur serveur edition: {type(exc).__name__}: {exc}"})


@router.post("/web/story/{session_id}")
def update_story(session_id: str, update: dict):
    try:
        return session_store.update_story(session_id, update).to_dict()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Erreur histoire")
        return JSONResponse(status_code=500, content={"detail": f"Erreur serveur histoire: {type(exc).__name__}: {exc}"})


@router.post("/web/split-three/{session_id}/{photo_id}")
def split_three(session_id: str, photo_id: str):
    try:
        session_store.split_three_vertical(session_id, photo_id)
        return {
            "photos": [state.to_dict() for state in session_store.get(session_id)],
            "story": session_store.get_story(session_id).to_dict(),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Erreur decoupage")
        return JSONResponse(status_code=500, content={"detail": f"Erreur serveur decoupage: {type(exc).__name__}: {exc}"})


@router.post("/web/create")
def create_collage(
    session_id: str = Form(...),
    layout_id: str = Form(...),
    theme_id: str = Form(...),
):
    try:
        layout = next((item for item in orchestrator.catalog.layouts if item["id"] == layout_id), None)
        theme = next((item for item in orchestrator.catalog.themes if item["id"] == theme_id), None)
        if not layout or not theme:
            raise HTTPException(status_code=400, detail="Layout ou theme inconnu.")

        states = session_store.get(session_id)
        story = session_store.get_story(session_id)
        if layout["photo_count"] != len(states):
            raise HTTPException(
                status_code=400,
                detail=f"Le layout {layout['name']} attend {layout['photo_count']} images, mais la session en contient {len(states)}.",
            )

        output = OUTPUTS_DIR / f"collage_{uuid.uuid4().hex}.png"
        render_collage(states, layout, theme, output, story=story)
        return JSONResponse(status_code=200, content={"status": "ok", "image_url": f"/outputs/{output.name}"})
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Erreur creation collage")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Erreur serveur de rendu: {type(exc).__name__}: {exc}"},
        )
