import streamlit as st

st.set_page_config(page_title="Procedure", layout="wide")
st.header("CFB Mode Implementation Procedure")

st.write(
    """
This section outlines the step-by-step procedure for implementing and using CFB (Cipher Feedback) mode encryption.
"""
)

st.markdown("---")

# ------------------ Setup Phase ------------------
st.subheader("🔧 Phase 1: Setup and Initialization")

st.write(
    """
**Step 1.1: Generate Cryptographic Parameters**
1. Generate a **256-bit AES key** (32 bytes) using a cryptographically secure random generator
2. Generate a **128-bit Initialization Vector (IV)** (16 bytes) - must be unique for each encryption
3. Choose the **segment size** (1, 8, or 16 bytes) based on your streaming requirements

**Step 1.2: Initialize the System**
1. Import required cryptographic libraries (`pycryptodome`)
2. Set up the AES cipher in ECB mode (for single block operations)
3. Prepare the feedback register with the IV
"""
)

st.code(
    """
from Crypto.Cipher import AES
import secrets

# Generate key and IV
key = secrets.token_bytes(32)  # 256-bit key
iv = secrets.token_bytes(16)   # 128-bit IV
segment_size = 16              # Choose segment size

# Initialize cipher
cipher = AES.new(key, AES.MODE_ECB)
""",
    language="python",
)

st.markdown("---")

# ------------------ Encryption Phase ------------------
st.subheader("🔒 Phase 2: CFB Encryption Process")

st.write(
    """
**Step 2.1: Prepare for Encryption**
1. Convert plaintext to bytes (e.g., UTF-8 encoding for text)
2. Initialize feedback register with IV
3. Prepare empty ciphertext buffer

**Step 2.2: Segment-by-Segment Encryption**
For each segment of plaintext:
1. **Encrypt feedback register**: `O = E(K, feedback_register)`
2. **XOR with plaintext**: `C = P ⊕ O[0:segment_size]`
3. **Update feedback register**: Shift left and append ciphertext
4. **Append to result**: Add ciphertext segment to output

**Step 2.3: Finalize Encryption**
1. Return complete ciphertext
2. Securely store or transmit IV alongside ciphertext (IV is not secret)
"""
)

st.code(
    """
def cfb_encrypt_step_by_step(plaintext_bytes, key, iv, segment_size):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b''
    feedback_register = iv
    
    print(f"Initial IV: {iv.hex()}")
    
    for i in range(0, len(plaintext_bytes), segment_size):
        # Step 1: Encrypt feedback register
        encrypted_feedback = cipher.encrypt(feedback_register)
        print(f"Encrypted feedback: {encrypted_feedback.hex()}")
        
        # Step 2: Get plaintext segment
        plaintext_segment = plaintext_bytes[i:i+segment_size]
        print(f"Plaintext segment: {plaintext_segment.hex()}")
        
        # Step 3: XOR operation
        ciphertext_segment = bytes(a ^ b for a, b in zip(plaintext_segment, encrypted_feedback))
        print(f"Ciphertext segment: {ciphertext_segment.hex()}")
        
        # Step 4: Update feedback register
        feedback_register = feedback_register[len(ciphertext_segment):] + ciphertext_segment
        if len(feedback_register) < 16:
            feedback_register += b'\\x00' * (16 - len(feedback_register))
        
        ciphertext += ciphertext_segment
        print(f"Updated feedback: {feedback_register.hex()}")
        print("---")
    
    return ciphertext
""",
    language="python",
)

st.markdown("---")

# ------------------ Decryption Phase ------------------
st.subheader("🔓 Phase 3: CFB Decryption Process")

st.write(
    """
**Step 3.1: Prepare for Decryption**
1. Ensure you have the same key and IV used for encryption
2. Initialize feedback register with the same IV
3. Prepare empty plaintext buffer

**Step 3.2: Segment-by-Segment Decryption**
For each segment of ciphertext:
1. **Encrypt feedback register**: `O = E(K, feedback_register)` *(same as encryption!)*
2. **XOR with ciphertext**: `P = C ⊕ O[0:segment_size]`
3. **Update feedback register**: Shift left and append received ciphertext
4. **Append to result**: Add plaintext segment to output

**Step 3.3: Finalize Decryption**
1. Convert decrypted bytes back to original format
2. Verify integrity if needed
"""
)

st.code(
    """
def cfb_decrypt_step_by_step(ciphertext_bytes, key, iv, segment_size):
    cipher = AES.new(key, AES.MODE_ECB)  # Same cipher as encryption!
    plaintext = b''
    feedback_register = iv  # Same IV as encryption
    
    print(f"Initial IV: {iv.hex()}")
    
    for i in range(0, len(ciphertext_bytes), segment_size):
        # Step 1: Encrypt feedback register (NOT decrypt!)
        encrypted_feedback = cipher.encrypt(feedback_register)
        print(f"Encrypted feedback: {encrypted_feedback.hex()}")
        
        # Step 2: Get ciphertext segment
        ciphertext_segment = ciphertext_bytes[i:i+segment_size]
        print(f"Ciphertext segment: {ciphertext_segment.hex()}")
        
        # Step 3: XOR operation
        plaintext_segment = bytes(a ^ b for a, b in zip(ciphertext_segment, encrypted_feedback))
        print(f"Plaintext segment: {plaintext_segment.hex()}")
        
        # Step 4: Update feedback register with received ciphertext
        feedback_register = feedback_register[len(ciphertext_segment):] + ciphertext_segment
        if len(feedback_register) < 16:
            feedback_register += b'\\x00' * (16 - len(feedback_register))
        
        plaintext += plaintext_segment
        print(f"Updated feedback: {feedback_register.hex()}")
        print("---")
    
    return plaintext
""",
    language="python",
)

st.markdown("---")

# ------------------ Testing Phase ------------------
st.subheader("🧪 Phase 4: Testing and Validation")

st.write(
    """
**Step 4.1: Unit Testing**
1. Test with known test vectors
2. Verify encryption/decryption round-trip
3. Test with different segment sizes
4. Test with various input lengths

**Step 4.2: Security Testing**
1. Verify IV uniqueness requirement
2. Test error propagation behavior
3. Validate that same plaintext with different IVs produces different ciphertext
4. Ensure no information leakage

**Step 4.3: Performance Testing**
1. Measure encryption/decryption speed
2. Test with large files
3. Compare different segment sizes
4. Memory usage analysis
"""
)

st.markdown("---")

# ------------------ Usage Guidelines ------------------
st.subheader("📋 Phase 5: Practical Usage Guidelines")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
    **✅ Do:**
    - Always use a unique IV for each encryption
    - Use cryptographically secure random generators
    - Store/transmit IV with ciphertext
    - Use appropriate segment sizes for your use case
    - Implement proper error handling
    - Use authenticated encryption in production
    """
    )

with col2:
    st.markdown(
        """
    **❌ Don't:**
    - Reuse IVs with the same key
    - Use predictable IVs
    - Ignore error propagation effects
    - Use for authentication without HMAC
    - Implement without proper testing
    - Use weak keys or short keys
    """
    )

st.markdown("---")

st.subheader("🎯 Summary of Key Procedures")

st.info(
    """
**Quick Reference:**
1. **Setup**: Generate key (32 bytes) and IV (16 bytes)
2. **Encrypt**: `C = P ⊕ E(K, feedback_register)`, update feedback with C
3. **Decrypt**: `P = C ⊕ E(K, feedback_register)`, update feedback with C  
4. **Key Point**: Both encryption and decryption use the cipher's ENCRYPT function
5. **Security**: Always use unique IVs and secure key management
"""
)

st.success(
    "🚀 **Ready to implement?** Head to the Simulation page to try the interactive CFB implementation!"
)
