import streamlit as st
import ollama
import os


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Cybersecurity RAG Chatbot",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================================
# TITLE
# ==========================================================

st.title("🛡️ Cybersecurity RAG Chatbot")

st.write(
    "Ask cybersecurity questions using "
    "your local RAG chatbot!"
)


# ==========================================================
# MODEL CONFIGURATION
# ==========================================================

EMBEDDING_MODEL = (
    "hf.co/CompendiumLabs/bge-base-en-v1.5-gguf"
)

LANGUAGE_MODEL = (
    "hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF"
)


# ==========================================================
# DATASET PATH
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "cybersecurity-facts.txt"
)


# ==========================================================
# LOAD DATASET
# ==========================================================

@st.cache_resource
def load_dataset():

    try:

        with open(
            DATASET_PATH,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            dataset = file.readlines()

        return dataset

    except Exception as e:

        st.error(
            f"Dataset Error: {e}"
        )

        return []


# ==========================================================
# LOAD DATA
# ==========================================================

dataset = load_dataset()


# ==========================================================
# CREATE VECTOR DATABASE
# ==========================================================

@st.cache_resource
def initialize_vector_db(data):

    vector_db = []

    if len(data) == 0:

        return vector_db

    status_text = st.empty()

    progress_bar = st.progress(0)

    total = len(data)

    for i, chunk in enumerate(data):

        chunk = chunk.strip()

        if not chunk:
            continue

        status_text.text(
            f"Embedding chunk "
            f"{i+1}/{total}"
        )

        try:

            embedding = ollama.embed(
                model=EMBEDDING_MODEL,
                input=chunk
            )["embeddings"][0]

            vector_db.append(
                (chunk, embedding)
            )

        except Exception as e:

            st.error(
                f"Embedding Error: {e}"
            )

        progress_bar.progress(
            (i + 1) / total
        )

    status_text.empty()

    progress_bar.empty()

    return vector_db


# ==========================================================
# INITIALIZE VECTOR DATABASE
# ==========================================================

with st.spinner(
    "Initializing Vector Database..."
):

    VECTOR_DB = initialize_vector_db(
        dataset
    )


# ==========================================================
# COSINE SIMILARITY
# ==========================================================

def cosine_similarity(a, b):

    dot_product = sum([
        x * y for x, y in zip(a, b)
    ])

    norm_a = sum([
        x ** 2 for x in a
    ]) ** 0.5

    norm_b = sum([
        x ** 2 for x in b
    ]) ** 0.5

    if norm_a == 0 or norm_b == 0:

        return 0

    return dot_product / (
        norm_a * norm_b
    )


# ==========================================================
# RETRIEVAL FUNCTION
# ==========================================================

def retrieve(query, top_n=3):

    try:

        query_embedding = ollama.embed(
            model=EMBEDDING_MODEL,
            input=query
        )["embeddings"][0]

    except Exception as e:

        st.error(
            f"Query Embedding Error: {e}"
        )

        return []

    similarities = []

    for chunk, embedding in VECTOR_DB:

        similarity = cosine_similarity(
            query_embedding,
            embedding
        )

        similarities.append(
            (chunk, similarity)
        )

    similarities.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return similarities[:top_n]


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("📂 Database Info")

    if len(VECTOR_DB) > 0:

        st.success(
            f"Loaded "
            f"{len(VECTOR_DB)} "
            f"cybersecurity entries."
        )

    else:

        st.error(
            "Dataset not loaded!"
        )

    st.markdown("---")

    st.subheader(
        "🔍 Retrieved Context"
    )

    st.info(
        "Ask a question to see "
        "retrieved chunks."
    )


# ==========================================================
# USER INPUT
# ==========================================================

input_query = st.text_input(
    "Ask a cybersecurity question:",
    placeholder=(
        "e.g., How do SOC analysts "
        "detect phishing attacks?"
    )
)


# ==========================================================
# PROCESS QUERY
# ==========================================================

if input_query and len(VECTOR_DB) > 0:

    # ======================================================
    # RETRIEVE KNOWLEDGE
    # ======================================================

    retrieved_knowledge = retrieve(
        input_query
    )


    # ======================================================
    # SHOW RETRIEVED RESULTS
    # ======================================================

    with st.sidebar:

        st.markdown("---")

        st.subheader(
            "📊 Similarity Results"
        )

        for i, (
            chunk,
            similarity
        ) in enumerate(
            retrieved_knowledge
        ):

            score = similarity * 100

            st.markdown(
                f"""
### Result {i+1}

**Similarity Score:** `{score:.2f}%`
"""
            )

            st.progress(
                min(
                    max(
                        score / 100,
                        0.0
                    ),
                    1.0
                )
            )

            st.info(chunk)

            st.markdown("---")


    # ======================================================
    # CREATE CONTEXT
    # ======================================================

    context = "\n".join([
        chunk
        for chunk, similarity
        in retrieved_knowledge
    ])


    # ======================================================
    # PROMPT
    # ======================================================

    instruction_prompt = f"""
You are a cybersecurity AI assistant.

Use ONLY the following context
to answer the question.

Context:
{context}

Question:
{input_query}
"""


    # ======================================================
    # RESPONSE UI
    # ======================================================

    st.subheader("🤖 Response")

    response_placeholder = st.empty()

    full_response = ""


    # ======================================================
    # GENERATE RESPONSE
    # ======================================================

    try:

        stream = ollama.chat(

            model=LANGUAGE_MODEL,

            messages=[
                {
                    "role": "system",
                    "content":
                    instruction_prompt
                },

                {
                    "role": "user",
                    "content":
                    input_query
                },
            ],

            stream=True,
        )


        # STREAM RESPONSE
        for chunk in stream:

            token = chunk[
                "message"
            ]["content"]

            full_response += token

            response_placeholder.markdown(
                full_response + "▌"
            )

        # FINAL RESPONSE
        response_placeholder.markdown(
            full_response
        )

    except Exception as e:

        st.error(
            f"Chat Response Error: {e}"
        )