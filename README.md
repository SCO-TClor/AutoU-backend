# 📧 AutoU Email Processor - Backend

API REST construída com FastAPI para processar e categorizar emails automaticamente usando IA (Google Gemini).

## 🚀 Funcionalidades

- **Processamento de múltiplos formatos**: PDF, TXT ou texto direto
- **Categorização inteligente**: Classifica emails como PRODUTIVO ou IMPRODUTIVO
- **Resposta automática**: Gera emails de resposta profissionais
- **API REST**: Comunicação via JSON com CORS configurado

## 📋 Pré-requisitos

- Python 3.10+
- Conta Google Cloud com API Gemini ativada

## 🔧 Instalação

1. **Clone o repositório e navegue até a pasta clonada**
```bash
cd backend # Exemplo
```

2. **Crie e ative o ambiente virtual**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto (pasta pai do backend):

```env
GEMINI_API_KEY=sua_chave_aqui
ALLOWED_ORIGIN=http://127.0.0.1:5501
```

> 💡 **Como obter a API Key do Gemini:**
> 1. Acesse [Google AI Studio](https://aistudio.google.com/app/apikey)
> 2. Crie uma nova API Key
> 3. Copie e cole no `.env`

## ▶️ Executando o servidor

```bash
uvicorn server:app --reload
```

O servidor estará disponível em: `http://127.0.0.1:8000`

## 📡 Endpoints

### POST `/email-process`

Processa um email e retorna a categoria + resposta gerada pela IA.

**Parâmetros (form-data):**
- `text` (opcional): Texto do email como string
- `file` (opcional): Arquivo PDF ou TXT

**Exemplo de resposta:**
```json
{
  "status": "success",
  "code": "200",
  "message": "Success | AI response successfully!",
  "data": {
    "category": "PRODUTIVO",
    "email": "Prezado(a),\n\nAgradecemos seu contato..."
  }
}
```

## 📂 Estrutura do Projeto

```
backend/
├── server.py           # Servidor FastAPI e rotas
├── router.py           # Roteamento de processamento
├── requirements.txt    # Dependências Python
├── services/
│   └── ReaderAI.py    # Integração com Gemini AI
└── utils/
    ├── pdfProcess.py  # Processador de PDFs
    └── txtProcess.py  # Processador de TXT
```

## 🧪 Testando a API

### Com cURL (texto):
```bash
curl -X POST http://127.0.0.1:8000/email-process \
  -F "text=Preciso de suporte técnico urgente"
```

### Com cURL (arquivo):
```bash
curl -X POST http://127.0.0.1:8000/email-process \
  -F "file=@email.pdf"
```

### Com Postman:
1. Método: `POST`
2. URL: `http://127.0.0.1:8000/email-process`
3. Body → form-data
4. Adicione `text` ou `file`

## 🛠️ Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **Google Gemini AI**: Modelo de linguagem para análise e geração de texto
- **pdfplumber**: Extração de texto de PDFs
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 🐛 Troubleshooting

**Erro: "GEMINI_API_KEY not found"**
- Verifique se o arquivo `.env` está na raiz do projeto
- Confirme que a chave está sem aspas

**Erro: CORS blocked**
- Ajuste `ALLOWED_ORIGIN` no `.env` para a URL do seu frontend
- Adicione mais origens em `server.py` se necessário

**Erro: Module not found**
- Execute `pip install -r requirements.txt` novamente
- Certifique-se de que o ambiente virtual está ativado

## 📝 Licença

Este projeto foi desenvolvido como desafio técnico para a AutoU.