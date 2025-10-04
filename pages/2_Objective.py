import streamlit as st

st.set_page_config(page_title="Objective", layout="wide")
st.header("Aim and Objectives")

st.write("""
The main objectives of this CFB (Cipher Feedback) mode implementation project are:

### 🎯 Primary Objectives:

1. **Understand CFB Mode Theory**: Learn the mathematical foundation and working principle of CFB mode operation.

2. **Implement CFB Encryption Algorithm**: Build a complete CFB encryption system that can handle variable-length input data.

3. **Implement CFB Decryption Algorithm**: Develop the corresponding decryption process to recover original plaintext.

4. **Demonstrate Stream Cipher Behavior**: Show how CFB transforms a block cipher into a stream cipher.

5. **Interactive Simulation**: Create a user-friendly interface for encrypting/decrypting text and understanding the process.

### 🔍 Learning Outcomes:

- Master the concept of **block cipher modes of operation**
- Understand the difference between **block ciphers** and **stream ciphers**
- Learn about **initialization vectors (IV)** and their importance
- Comprehend **error propagation** characteristics in CFB mode
- Gain practical experience in **cryptographic algorithm implementation**
- Understand **security considerations** specific to CFB mode

### 💡 Practical Applications:

- Real-time data encryption for network communications
- Secure transmission over error-prone channels
- Understanding modern cryptographic protocols (SSL/TLS)
- Foundation for advanced cryptographic studies

This project bridges theoretical cryptography concepts with practical implementation.
""")
