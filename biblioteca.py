import streamlit as st
from groq import Groq
import json

if "usuarios" not in st.session_state:
    st.session_state["usuarios"] = {}

if "catalogo_livros" not in st.session_state:
    st.session_state["catalogo_livros"] = [
        {"titulo": "Fundacao", "autor": "Isaac Asimov", "tema": "Ficcao Cientifica", "status": "Disponivel"},
        {"titulo": "Duna", "autor": "Frank Herbert", "tema": "Ficcao Cientifica", "status": "Disponivel"},
        {"titulo": "Neuromancer", "autor": "William Gibson", "tema": "Ficcao Cientifica", "status": "Disponivel"},
    ]

# Banco simulado
catalogo_livros = [
    {"titulo": "Fundacao", "autor": "Isaac Asimov", "tema": "Ficcao Cientifica", "status": "Disponivel"},
    {"titulo": "Duna", "autor": "Frank Herbert", "tema": "Ficcao Cientifica", "status": "Disponivel"},
    {"titulo": "Neuromancer", "autor": "William Gibson", "tema": "Ficcao Cientifica", "status": "Disponivel"},
]

usuarios = {}

# Funções do sistema
def buscar_livro(titulo):
    for livro in st.session_state.catalogo_livros:
        if livro["titulo"].lower() == titulo.lower():
            return livro
    return None

def emprestar_livro(usuario, titulo):
    if not usuario:
        return "Nome do usuário não informado. Não é possível registrar o empréstimo."

    livro = buscar_livro(titulo)
    if not livro:
        return f"Livro '{titulo}' não encontrado."
    if livro["status"] != "Disponivel":
        return f"O livro '{titulo}' não está disponível para empréstimo."

    livro["status"] = "Emprestado"
    if usuario not in st.session_state.usuarios:
        st.session_state.usuarios[usuario] = {"livros": []}
    st.session_state.usuarios[usuario]["livros"].append(titulo)
    return f"Livro '{titulo}' emprestado com sucesso para {usuario}."

    livro = buscar_livro(titulo)
    if not livro:
        return f"Livro '{titulo}' não encontrado."
    if livro["status"] != "Disponivel":
        return f"O livro '{titulo}' não está disponível para empréstimo."

    livro["status"] = "Emprestado"
    if usuario not in st.session_state.usuarios:
        st.session_state.usuarios[usuario] = {"livros": []}
    st.session_state.usuarios[usuario]["livros"].append(titulo)
    return f"Livro '{titulo}' emprestado com sucesso para {usuario}."

def devolver_livro(usuario, titulo):
    if not usuario:
        return "Nome do usuário não informado. Não é possível registrar a devolução."
    
    if usuario not in st.session_state.usuarios:
        return f"O usuário '{usuario}' não possui registros de empréstimos."
    
    livro = buscar_livro(titulo)
    if not livro:
        return f"Livro '{titulo}' não encontrado."
    
    if titulo in st.session_state.usuarios[usuario]["livros"]:
        st.session_state.usuarios[usuario]["livros"].remove(titulo)
        livro["status"] = "Disponivel"
        if not st.session_state.usuarios[usuario]["livros"]:
            del st.session_state.usuarios[usuario]
        return f"Livro '{titulo}' devolvido com sucesso."
    else:
        return f"O usuário {usuario} não possui o livro '{titulo}' para devolução."

    if usuario not in st.session_state.usuarios:
        return f"O usuário '{usuario}' não possui registros de empréstimos."

    livro = buscar_livro(titulo)
    if not livro:
        return f"Livro '{titulo}' não encontrado."

    if titulo in st.session_state.usuarios[usuario]["livros"]:
        st.session_state.usuarios[usuario]["livros"].remove(titulo)
        livro["status"] = "Disponivel"
        if not st.session_state.usuarios[usuario]["livros"]:
            del st.session_state.usuarios[usuario]
        return f"Livro '{titulo}' devolvido com sucesso."
    else:
        return f"O usuário {usuario} não tem o livro '{titulo}' emprestado."

def listar_emprestimos(usuario):
    livros = st.session_state.usuarios.get(usuario, {}).get("livros", [])
    if livros:
        return f"Livros emprestados por {usuario}: {', '.join(livros)}"
    else:
        return f"{usuario} não possui empréstimos ativos."

def listar_catalogo():
    if not st.session_state.catalogo_livros:
        return "Nenhum livro cadastrado no catálogo."
    resultado = "📚 Catálogo de Livros Disponíveis:\n"
    for livro in st.session_state.catalogo_livros:
        resultado += f"- {livro['titulo']} por {livro['autor']} [{livro['tema']}] - Status: {livro['status']}\n"
    return resultado

    if not catalogo_livros:
        return "Nenhum livro cadastrado no catálogo."
    resultado = "📚 Catálogo de Livros Disponíveis:\n"
    for livro in catalogo_livros:
        resultado += f"- {livro['titulo']} por {livro['autor']} [{livro['tema']}] - Status: {livro['status']}\n"
    return resultado

# Definições para a IA
function_definitions = [
    {
        "type": "function",
        "function": {
            "name": "emprestar_livro",
            "description": "Emprestar um livro a um usuário",
            "parameters": {
                "type": "object",
                "properties": {
                    "usuario": {"type": "string", "description": "Nome do usuário"},
                    "titulo": {"type": "string", "description": "Título do livro"}
                },
                "required": ["usuario", "titulo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "devolver_livro",
            "description": "Registrar a devolução de um livro",
            "parameters": {
                "type": "object",
                "properties": {
                    "usuario": {"type": "string", "description": "Nome do usuário"},
                    "titulo": {"type": "string", "description": "Título do livro"}
                },
                "required": ["usuario", "titulo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listar_emprestimos",
            "description": "Listar livros emprestados por um usuário",
            "parameters": {
                "type": "object",
                "properties": {
                    "usuario": {"type": "string", "description": "Nome do usuário"}
                },
                "required": ["usuario"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listar_catalogo",
            "description": "Listar todos os livros disponíveis no catálogo da biblioteca",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

# Mapeamento
function_mapping = {
    "emprestar_livro": emprestar_livro,
    "devolver_livro": devolver_livro,
    "listar_emprestimos": listar_emprestimos,
    "listar_catalogo": listar_catalogo
}

# Streamlit App
def main():
    st.set_page_config(page_title="AIBrary - Biblioteca Inteligente", page_icon="📚")
    st.markdown("""
        <div style='text-align: center;'>
            <h1>AIBrary | Assistente Bibliotecário 📚</h1>
            <h4>Gerencie livros e empréstimos de forma inteligente</h4>
        </div>
        <hr>
    """, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {"role": "system", "content": """
                Você é AIBrary, um assistente de biblioteca. Gerencie empréstimos apenas com nome e título do livro.
                Nunca exija cadastro de email ou dados extras.
                Se faltar informações obrigatórias, solicite educadamente.
                Trabalhe sempre em português e responda de forma breve e clara.
            """}
        ]
    if "pending_action" not in st.session_state:
        st.session_state["pending_action"] = None
        st.session_state["pending_arguments"] = {}

    user_input = st.chat_input("Digite sua mensagem...")

    if user_input:
        if st.session_state.pending_action:
            function_name = st.session_state.pending_action
            pending_args = st.session_state.pending_arguments

            # Captura a resposta do usuário
            user_response = user_input.strip()

            # Lida com as pendências
            if function_name in ["emprestar_livro", "devolver_livro"]:
                # Esperamos: "usuario titulo do livro"
                dados = user_response.split()
                if len(dados) >= 2:
                    usuario = dados[0]
                    titulo = " ".join(dados[1:])
                    resultado = function_mapping[function_name](usuario, titulo)
                    st.session_state.chat_history.append({"role": "function", "name": function_name, "content": resultado})
                    st.success(f"✅ {resultado}")
                    st.session_state.pending_action = None
                    st.session_state.pending_arguments = {}
                else:
                    st.session_state.chat_history.append({"role": "assistant", "content": "Por favor, informe seu nome seguido do título do livro."})

            elif function_name == "listar_emprestimos":
                # Aqui só esperamos o nome do usuário
                usuario = user_response
                resultado = listar_emprestimos(usuario)
                st.session_state.chat_history.append({"role": "function", "name": function_name, "content": resultado})
                st.success(f"✅ {resultado}")
                st.session_state.pending_action = None
                st.session_state.pending_arguments = {}

        else:
            # Conversa normal, manda o que o usuário digitou para o modelo
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            with st.spinner("Consultando a biblioteca..."):
                client = Groq(api_key="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")
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.chat_history,
                    tools=function_definitions
                )

                message = response.choices[0].message

                if hasattr(message, "tool_calls") and message.tool_calls:
                    for tool_call in message.tool_calls:
                        function_name = tool_call.function.name
                        arguments = json.loads(tool_call.function.arguments)

                        required_fields = {
                            "emprestar_livro": ["usuario", "titulo"],
                            "devolver_livro": ["usuario", "titulo"],
                            "listar_emprestimos": ["usuario"],
                            "listar_catalogo": []
                        }.get(function_name, [])

                        missing_fields = [field for field in required_fields if field not in arguments or not arguments[field]]

                        if missing_fields:
                            # -> Faltam dados! NÃO EXECUTAR AGORA.
                            st.session_state.pending_action = function_name
                            st.session_state.pending_arguments = arguments
                            # pergunta conforme o que falta
                            if function_name in ["emprestar_livro", "devolver_livro"]:
                                st.session_state.chat_history.append({
                                    "role": "assistant",
                                    "content": "Por favor, informe seu nome seguido do título do livro."
                                })
                            elif function_name == "listar_emprestimos":
                                st.session_state.chat_history.append({
                                    "role": "assistant",
                                    "content": "Por favor, informe seu nome."
                                })
                            continue  # Não executar nada agora
                        
                        # Só chega aqui se NÃO faltar nada
                        resultado = function_mapping[function_name](**arguments)
                        st.session_state.chat_history.append({
                            "role": "function",
                            "name": function_name,
                            "content": resultado
                        })
                        st.success(f"✅ {resultado}")
                else:
                    # Resposta normal do assistente
                    assistant_reply = message.content
                    st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
                    st.info(assistant_reply)

    st.divider()
    st.subheader("Histórico de Conversa")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").markdown(f"{msg['content']}")
        elif msg["role"] == "assistant":
            st.chat_message("assistant").markdown(f"{msg['content']}")
        elif msg["role"] == "function":
            st.chat_message("assistant").markdown(f"[Execução: {msg['name']}] {msg['content']}")

if __name__ == "__main__":
    main()