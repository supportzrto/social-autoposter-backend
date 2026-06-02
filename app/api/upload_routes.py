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

    preview = (
        df.head(10)
        .fillna("")
        .to_dict(orient="records")
    )

    return {
        "success": True,
        "rows": len(df),
        "columns": list(df.columns),
        "preview": preview
    }