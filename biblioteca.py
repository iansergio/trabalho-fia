import random
import json
import streamlit as st
from groq import Groq  # Substitua pelo seu client adequado

# Banco simulado com livros enriquecidos
st.session_state.catalogo_livros = [
    {"titulo": "Fundacao", "autor": "Isaac Asimov", "tema": "Ficcao Cientifica", "status": "Disponivel", 
     "descricao": "Uma saga épica sobre o futuro da humanidade e a ciência do comportamento humano.", 
     "ano_publicacao": 1951, "avaliacao": 4.7},
    {"titulo": "Duna", "autor": "Frank Herbert", "tema": "Ficcao Cientifica", "status": "Disponivel", 
     "descricao": "Uma história de poder, religião e ecologia em um futuro distante, no planeta desértico Arrakis.", 
     "ano_publicacao": 1965, "avaliacao": 4.8},
    {"titulo": "Neuromancer", "autor": "William Gibson", "tema": "Ficcao Cientifica", "status": "Disponivel", 
     "descricao": "Uma história de hackers e inteligência artificial, que ajudou a definir o gênero ciberpunk.", 
     "ano_publicacao": 1984, "avaliacao": 4.5},
    {"titulo": "1984", "autor": "George Orwell", "tema": "Distopia", "status": "Disponivel", 
     "descricao": "Uma sociedade totalitária onde o governo controla todos os aspectos da vida humana.", 
     "ano_publicacao": 1949, "avaliacao": 4.9},
    {"titulo": "O Hobbit", "autor": "J.R.R. Tolkien", "tema": "Fantasia", "status": "Disponivel", 
     "descricao": "Aventura de Bilbo Baggins, que é levado em uma jornada cheia de perigos e mistérios.", 
     "ano_publicacao": 1937, "avaliacao": 4.6},
]

# Função de busca de livros
def buscar_livro(titulo):
    for livro in st.session_state.catalogo_livros:
        if livro["titulo"].lower() == titulo.lower():
            return livro
    return None

# Função para listar empréstimos (exemplo básico)
def listar_emprestimos(usuario):
    return f"Empréstimos de {usuario}: Nenhum empréstimo no momento."

# Função de empréstimo de livro (exemplo básico)
def emprestar_livro(usuario, titulo):
    livro = buscar_livro(titulo)
    if livro:
        if livro["status"] == "Disponivel":
            livro["status"] = "Emprestado"
            return f"{usuario} emprestou o livro '{titulo}'."
        else:
            return f"O livro '{titulo}' já está emprestado."
    else:
        return f"O livro '{titulo}' não foi encontrado."

# Função para devolver livro
def devolver_livro(usuario, titulo):
    livro = buscar_livro(titulo)
    if livro:
        if livro["status"] == "Emprestado":
            livro["status"] = "Disponivel"
            return f"{usuario} devolveu o livro '{titulo}'."
        else:
            return f"O livro '{titulo}' não está emprestado."
    else:
        return f"O livro '{titulo}' não foi encontrado."

# Função de recomendação de livros
def recomendar_livros(titulo):
    livro_referencia = buscar_livro(titulo)
    
    if not livro_referencia:
        return f"Livro '{titulo}' não encontrado no catálogo."
    
    tema = livro_referencia['tema']
    autor = livro_referencia['autor']
    
    # Recomendando livros do mesmo tema ou autor
    livros_recomendados = [
        livro for livro in st.session_state.catalogo_livros 
        if livro['tema'] == tema or livro['autor'] == autor and livro['titulo'] != titulo
    ]
    
    if not livros_recomendados:
        return "Desculpe, não temos livros recomendados no momento."

    recomendacoes = random.sample(livros_recomendados, min(3, len(livros_recomendados)))
    
    resposta = "🎯 Recomendações de livros:\n"
    for livro in recomendacoes:
        resposta += f"- **{livro['titulo']}** por {livro['autor']} ({livro['ano_publicacao']}) - Avaliação: {livro['avaliacao']}/5\n"
        resposta += f"  *{livro['descricao']}*\n\n"
    
    return resposta

# Funções definidas para interação com o assistente
function_definitions = [
    {
        "type": "function",
        "function": {
            "name": "emprestar_livro",
            "description": "Emprestar um livro para um usuário",
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
            "description": "Devolver um livro emprestado",
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
            "description": "Listar empréstimos de um usuário",
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
            "description": "Listar todos os livros no catálogo",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recomendar_livros",
            "description": "Recomendar livros baseados no tema ou autor do livro fornecido.",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string", "description": "Título do livro para recomendações"}
                },
                "required": ["titulo"]
            }
        }
    }
]

# Mapeamento das funções
function_mapping = {
    "emprestar_livro": emprestar_livro,
    "devolver_livro": devolver_livro,
    "listar_emprestimos": listar_emprestimos,
    "listar_catalogo": lambda: st.session_state.catalogo_livros,
    "recomendar_livros": recomendar_livros
}

# Função principal para execução do aplicativo
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
                Você é AIBrary, um assistente de biblioteca. Gerencie empréstimos, devoluções, recomendações e informações de livros.
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

            elif function_name == "recomendar_livros":
                titulo = user_response
                resultado = recomendar_livros(titulo)
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
                            "listar_catalogo": [],
                            "recomendar_livros": ["titulo"]
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
                            elif function_name == "recomendar_livros":
                                st.session_state.chat_history.append({
                                    "role": "assistant",
                                    "content": "Por favor, informe o título do livro que você quer que eu recomende."
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
