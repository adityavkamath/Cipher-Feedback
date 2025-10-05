import streamlit as st

st.set_page_config(page_title="Procedure", layout="wide")
st.header("CFB Mode Implementation Procedure")

st.write(
    """
The steps followed in this CFB (Cipher Feedback) mode encryption project:
"""
)

st.markdown("---")

st.subheader("� Implementation Steps")

st.markdown("""
1. **Select encryption parameters:**
   - Choose AES-256 as the block cipher
   - Set segment size (1, 8, or 16 bytes)
   - Generate a unique 128-bit IV for each encryption

2. **Input plaintext:**
   - Enter text message or upload a file
   - System converts input to bytes for processing

3. **Encryption process:**
   - Initialize feedback register with IV
   - Encrypt feedback register using AES
   - XOR result with plaintext segment
   - Update feedback register with ciphertext

4. **View results:**
   - Display encrypted ciphertext in hexadecimal
   - Show step-by-step encryption process
   - Export results if needed

5. **Decryption verification:**
   - Use same key and IV for decryption
   - Apply reverse CFB process
   - Verify that decrypted text matches original input

""")
