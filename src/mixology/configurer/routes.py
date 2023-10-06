from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from mixology.services.tasmota import AnonymousTasmotaBBDDService
from mixology.services.temporary_token import TemporaryTokenService
from mixology.settings import Settings

router = APIRouter()


@router.get("/app_settings")
async def return_settings(
    code: str,
    bbdd_service=Depends(AnonymousTasmotaBBDDService()),
    ttoken_service=Depends(TemporaryTokenService()),
):
    resp = await ttoken_service.get_token(code)
    tasmotas = await bbdd_service.get_tasmotas(
        key=resp["key"], token=resp["token"]
    )
    resp["api_url"] = Settings.public_url
    resp["wifis"] = ",".join({a.wifi for a in tasmotas})
    return resp


@router.get("/", response_class=HTMLResponse)
async def return_index(
    key: str,
    token: str,
    ttoken_service=Depends(TemporaryTokenService()),
):
    code = await ttoken_service.set_token(key, token)
    return (
        (Path(__file__).parent / "index.html")
        .read_text()
        .replace("{code}", code)
    )
