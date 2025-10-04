import streamlit as st

st.set_page_config(page_title="Introduction", layout="wide")
st.header("Introduction to CFB Mode")

st.write("""
In modern cryptography, **block ciphers** like AES (Advanced Encryption Standard) operate on fixed-size blocks of data. 
However, real-world data often comes in arbitrary lengths, requiring **modes of operation** to handle variable-length inputs.

**CFB (Cipher Feedback)** is one of the five standard modes of operation for block ciphers, 
alongside ECB, CBC, OFB, and CTR modes. CFB mode transforms a block cipher into a **stream cipher**, 
enabling encryption and decryption of data streams of any length.

### Key Characteristics of CFB Mode:

🔐 **Stream-like Operation**: Processes data in segments smaller than the block size  
🔄 **Self-Synchronizing**: Can recover from transmission errors automatically  
⚡ **Real-time Processing**: Suitable for encrypting data as it arrives  
🛡️ **Error Propagation**: Limited error propagation enhances security  
🔗 **Chaining**: Each ciphertext block depends on all previous plaintext blocks  

### Applications:
- **Network Communications**: SSL/TLS protocols
- **Real-time Data Encryption**: Voice and video streaming
- **Error-Prone Channels**: Radio communications
- **Interactive Applications**: Terminal sessions and chat applications

CFB mode is particularly valuable when you need to encrypt data immediately as it becomes available, 
without waiting for a complete block.
""")