import json
import streamlit as st
import random
from groq import Groq  # Verifique se você está importando corretamente a biblioteca

# Banco simulado com livros enriquecidos
st.session_state["catalogo_livros"] = [
    {"titulo": "Fundacao", "autor": "Isaac Asimov", "tema": "Ficcao Cientifica", "status": "Disponivel"},
    {"titulo": "Duna", "autor": "Frank Herbert", "tema": "Ficcao Cientifica", "status": "Disponivel"},
    {"titulo": "Neuromancer", "autor": "William Gibson", "tema": "Ficcao Cientifica", "status": "Disponivel"},
    {"titulo": "1984", "autor": "George Orwell", "tema": "Distopia", "status": "Disponivel"},
    {"titulo": "O Hobbit", "autor": "J.R.R. Tolkien", "tema": "Fantasia", "status": "Disponivel"},
    {"titulo": "Harry Potter e a Pedra Filosofal", "autor": "J.K. Rowling", "tema": "Fantasia", "status": "Disponivel"},
    {"titulo": "O Senhor dos Anéis: A Sociedade do Anel", "autor": "J.R.R. Tolkien", "tema": "Fantasia", "status": "Emprestado"},
    {"titulo": "A Guerra dos Tronos", "autor": "George R.R. Martin", "tema": "Fantasia", "status": "Disponivel"},
    {"titulo": "O Código Da Vinci", "autor": "Dan Brown", "tema": "Mistério", "status": "Disponivel"},
    {"titulo": "A Menina que Roubava Livros", "autor": "Markus Zusak", "tema": "Ficção Histórica", "status": "Disponivel"},
    {"titulo": "O Caçador de Pipas", "autor": "Khaled Hosseini", "tema": "Drama", "status": "Disponivel"},
    {"titulo": "O Diário de Anne Frank", "autor": "Anne Frank", "tema": "Memórias", "status": "Emprestado"},
    {"titulo": "Mestre do Jogo", "autor": "Sidney Sheldon", "tema": "Suspense", "status": "Disponivel"},
    {"titulo": "O Poder do Hábito", "autor": "Charles Duhigg", "tema": "Psicologia", "status": "Disponivel"},
    {"titulo": "Sapiens: Uma Breve História da Humanidade", "autor": "Yuval Noah Harari", "tema": "História", "status": "Disponivel"},
    {"titulo": "O Príncipe", "autor": "Nicolau Maquiavel", "tema": "Filosofia", "status": "Disponivel"},
]

# Função de recomendação de livros
def recomendar_livros(titulo):
    livro_referencia = next((livro for livro in st.session_state.catalogo_livros if livro['titulo'].lower() == titulo.lower()), None)
    
    if not livro_referencia:
        return f"Livro '{titulo}' não encontrado no catálogo."
    
    tema = livro_referencia['tema']
    autor = livro_referencia['autor']
    
    livros_recomendados = [
        livro for livro in st.session_state.catalogo_livros 
        if livro['tema'] == tema or livro['autor'] == autor and livro['titulo'] != titulo
    ]
    
    if not livros_recomendados:
        return "Desculpe, não temos livros recomendados no momento."

    recomendacoes = random.sample(livros_recomendados, min(3, len(livros_recomendados)))
    
    resposta = "🎯 Recomendações de livros:\n"
    for livro in recomendacoes:
        resposta += f"- **{livro['titulo']}** por {livro['autor']} ({livro['tema']}) - Status: {livro['status']}\n"
    
    return resposta

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

    user_input = st.chat_input("Digite sua mensagem...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Consultando a biblioteca..."):
            client = Groq(api_key="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")
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",  # Ou qualquer modelo válido da Groq
                    messages=st.session_state.chat_history
                )

                message = response['choices'][0]['message']['content']
                st.session_state.chat_history.append({"role": "assistant", "content": message})
                st.info(message)

            except Exception as e:
                st.error(f"Ocorreu um erro ao acessar a API da Groq: {e}")

if __name__ == "__main__":
    main()
