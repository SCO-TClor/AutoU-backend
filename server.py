from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Modularização:
from backend.router import routerPy
from backend.services.ReaderAI import AI_reader

# Autorização:
import os
from dotenv import load_dotenv

load_dotenv()

print('hello world')

app = FastAPI()
debug = True

allowed = os.getenv("ALLOWED_ORIGIN") or ''

app.add_middleware(
    CORSMiddleware,
    allow_origins=[allowed],
    allow_credentials= True,
    allow_methods=['POST', 'OPTIONS'], # CORS precisa de options? Idk
    allow_headers=['*']
)

# debugger:
def serverDebugger(
        request: Request,
        step: int
):
    print(f'Step    | {step}')
    print(f'Route   | {request.url.path}')
    print(f'Method  | {request.method}')
    return

# Rota padrão:
@app.post("/email-process")
async def main(
        request: Request,
        text: str = Form(None),         # string
        file: UploadFile = File(None)   # TXT ou PDF
):
    # Hierarquia:
            # PDF > TXT > String

    # Debug inicial rápido:
    step = 1
    if(debug): 
        print('>---------<> Server <>---------<')
        serverDebugger(request, step)
    if(debug and text): print(f'text    | {text}')
    if(debug and file): print(f'pdf     | {file.filename}')
    step += 1
    
    try:
        
        if(not(text or file)):
            raise Exception('4001 | text or file are required')

        response = await routerPy(text, file, debug, step)

        if(response is None):
            raise Exception('4001 | response is None')
        else:
            print(response)

            category, email, raw = AI_reader(response, debug, step)

        print('server.py')
        if(category and email):
            if(debug):
                print(f'Categoria | {category}')
                print(f'Email     | {email}')
            
            return JSONResponse(status_code=200, content={
                "status": "success",
                "code": "OK_200_1",
                "message": "Success | AI response successfully!",
                "data": {
                    "category": category,
                    "email": email
                }
            })
        elif(raw):
            return JSONResponse(status_code=200, content={
                "status": "success",
                "code": "OK_200_2",
                "message": "Success | wrong filename!",
                "data": raw
            })
        else:
            raise Exception('AI response Error')
    
    except Exception as e:
        # Trate Exception aqui
        ErrorStr = str(e)

        if("|" in ErrorStr):
            code, msm = ErrorStr.split("|")
            code = int(code.strip())

            match code:
                case 400:
                    return JSONResponse(status_code=400, content={
                        "status": "error",
                        "code": f"{code}",
                        "message": "BadRequest | wrong filename!",
                        "data": "null"
                    })
                case 4001:
                    return JSONResponse(status_code=400, content={
                        "status": "error",
                        "code": f"{code}",
                        "message": f"BadRequest | {msm}!",
                        "data": "null"
                    })
                case 422:
                    return JSONResponse(status_code=422, content={
                        "status": "error",
                        "code": "422",
                        "message": "Enconding diferente do padrão UTF-8",
                        "data": "null"
                    })
                case 5001:
                    return JSONResponse(status_code=500, content={
                        "status": "error",
                        "code": f"{code}",
                        "message": f"InternalServerError | {msm}!",
                        "data": "null"
                    })

            
        else:
            return JSONResponse(status_code=500, content={
            "status": "error",
            "code": "500",
            "message": "InternalServerError",
            "data": "null"
        })