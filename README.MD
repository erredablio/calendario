# 📌 Guia da API - Calendário API

## 📢 Introdução
Esta API permite o gerenciamento de usuários e tarefas. Apenas **usuários administradores (`admin`)** podem gerenciar usuários, enquanto **usuários comuns (`common`)** têm permissões restritas.

## 🔹 Inicialização do Projeto  
Para rodar a API localmente, siga os passos:

### **1️⃣ Instalar dependências**
```bash
pip install -r requirements.txt
```
### **2️⃣ Configurar banco de dados**
```bash
flask db migrate
flask db upgrade
```
### **3️⃣ Rodar o servidor**
```bash
python3 app.py
```
Agora a API estará disponível em:
http://127.0.0.1:5000
🔐 Diferença entre usuários admin e common
Admin: Pode listar, criar e modificar usuários (incluindo role).
Common: Pode modificar apenas suas próprias informações e não pode alterar a role.
Tokens JWT: Ambos os tipos de usuários recebem tokens JWT, mas o role define os níveis de acesso.

## 📌 Endpoints da API

### **1️⃣ Registro de Usuário (POST /register)**
Cria um novo usuário com dados adicionais.

**POST /register**
```json
Headers: 
    Authorization: None
    Content-Type: application/json
Body:
{
    "username": "usuario_teste",
    "password": "senha_segura",
    "role": "common",
    "full_name": "Nome Completo",
    "gender": "male",
    "email": "usuario@email.com",
    "phone": "+55 99999-9999",
    "profile_picture": "https://example.com/foto.jpg"
}
```
#### ✅ Resposta de sucesso (201):
```json
{"msg": "Usuário registrado com sucesso"}
```
#### ❌ Usuário já existe (400):
```json
{"msg": "Usuário já existe"}
```
### **2️⃣ Login (POST /login)**
Autentica um usuário e gera um JWT.

**POST /login**
```json
Headers: 
    Authorization: None
    Content-Type: application/json
Body:
{
    "username": "usuario_teste",
    "password": "senha_segura"
}
```
#### **✅ Resposta de sucesso (200):**
```json
{
    "access_token": "eyJh...token_exemplo..."
}
```
#### **❌ Credenciais inválidas (401):**
```json
{"msg": "Credenciais inválidas"}
```
### **3️⃣ Listagem de Usuários (GET /users)**

**GET /users**
```json
Headers: 
    Authorization: Bearer SEU_TOKEN_ADMIN
```
#### **✅ Resposta de sucesso (200):**
```json
[
    {
        "id": "1234",
        "username": "admin_user",
        "role": "admin",
        "email": "admin@email.com",
        "active": true
    },
    {
        "id": "5678",
        "username": "user_common",
        "role": "common",
        "email": "user@email.com",
        "active": true
    }
]
```
#### **❌ Usuário sem permissão (403):**
```json
{"msg": "Acesso negado"}
```
### **4️⃣ Atualização de Usuário (PUT /users/<user_id>)**
🔹 Usuários comuns podem atualizar suas próprias informações. 🔹 Apenas admins podem alterar role.
**PUT /users/1234**
```json
Headers: 
    Authorization: Bearer SEU_TOKEN
    Content-Type: application/json
Body:
{
    "full_name": "Novo Nome",
    "email": "novo@email.com",
    "phone": "+55 99999-9999",
    "profile_picture": "https://example.com/foto.jpg",
    "password": "nova_senha"
}
```
#### **✅ Resposta de sucesso (200):**
```json
{"msg": "Usuário atualizado"}
```
#### **❌ Acesso negado (403):**
```json
{"msg": "Acesso negado"}
```
### **5️⃣ Desativar Usuário (PUT /users/<user_id>/deactivate)**
🔹 Apenas usuários admin podem desativar um usuário.
**PUT /users/1234/deactivate**
```json
Headers: 
    Authorization: Bearer SEU_TOKEN_ADMIN
```
**✅ Resposta de sucesso (200):**
```json
{"msg": "Usuário desativado"}
```
**❌ Usuário sem permissão (403):**
```json
{"msg": "Acesso negado"}
```
### **6️⃣ Criar Tarefa (POST /tasks)**
Cria uma nova tarefa associada ao usuário logado.
**POST /tasks**
```json
Headers: 
    Authorization: Bearer SEU_TOKEN
    Content-Type: application/json
Body:
{
    "event_date": "2025-05-24",
    "description": "Reunião de planejamento"
}
```
**✅ Resposta de sucesso (201):**
```json
{"msg": "Tarefa criada"}
```
### **7️⃣ Listar Tarefas (GET /tasks)**
🔹 Usuários podem visualizar apenas suas próprias tarefas.
**GET /tasks**
```json
Headers: 
    Authorization: Bearer SEU_TOKEN
```
#### **✅ Resposta de sucesso (200):**
```json
[
    {
        "id": "task_123",
        "event_date": "2025-05-24",
        "description": "Reunião de planejamento"
    }
]
```
### **8️⃣ Excluir Tarefa (DELETE /tasks/<task_id>)**
🔹 Usuários podem excluir apenas suas próprias tarefas.
**DELETE /tasks/task_123**
```json
Headers: 
    Authorization: Bearer SEU_TOKEN
```
#### **✅ Resposta de sucesso (200):**
```json
{"msg": "Tarefa excluída"}
```
## 🔐 Configuração do `.env`  

Para garantir segurança, a API utiliza um arquivo **`.env`** para armazenar **credenciais sensíveis** como JWT Secret Key.

### **1️⃣ Criar o arquivo `.env`**
No diretório raiz do projeto, crie um arquivo `.env`:
```ini
JWT_SECRET_KEY=super_seguro_token_aleatorio_12345
```
*Este guia, tal como todo o código do repositório, foram gerados pelo Copilot da Microsot 🚀*
