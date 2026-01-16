import os
from dotenv import load_dotenv

import google.genai as genai
from google.genai import types

import re

# Transformers classificador:

def AI_reader(
        content: str,
        debug: bool,
        step: int
):
    if(debug): 
        print('>---------> ReaderAI <---------<')
        print(f'Step | {step}')
        print(f'len  | {len(content)}')
        step += 1
    
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print('api_key não encontrada no .env!!')
        raise Exception('API key not found')

    try:
        client = genai.Client(api_key=api_key)

        gemini_prompt = f'''
        Você trabalha no setor de uma grande empresa chamada AutoU que precisa lidar com um grande volume de emails diariamente.
        Esses emails tem que ser categorizados em [produtivos] e [improdutivos].

        - Produtivo: Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
        - Improdutivo: Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).
        
        Sua tarefa é escrever categorizar o email em PRODUTIVO e IMPRODUTIVO (apenas duas opções), e um email de resposta sobre o nome da AutoU mantendo a profissionalidade e padrões claros independente da categoria selecionada

        Responda EXATAMENTE neste formato (com $ após o final do email):
        -CATEGORIA: [PRODUTIVO ou IMPRODUTIVO]
        -EMAIL: [email de resposta aqui]$

        ---------------
        EMAIL RECEBIDO:
        {content}
        ---------------
        '''

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=gemini_prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=400
            )
        )

        if(response.text == None):
            raise Exception('AI response failed')
        
        answer = response.text.strip()
        
        regex_category = r'^-CATEGORIA: *(PRODUTIVO|IMPRODUTIVO) *$'
        regex_email = r'-EMAIL: *((?:.*[^$])*)'

        category = re.search(regex_category, answer, re.MULTILINE)
        email = re.search(regex_email, answer)

        categoria = category.group(1) if category else None
        resposta = email.group(1) if email else None

        if(not (categoria and resposta)):
            raise Exception('Error at AI response')
        

        return (categoria, resposta, answer)
    
    except Exception as e:
        if(debug):
            print(f'----Gemini error: {str(e)}')
        raise Exception('5001 | AI processing failed')