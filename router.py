from fastapi import UploadFile

from backend.utils.pdfProcess import pdfProcesser
from backend.utils.txtProcess import textProcesser

async def routerPy(
        text: str | None,
        file: UploadFile | None,
        debug: bool,
        step: int
):
    if(debug): 
        print('>----------> router <----------<')
        print(f'Step    | {step}')
        step += 1
    
    texto = text or ""

    # Processar informações:
    if(file):
        if(not file.filename):
            raise Exception('400 |filename')
        
        arquivo = file.filename.lower()

        # Caso seja PDF:
        if(arquivo.endswith('.pdf')):
            texto = await pdfProcesser(file, debug, step)
            return texto
        # Caso seja TXT:
        elif(arquivo.endswith('.txt')):
            texto = await textProcesser(file, texto, debug, step)
            return texto
        else:
            raise Exception('400 |')
    else:
        return texto
        