from fastapi import APIRouter, UploadFile, File

import pandas as pd

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/excel")
async def upload_excel(
    file: UploadFile = File(...)
):

    df = pd.read_excel(
        file.file
    )

    return {
        "success": True,
        "rows": len(df),
        "columns": list(df.columns)
    }