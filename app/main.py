from fastapi import FastAPI, UploadFile, File, HTTPException
import subprocess
import tempfile
import os
from io import BytesIO
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/convert/")
async def convert_docx_to_pdf(file: UploadFile = File(...)):
    try:
        # Create a temporary file to store the uploaded .docx
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
            content = await file.read()
            tmp_docx.write(content)
            tmp_docx.close()

            # Generate the output PDF path
            tmp_pdf = tmp_docx.name.replace(".docx", ".pdf")

            # Use Pandoc to convert .docx to PDF using LaTeX
            result = subprocess.run(
                ["pandoc", tmp_docx.name, "-o", tmp_pdf, "--pdf-engine=xelatex"],
                capture_output=True,
                text=True
            )

            # Check for errors in the Pandoc conversion
            if result.returncode != 0:
                raise HTTPException(status_code=500, detail=f"Pandoc conversion failed: {result.stderr}")

            # Open the generated PDF file
            with open(tmp_pdf, "rb") as f:
                pdf_content = f.read()

            # Clean up temporary files
            os.remove(tmp_docx.name)
            os.remove(tmp_pdf)

            # Return the PDF as a streaming response
            return StreamingResponse(BytesIO(pdf_content), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=converted.pdf"})

    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}
