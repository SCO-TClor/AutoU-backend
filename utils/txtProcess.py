from fastapi.responses import JSONResponse

async def textProcesser(
    file, 
    texto: str, 
    debug: bool,
    step: int
):
    if(debug): 
        print('>--------> txtProcess <--------<')
        print(f'Step   | {step}')
        step += 1

    texto = ""

    try:
        content = await file.read()
        
        texto += '\n' + content.decode('utf-8')

        return texto
    
    except:
        raise Exception('422 | Enconding Error')