import streamlit as st
import time
import streamlit.components.v1 as components
import pandas as pd
import matplotlib.pyplot as plt

from he.he_context import create_context
from he.encryptor import encrypt_vector
from he.decryptor import decrypt_vector
from he.evaluator import encrypted_linear_score

from model.risk_model import WEIGHTS, BIAS
from model.plaintext_model import compute_plain


st.set_page_config(page_title="Homomorphic Encryption Demo", layout="wide")

st.title("🔐 Privacy-Preserving Credit Risk Scoring")


# -----------------------------------------------------
# Pipeline Indicator
# -----------------------------------------------------

def pipeline_indicator(step):

    steps = ["Client", "Encryption", "Encrypted Server", "Decryption"]
    colors = ["#4CAF50", "#FFC107", "#2196F3", "#FF7043"]

    html = """
    <style>
    .pipeline {display:flex;width:100%;font-weight:bold;}
    .step {
        flex:1;
        padding:16px;
        text-align:center;
        border-radius:10px;
        margin-right:6px;
        color:white;
        transition:all 0.4s ease;
    }
    </style>
    <div class="pipeline">
    """

    for i, name in enumerate(steps):

        border = "4px solid black" if i == step else "1px solid #ddd"

        html += f"""
        <div class="step"
        style="background:{colors[i]};border:{border};">
        {name}
        </div>
        """

    html += "</div>"

    components.html(html, height=80)


pipeline_placeholder = st.empty()


# -----------------------------------------------------
# Attack Simulation Popup
# -----------------------------------------------------

@st.dialog("⚠️ Live Attack Simulation")
def attack_simulation():

    if "cipher_preview" not in st.session_state:
        st.warning("Run the computation first to generate encrypted traffic.")
        return

    st.warning("Attacker intercepted network traffic.")

    st.markdown("### Captured Packet Metadata")

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


# -----------------------------------------------------
# Input Section
# -----------------------------------------------------

st.markdown("### Input Financial Features")

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

st.markdown("---")


# -----------------------------------------------------
# Compute
# -----------------------------------------------------

if st.button("Compute Risk Score"):

    progress = st.progress(0)

    x = [
        income,
        loan,
        credit_score,
        debt_ratio,
        employment_years,
        open_loans
    ]

    context = create_context()

    col_client, col_server = st.columns(2)


    # CLIENT INPUT
    with pipeline_placeholder:
        pipeline_indicator(0)

    with col_client:
        st.markdown("## 🧑 Client Machine")
        st.info("User Inputs Financial Data")
        st.write("Feature Vector:", x)

    with col_server:
        st.markdown("## ☁ Secure HE Compute Server")
        st.caption("Running TenSEAL homomorphic computation")

    progress.progress(10)
    time.sleep(1)


    # ENCRYPTION
    with pipeline_placeholder:
        pipeline_indicator(1)

    with col_client:
        st.warning("Encrypting Data (CKKS)")

    start_enc = time.time()
    enc_x = encrypt_vector(context, x)
    end_enc = time.time()

    encryption_time = end_enc - start_enc

    serialized = enc_x.serialize()

    st.session_state.cipher_preview = serialized[:120]
    st.session_state.cipher_size = len(serialized)
    st.session_state.vector_len = len(x)
    st.session_state.packet_time = time.strftime("%H:%M:%S")

    with col_client:
        st.success("Encryption Completed")
        st.write("Encryption Time:", round(encryption_time,6),"seconds")
        st.write("Ciphertext Size:", len(serialized),"bytes")

    progress.progress(40)
    time.sleep(1)


    # SERVER COMPUTE
    with pipeline_placeholder:
        pipeline_indicator(2)

    with col_server:
        st.warning("Homomorphic Computation Running")

    start_compute = time.time()
    enc_score = encrypted_linear_score(enc_x, WEIGHTS, BIAS)
    end_compute = time.time()

    compute_time = end_compute - start_compute

    with col_server:
        st.success("Encrypted Computation Completed")
        st.write("Server Compute Time:", round(compute_time,6),"seconds")

    progress.progress(70)
    time.sleep(1)


    # DECRYPTION
    with pipeline_placeholder:
        pipeline_indicator(3)

    with col_client:
        st.warning("Decrypting Result")

    start_dec = time.time()
    score = decrypt_vector(enc_score)[0]
    end_dec = time.time()

    decrypt_time = end_dec - start_dec

    with col_client:
        st.success("Decryption Completed")
        st.write("Decryption Time:", round(decrypt_time,6),"seconds")

    progress.progress(90)
    time.sleep(1)


    # RESULTS
    plain_start = time.time()
    plain_score = compute_plain(x, WEIGHTS, BIAS)
    plain_end = time.time()

    plaintext_time = plain_end - plain_start

    total_time = encryption_time + compute_time + decrypt_time

    progress.progress(100)

    st.markdown("## 🎯 Final Results")

    st.write("HE Risk Score:", round(score,4))
    st.write("Plaintext Baseline:", round(plain_score,4))
    st.write("Total HE Processing Time:", round(total_time,6),"seconds")


    # -----------------------------------------------------
    # Performance Charts
    # -----------------------------------------------------

    st.markdown("## 📊 Performance Comparison")

    col1, col2, col3 = st.columns(3)

    with col1:

        df_compare = pd.DataFrame({
            "Method": ["Plaintext", "Homomorphic Encryption"],
            "Time": [plaintext_time, total_time]
        })

        fig1, ax1 = plt.subplots()
        ax1.bar(df_compare["Method"], df_compare["Time"])
        ax1.set_title("Plaintext vs HE")
        ax1.set_ylabel("Seconds")

        st.pyplot(fig1)

    with col2:

        df_breakdown = pd.DataFrame({
            "Stage": ["Encryption", "Compute", "Decryption"],
            "Time": [encryption_time, compute_time, decrypt_time]
        })

        fig2, ax2 = plt.subplots()
        ax2.bar(df_breakdown["Stage"], df_breakdown["Time"])
        ax2.set_title("HE Processing Breakdown")

        st.pyplot(fig2)

    with col3:

        plaintext_size = len(str(x).encode())
        cipher_size = len(serialized)

        df_size = pd.DataFrame({
            "Type": ["Plaintext", "Ciphertext"],
            "Size": [plaintext_size, cipher_size]
        })

        fig3, ax3 = plt.subplots()
        ax3.bar(df_size["Type"], df_size["Size"])
        ax3.set_title("Ciphertext Expansion")

        st.pyplot(fig3)


# -----------------------------------------------------
# Attack Simulation Button
# -----------------------------------------------------

st.markdown("---")

if st.button("⚠️ Live Attack Simulation Panel"):
    attack_simulation()