from fastapi import FastAPI, File, UploadFile
import pypandoc
import os
import shutil

app = FastAPI()

@app.post("/convert/")
async def convert_docx_to_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        return {"error": "Only .docx files are supported"}

    # Save the uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Convert to PDF using pypandoc
    try:
        output_file = temp_file_path.replace(".docx", ".pdf")
        pypandoc.convert_file(temp_file_path, 'pdf', outputfile=output_file)
        return {"message": "Conversion successful", "file": output_file}
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Clean up temp files
        os.remove(temp_file_path)
