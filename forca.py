import streamlit as st

# Frase alvo
frase = 'Eu te amo meu amor'

# Dicionário de imagens por fase
fases = {
    7: "imagem/1.png",
    6: "imagem/2.png",
    5: "imagem/3.png",
    4: "imagem/4.png",
    3: "imagem/5.png",
    2: "imagem/6.png",
    1: "imagem/7.png",
    0: "imagem/8.png",
}

# Função para exibir imagem da fase
def img():
    st.image(fases.get(st.session_state.tentativas))

# Estilo da página
st.title('Jogo da Forca do Amor 💘')
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] > .main {
            background-color: #FF9A8B;
            background-image: linear-gradient(90deg, #FF9A8B 0%, #FF6A88 100%);
        }
    </style>
    """, unsafe_allow_html=True)

# Função para reiniciar o jogo
def reset_game():
    st.session_state.clear()
    st.experimental_rerun()

# Inicialização do estado
if 'tentativas' not in st.session_state:
    st.session_state.tentativas = 7
    st.session_state.letras_adivinhadas = []
    st.session_state.frase_completa = ''.join(['_' if c != ' ' else ' ' for c in frase])
    img()

# Entrada do usuário
input_letra = st.text_input('Digite uma letra 😁', key="input_letra")

# Função principal do jogo
def jogar():
    if input_letra:
        letra = input_letra.strip().lower()

        if len(letra) == 1 and letra.isalpha():
            if letra in st.session_state.letras_adivinhadas:
                st.error(f"Essa letra já foi usada: {letra}")
            elif letra not in frase.lower():
                st.error(f"{letra} não está na frase 😢")
                st.session_state.tentativas -= 1
                st.session_state.letras_adivinhadas.append(letra)
            else:
                st.success(f"Arrasou! {letra} está na frase 💖")
                st.session_state.letras_adivinhadas.append(letra)
                nova_frase = list(st.session_state.frase_completa)
                for i, c in enumerate(frase.lower()):
                    if c == letra:
                        nova_frase[i] = frase[i]  # Mantém maiúsculas
                st.session_state.frase_completa = ''.join(nova_frase)
        elif len(letra) > 1:
            st.warning('Digite apenas uma letra.')
        else:
            st.warning('Digite uma letra válida.')

        img()

        # Verifica vitória
        if '_' not in st.session_state.frase_completa:
            st.balloons()
            st.success('Você acertou a frase! Eu te amo imensamente! 💘')

        # Verifica derrota
        if st.session_state.tentativas <= 0:
            st.error('Você perdeu 😢')
            if st.button('Tentar novamente'):
                reset_game()

    # Exibe a frase com letras adivinhadas
    columns = st.columns(len(frase))
    for i, col in enumerate(columns):
        with col:
            char = st.session_state.frase_completa[i]
            st.subheader(char if char != '_' else '_')

# Executa o jogo
jogar()

# Debug opcional
st.write(f"Tentativas restantes: {st.session_state.tentativas}")
