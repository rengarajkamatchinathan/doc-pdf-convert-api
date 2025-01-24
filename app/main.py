from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import pypandoc
import tempfile
import os

app = FastAPI()

@app.post("/convert/")
async def convert_docx_to_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, file.filename)

        # Save the uploaded file temporarily
        with open(temp_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Convert to PDF using pypandoc
        try:
            output_file = temp_file_path.replace(".docx", ".pdf")
            pypandoc.convert_file(temp_file_path, 'pdf', outputfile=output_file)

            # Return the PDF file as a response
            return FileResponse(output_file, media_type="application/pdf", filename=f"{file.filename.replace('.docx', '.pdf')}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
