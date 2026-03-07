# 🔐 Privacy-Preserving Credit Risk Scoring using Homomorphic Encryption

This project demonstrates how **Homomorphic Encryption (HE)** enables secure computation on encrypted financial data without exposing the underlying information.

The system encrypts user financial inputs, sends encrypted data to a compute server, performs calculations on ciphertext, and returns an encrypted result which is decrypted only on the client side.

---

# 🚀 Features

- Homomorphic Encryption using **TenSEAL (CKKS scheme)**
- Secure computation without exposing raw financial data
- Interactive UI using **Streamlit**
- Docker containerized deployment
- Dynamic attack simulation showing intercepted encrypted packets
- Performance comparison between plaintext and encrypted computation
- Ciphertext expansion analysis

---

# 🧠 Input Features

The credit risk model uses the following inputs:

- Income
- Loan Amount
- Credit Score
- Debt Ratio
- Employment Years
- Number of Open Loans

These values are encrypted before being processed.

---

# 🔐 Security Demonstration

The system includes a **Live Attack Simulation Panel** that demonstrates:

What an attacker can see:

- Encrypted ciphertext
- Packet metadata

What an attacker **cannot see**:

- Income
- Loan amount
- Credit score
- Risk score

This demonstrates the confidentiality guarantees of Homomorphic Encryption.

---

# 📊 Performance Metrics

The application visualizes:

- Plaintext vs Homomorphic computation time
- Encryption / Computation / Decryption breakdown
- Ciphertext size expansion

---

# 🐳 Running with Docker

### Build the Docker Image

```bash
docker build -t he-demo .

Run the Container
docker run -p 8501:8501 --name he-secure-compute-server he-demo

Open the application:
http://localhost:8501

🛠 Local Development
pip install -r requirements.txt
streamlit run app.py

📦 Project Structure
he_credit_risk_demo
│
├── app.py
├── Dockerfile
├── requirements.txt
│
├── he/
│   ├── he_context.py
│   ├── encryptor.py
│   ├── decryptor.py
│   └── evaluator.py
│
└── model/
├── risk_model.py
└── plaintext_model.py

📚 Technologies Used
Python
Streamlit
TenSEAL
Docker
Pandas
Matplotlib

📌 Author
Arindom Datta


