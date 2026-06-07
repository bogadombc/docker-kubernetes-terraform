import os
import pandas as pd
import psycopg
import streamlit as st


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "clientesdb")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "pass")


def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def inserir_cliente(nome, email, telefone):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO clientes (nome, email, telefone)
                VALUES (%s, %s, %s);
                """,
                (nome, email, telefone)
            )
            conn.commit()


def listar_clientes():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, nome, email, telefone, criado_em
                FROM clientes
                ORDER BY id;
                """
            )
            linhas = cur.fetchall()

    return linhas


st.set_page_config(
    page_title="Cadastro de Clientes",
    layout="centered"
)

st.title("Cadastro de Clientes")
st.write("Aplicação Streamlit conectada a um banco PostgreSQL usando Docker Compose.")

st.divider()

st.subheader("Novo cliente")

with st.form("form_cliente"):
    nome = st.text_input("Nome")
    email = st.text_input("E-mail")
    telefone = st.text_input("Telefone")

    enviar = st.form_submit_button("Salvar cliente")

    if enviar:
        if not nome or not email:
            st.error("Nome e e-mail são obrigatórios.")
        else:
            inserir_cliente(nome, email, telefone)
            st.success("Cliente cadastrado com sucesso.")

st.divider()

st.subheader("Clientes cadastrados")

try:
    clientes = listar_clientes()

    if clientes:
        df = pd.DataFrame(
            clientes,
            columns=["ID", "Nome", "E-mail", "Telefone", "Criado em"]
        )
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhum cliente cadastrado ainda.")

except Exception as e:
    st.error("Não foi possível conectar ao banco de dados.")
    st.exception(e)
