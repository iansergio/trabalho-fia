import streamlit as st
import fitz  # PyMuPDF
from groq import Groq

# Configurar chave da Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Função para extrair texto dos PDFs
def extract_files(uploader):
    text = ""
    for pdf in uploader:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text")
    return text

# Função de chat com histórico
def chat_with_groq(user_prompt):
    messages = st.session_state["chat_history"]
    messages.append({"role": "user", "content": user_prompt})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Modelo válido
        messages=messages
    )
    
    assistant_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_reply})
    
    return assistant_reply

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }
            
    body {
        background-image: url('https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdTZpMXQxYzg4dHFwcHlwMXR6bm1jZHRuZTQ4dG1raHJ2Nm5nN2JvZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/11bpfFjr6pQfsJ0XQ7/giphy.gif');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        color: white;
    }

    /* Transparência para destacar os elementos */
    .stApp {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 2rem;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Interface principal
def main():
    st.title("Ednilson")

    # Inicializar o histórico se não existir
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {"role": "system", "content": "Você é um assistente que responde com base em documentos fornecidos. Aja como um bibliotecário(a) e sempre consulte a base fornecida."}
        ]

    with st.sidebar:
        st.header("Upload de Arquivos")
        uploader = st.file_uploader("Adicione arquivos PDF", type="pdf", accept_multiple_files=True)

    if uploader:
        text = extract_files(uploader)
        st.session_state["document-text"] = text
        st.success("Texto extraído com sucesso!")
        # Adiciona contexto no sistema
        st.session_state["chat_history"].append(
            {"role": "system", "content": f"Contexto dos documentos carregados:\n{text}"}
        )

    user_input = st.text_input("Digite a sua pergunta")

    if user_input and "document-text" in st.session_state:
        with st.spinner("Consultando IA..."):
            resposta = chat_with_groq(user_input)
            st.markdown("**Resposta da IA:**")
            st.write(resposta)

if __name__ == "__main__":
    main()
