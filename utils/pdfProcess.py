from fastapi.responses import JSONResponse
from io import BytesIO

import pdfplumber

async def pdfProcesser(
    file, 
    debug: bool,
    step: int
):
    if(debug): 
        print('>--------> pdfProcess <--------<')
        print(f'Step   | {step}')
        step += 1

    try:
        pdf_file = BytesIO(await file.read())
        pdf_file.seek(0)

        with pdfplumber.open(pdf_file) as pdf:
            texto = ""
            for page in pdf.pages:
                texto += page.extract_text()

        
        print('corte --------------------------------')

        return texto
    
    except:
        print('Error at | pdfProcess.py / pdfProcesser()')
        raise Exception()