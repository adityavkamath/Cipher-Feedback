import streamlit as st
import os
import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

st.set_page_config(page_title="CFB Simulation", layout="wide")
st.header("🔐 CFB Mode Simulation")

def cfb_encrypt(plaintext_bytes, key, iv, segment_size=16):
    """
    CFB mode encryption implementation
    
    Args:
        plaintext_bytes: Data to encrypt (bytes)
        key: 256-bit encryption key (32 bytes)
        iv: Initialization vector (16 bytes)
        segment_size: Segment size in bytes (default: 16)
    
    Returns:
        Encrypted ciphertext (bytes)
    """
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b''
    feedback_register = iv

    for i in range(0, len(plaintext_bytes), segment_size):
        encrypted_feedback = cipher.encrypt(feedback_register)
        
        plaintext_segment = plaintext_bytes[i:i+segment_size]
        
        ciphertext_segment = bytes(a ^ b for a, b in zip(plaintext_segment, encrypted_feedback))
        ciphertext += ciphertext_segment
        
        feedback_register = feedback_register[len(ciphertext_segment):] + ciphertext_segment
        
        if len(feedback_register) < 16:
            feedback_register += b'\x00' * (16 - len(feedback_register))
    
    return ciphertext

def cfb_decrypt(ciphertext_bytes, key, iv, segment_size=16):
    """
    CFB mode decryption implementation
    
    Args:
        ciphertext_bytes: Data to decrypt (bytes)
        key: 256-bit decryption key (32 bytes)
        iv: Initialization vector (16 bytes)
        segment_size: Segment size in bytes (default: 16)
    
    Returns:
        Decrypted plaintext (bytes)
    """
    cipher = AES.new(key, AES.MODE_ECB) 
    plaintext = b''
    feedback_register = iv

    for i in range(0, len(ciphertext_bytes), segment_size):
        encrypted_feedback = cipher.encrypt(feedback_register)

        ciphertext_segment = ciphertext_bytes[i:i+segment_size]

        plaintext_segment = bytes(a ^ b for a, b in zip(ciphertext_segment, encrypted_feedback))
        plaintext += plaintext_segment

        feedback_register = feedback_register[len(ciphertext_segment):] + ciphertext_segment

        if len(feedback_register) < 16:
            feedback_register += b'\x00' * (16 - len(feedback_register))
    
    return plaintext

def generate_key():
    """Generate a random 256-bit AES key"""
    return secrets.token_bytes(32)

def generate_iv():
    """Generate a random 128-bit IV"""
    return secrets.token_bytes(16)


st.write("""
This simulation demonstrates CFB (Cipher Feedback) mode encryption and decryption using AES as the underlying block cipher.
""")

# Initialize session state
if 'key' not in st.session_state:
    st.session_state.key = generate_key()
if 'iv' not in st.session_state:
    st.session_state.iv = generate_iv()

# Key and IV management
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔑 Generate New Key"):
        st.session_state.key = generate_key()
        st.rerun()

with col2:
    if st.button("🎲 Generate New IV"):
        st.session_state.iv = generate_iv()
        st.rerun()

with col3:
    segment_size = st.selectbox("Segment Size (bytes)", [1, 8, 16], index=2)

# Display current key and IV
st.subheader("🔐 Current Cryptographic Parameters")
col1, col2 = st.columns(2)

with col1:
    st.write("**AES Key (256-bit):**")
    st.code(base64.b64encode(st.session_state.key).decode())

with col2:
    st.write("**Initialization Vector (128-bit):**")
    st.code(base64.b64encode(st.session_state.iv).decode())

st.markdown("---")

# Main encryption/decryption interface
tab1, tab2, tab3 = st.tabs(["🔒 Text Encryption", "🔓 Text Decryption", "📁 File Operations"])

with tab1:
    st.subheader("CFB Encryption")
    
    plaintext_input = st.text_area("Enter plaintext to encrypt:", height=100, placeholder="Type your message here...")
    
    if st.button("🔒 Encrypt Text", disabled=not plaintext_input):
        try:
            # Convert to bytes
            plaintext_bytes = plaintext_input.encode('utf-8')
            
            # Encrypt using CFB mode
            ciphertext_bytes = cfb_encrypt(plaintext_bytes, st.session_state.key, st.session_state.iv, segment_size)
            
            # Encode for display
            ciphertext_b64 = base64.b64encode(ciphertext_bytes).decode()
            
            st.success("✅ Encryption successful!")
            st.write("**Ciphertext (Base64):**")
            st.code(ciphertext_b64, language="text")
            
            # Store in session for decryption tab
            st.session_state.last_ciphertext = ciphertext_b64
            st.session_state.last_plaintext = plaintext_input
            
            # Show encryption details
            with st.expander("🔍 Encryption Details"):
                st.write(f"**Original length:** {len(plaintext_bytes)} bytes")
                st.write(f"**Encrypted length:** {len(ciphertext_bytes)} bytes")
                st.write(f"**Segment size:** {segment_size} bytes")
                st.write(f"**Number of segments:** {(len(plaintext_bytes) + segment_size - 1) // segment_size}")
                
        except Exception as e:
            st.error(f"❌ Encryption failed: {str(e)}")

with tab2:
    st.subheader("CFB Decryption")
    
    # Auto-fill with last ciphertext if available
    default_ciphertext = st.session_state.get('last_ciphertext', '')
    ciphertext_input = st.text_area("Enter ciphertext to decrypt (Base64):", 
                                   value=default_ciphertext, height=100,
                                   placeholder="Paste Base64 encoded ciphertext here...")
    
    if st.button("🔓 Decrypt Text", disabled=not ciphertext_input):
        try:
            # Decode from Base64
            ciphertext_bytes = base64.b64decode(ciphertext_input)
            
            # Decrypt using CFB mode
            decrypted_bytes = cfb_decrypt(ciphertext_bytes, st.session_state.key, st.session_state.iv, segment_size)
            
            # Convert back to string
            decrypted_text = decrypted_bytes.decode('utf-8')
            
            st.success("✅ Decryption successful!")
            st.write("**Decrypted plaintext:**")
            st.code(decrypted_text, language="text")
            
            # Verify round-trip if we have the original
            if 'last_plaintext' in st.session_state:
                if decrypted_text == st.session_state.last_plaintext:
                    st.success("🎯 **Round-trip verification:** SUCCESS - Decrypted text matches original!")
                else:
                    st.error("❌ **Round-trip verification:** FAILED - Decrypted text doesn't match original!")
            
            # Show decryption details
            with st.expander("🔍 Decryption Details"):
                st.write(f"**Ciphertext length:** {len(ciphertext_bytes)} bytes")
                st.write(f"**Decrypted length:** {len(decrypted_bytes)} bytes")
                st.write(f"**Segment size:** {segment_size} bytes")
                
        except Exception as e:
            st.error(f"❌ Decryption failed: {str(e)}")

with tab3:
    st.subheader("File Encryption/Decryption")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📤 Encrypt File**")
        uploaded_file = st.file_uploader("Choose file to encrypt", key="encrypt_file")
        
        if uploaded_file and st.button("🔒 Encrypt File"):
            try:
                # Read file content
                file_bytes = uploaded_file.read()
                
                # Encrypt
                encrypted_bytes = cfb_encrypt(file_bytes, st.session_state.key, st.session_state.iv, segment_size)
                
                # Provide download
                st.download_button(
                    label="💾 Download Encrypted File",
                    data=encrypted_bytes,
                    file_name=f"{uploaded_file.name}.cfb_encrypted",
                    mime="application/octet-stream"
                )
                
                st.success(f"✅ File encrypted! Original: {len(file_bytes)} bytes → Encrypted: {len(encrypted_bytes)} bytes")
                
            except Exception as e:
                st.error(f"❌ File encryption failed: {str(e)}")
    
    with col2:
        st.write("**📥 Decrypt File**")
        encrypted_file = st.file_uploader("Choose encrypted file", key="decrypt_file")
        
        if encrypted_file and st.button("🔓 Decrypt File"):
            try:
                # Read encrypted file
                encrypted_bytes = encrypted_file.read()
                
                # Decrypt
                decrypted_bytes = cfb_decrypt(encrypted_bytes, st.session_state.key, st.session_state.iv, segment_size)
                
                # Determine original filename
                original_name = encrypted_file.name
                if original_name.endswith('.cfb_encrypted'):
                    original_name = original_name[:-14]  # Remove .cfb_encrypted
                else:
                    original_name = f"decrypted_{original_name}"
                
                # Provide download
                st.download_button(
                    label="💾 Download Decrypted File",
                    data=decrypted_bytes,
                    file_name=original_name,
                    mime="application/octet-stream"
                )
                
                st.success(f"✅ File decrypted! Encrypted: {len(encrypted_bytes)} bytes → Decrypted: {len(decrypted_bytes)} bytes")
                
            except Exception as e:
                st.error(f"❌ File decryption failed: {str(e)}")


