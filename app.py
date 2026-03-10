import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt

from he.he_context import create_context
from he.encryptor import encrypt_vector
from he.decryptor import decrypt_vector
from he.evaluator import encrypted_linear_score

from model.risk_model import WEIGHTS, BIAS
from model.plaintext_model import compute_plain


st.set_page_config(page_title="Privacy-Preserving Credit Risk Scoring", layout="wide")

st.title("🔐 Privacy-Preserving Credit Risk Scoring Demo")


# -----------------------------
# Attack Simulation Dialog
# -----------------------------

@st.dialog("⚠️ Live Attack Simulation")
def attack_simulation():

    if "cipher_preview" not in st.session_state:
        st.warning("Run the computation first to generate encrypted traffic.")
        return

    st.warning("Attacker intercepted network traffic.")

    st.write("Timestamp:", st.session_state.packet_time)
    st.write("Ciphertext Size:", st.session_state.cipher_size, "bytes")
    st.write("Encrypted Vector Length:", st.session_state.vector_len)

    st.markdown("### Ciphertext Preview")

    st.code(st.session_state.cipher_preview)

    attack_attempt = st.selectbox(
        "Attacker Action",
        [
            "Try to read plaintext",
            "Try brute-force decode",
            "Inspect packet metadata"
        ]
    )

    if attack_attempt == "Try to read plaintext":
        st.error("Failed — ciphertext cannot be decoded.")

    elif attack_attempt == "Try brute-force decode":
        st.error("Failed — secret key required.")

    elif attack_attempt == "Inspect packet metadata":
        st.info("Attacker can only observe ciphertext structure.")

    st.success("Homomorphic encryption keeps financial data private.")


# -----------------------------
# Input Section
# -----------------------------

st.markdown("## Input Financial Data")

col1, col2, col3 = st.columns(3)

with col1:
    income = st.number_input("Income", value=5000.0)
    loan = st.number_input("Loan Amount", value=20000.0)

with col2:
    credit_score = st.number_input("Credit Score", value=720.0)
    debt_ratio = st.number_input("Debt Ratio", value=0.35)

with col3:
    employment_years = st.number_input("Employment Years", value=5)
    open_loans = st.number_input("Open Loans", value=2)


x = [
    income,
    loan,
    credit_score,
    debt_ratio,
    employment_years,
    open_loans
]


# -----------------------------
# Compute Button
# -----------------------------

if st.button("Compute Risk Score"):

    st.markdown("---")

    # Plaintext compute
    start_plain = time.time()

    plaintext_score = compute_plain(x, WEIGHTS, BIAS)

    plaintext_compute_time = time.time() - start_plain


    # HE Context
    context = create_context()

    # Encryption
    start_enc = time.time()

    enc_x = encrypt_vector(context, x)

    encryption_time = time.time() - start_enc


    serialized = enc_x.serialize()

    st.session_state.cipher_preview = serialized[:120]
    st.session_state.cipher_size = len(serialized)
    st.session_state.vector_len = len(x)
    st.session_state.packet_time = time.strftime("%H:%M:%S")


    # HE Compute
    start_compute = time.time()

    enc_score = encrypted_linear_score(enc_x, WEIGHTS, BIAS)

    compute_time = time.time() - start_compute


    # Decrypt
    start_dec = time.time()

    he_score = decrypt_vector(enc_score)[0]

    decrypt_time = time.time() - start_dec


    total_he_time = encryption_time + compute_time + decrypt_time


    # -----------------------------
    # Results Section
    # -----------------------------

    st.markdown("## Results")

    col_plain, col_he = st.columns(2)

    # Plaintext column
    with col_plain:

        st.subheader("📄 Plaintext Processing")

        st.metric(
            "Risk Score",
            f"{plaintext_score:.5f}"
        )

        st.metric(
            "Server Compute Time",
            f"{plaintext_compute_time:.6f} seconds"
        )


    # HE column
    with col_he:

        st.subheader("🔐 Homomorphic Encryption")

        st.metric(
            "HE Score",
            f"{he_score:.5f}"
        )

        st.metric(
            "Encryption Time",
            f"{encryption_time:.6f} seconds"
        )

        st.metric(
            "Server Compute Time",
            f"{compute_time:.6f} seconds"
        )

        st.metric(
            "Decryption Time",
            f"{decrypt_time:.6f} seconds"
        )

        st.metric(
            "Total HE Time",
            f"{total_he_time:.6f} seconds"
        )


    # Correctness check
    st.success(
        f"Difference between Plaintext and HE score: {abs(plaintext_score - he_score):.8f}"
    )


    # -----------------------------
    # Performance Charts
    # -----------------------------

    st.markdown("## Performance Comparison")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:

        df = pd.DataFrame({
            "Method": ["Plaintext", "Homomorphic Encryption"],
            "Time": [plaintext_compute_time, total_he_time]
        })

        fig, ax = plt.subplots()

        ax.bar(df["Method"], df["Time"])

        ax.set_ylabel("Time (seconds)")
        ax.set_title("Plaintext vs HE Total Time")

        st.pyplot(fig)


    with col_chart2:

        df2 = pd.DataFrame({
            "Stage": ["Encryption", "Computation", "Decryption"],
            "Time": [encryption_time, compute_time, decrypt_time]
        })

        fig2, ax2 = plt.subplots()

        ax2.bar(df2["Stage"], df2["Time"])

        ax2.set_ylabel("Time (seconds)")
        ax2.set_title("HE Processing Breakdown")

        st.pyplot(fig2)


# -----------------------------
# Attack Simulation Button
# -----------------------------

st.markdown("---")

if st.button("⚠️ Live Attack Simulation Panel"):
    attack_simulation()