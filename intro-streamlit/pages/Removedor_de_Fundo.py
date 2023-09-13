import streamlit as st
from PIL import Image
from rembg import remove


def remove_br(image, widget):
    bytes_data = Image.open(image)
    output = remove(bytes_data)
    widget.title("Imagem sem fundo")
    widget.image(output)


st.title("Carregando um arquivo")
image = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg"])

# Cria duas colunas para a página
col_a, col_b = st.columns(2)

if image is not None:
    # Coloca a imagem na primeira coluna
    col_a.title("Imagem com fundo")
    col_a.image(image)

    st.button("Remover fundo", on_click=remove_br, args=(image, col_b))

# Código fonte utilizado para criar a imagem de fundo
with st.expander("Código fonte"):
    st.code(
    """
    import streamlit as st
    from PIL import Image
    from rembg import remove


    def remove_br(image, widget):
        bytes_data = Image.open(image)
        output = remove(bytes_data)
        widget.title("Imagem sem fundo")
        widget.image(output)


    st.title("Carregando um arquivo")
    image = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg"])

    # Cria duas colunas para a página
    col_a, col_b = st.columns(2)

    if image is not None:
        # Coloca a imagem na primeira coluna
        col_a.title("Imagem com fundo")
        col_a.image(image)

        st.button("Remover fundo", on_click=remove_br, args=(image, col_b))
    """,
    language="python" 
    )