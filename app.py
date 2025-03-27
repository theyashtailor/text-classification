from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import requests
from io import BytesIO

app = FastAPI()

def download_file_from_google_drive(file_id: str, token: str):
    """
    Downloads a file from Google Drive using the file ID and an authorization token.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to download file from Google Drive.")
    return BytesIO(response.content)

@app.get("/download/{file_id}")
async def download(file_id: str, token: str):
    """
    Endpoint to download a file from Google Drive given its file ID and an authorization token.
    """
    file_stream = download_file_from_google_drive(file_id, token)
    return StreamingResponse(file_stream, media_type='application/octet-stream', headers={"Content-Disposition": f"attachment; filename={file_id}"})
