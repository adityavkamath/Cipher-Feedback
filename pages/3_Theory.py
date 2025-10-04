import streamlit as st

st.set_page_config(page_title="Theory", layout="wide")
st.header("CFB Mode Theory")

st.write("""
### Block Ciphers vs Stream Ciphers

**Block Ciphers** (like AES) encrypt fixed-size blocks of data (typically 128 bits). 
**Stream Ciphers** encrypt data bit-by-bit or byte-by-byte. 

CFB mode converts a block cipher into a stream cipher, allowing encryption of arbitrary-length data.
""")

st.markdown("---")

# ------------------ CFB Encryption Process ------------------
st.subheader("🔐 CFB Encryption Process")

st.write("""
CFB mode uses the block cipher in **encryption mode only** for both encryption and decryption.
The plaintext is XORed with the output of the encrypted feedback register.
""")

st.markdown("""
**Mathematical Representation:**

For encryption:
- **I₁ = IV** (Initialization Vector)
- **O₁ = E(K, I₁)** (Encrypt the IV with key K)
- **C₁ = P₁ ⊕ O₁** (XOR plaintext with encrypted output)
- **I₂ = C₁** (Feedback: use ciphertext as next input)

For subsequent blocks:
- **Iᵢ = Cᵢ₋₁** (Previous ciphertext becomes next input)  
- **Oᵢ = E(K, Iᵢ)** (Encrypt the input)
- **Cᵢ = Pᵢ ⊕ Oᵢ** (XOR plaintext with encrypted output)

Where:
- **E(K, X)** = Block cipher encryption with key K
- **P** = Plaintext block
- **C** = Ciphertext block  
- **I** = Input to block cipher
- **O** = Output from block cipher
- **⊕** = XOR operation
""")

st.markdown("---")

# ------------------ CFB Decryption Process ------------------
st.subheader("🔓 CFB Decryption Process")

st.write("""
CFB decryption uses the **same block cipher encryption** (not decryption) function.
This is because we XOR the ciphertext with the encrypted feedback register.
""")

st.markdown("""
**Mathematical Representation:**

For decryption:
- **I₁ = IV** (Same initialization vector)
- **O₁ = E(K, I₁)** (Encrypt the IV - same as encryption)
- **P₁ = C₁ ⊕ O₁** (XOR ciphertext with encrypted output)
- **I₂ = C₁** (Feedback: use received ciphertext)

For subsequent blocks:
- **Iᵢ = Cᵢ₋₁** (Previous ciphertext)
- **Oᵢ = E(K, Iᵢ)** (Encrypt the input)  
- **Pᵢ = Cᵢ ⊕ Oᵢ** (XOR ciphertext with encrypted output)
""")

st.markdown("---")

# ------------------ Key Properties ------------------
st.subheader("🔑 Key Properties of CFB Mode")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Advantages:**
    - ✅ **Stream Processing**: Can encrypt data of any length
    - ✅ **Self-Synchronizing**: Recovers from bit errors
    - ✅ **Real-time**: Encrypts data as it arrives
    - ✅ **No Padding**: No need to pad data to block size
    - ✅ **Parallel Decryption**: Can decrypt in parallel
    """)

with col2:
    st.markdown("""
    **Considerations:**
    - ⚠️ **Sequential Encryption**: Must encrypt sequentially
    - ⚠️ **Error Propagation**: Bit errors affect multiple blocks
    - ⚠️ **IV Uniqueness**: Requires unique IV for each encryption
    - ⚠️ **Malleable**: Vulnerable to bit-flipping attacks
    """)

st.markdown("---")

# ------------------ Implementation Functions ------------------
st.subheader("🔹 Core CFB Functions")

st.markdown("""
```python
def cfb_encrypt(plaintext, key, iv, block_size=16):
    '''
    CFB mode encryption
    
    Args:
        plaintext: Data to encrypt (bytes)
        key: Encryption key (bytes)
        iv: Initialization vector (bytes)
        block_size: Block size in bytes (default: 16 for AES)
    
    Returns:
        Encrypted ciphertext (bytes)
    '''
    cipher = AES.new(key, AES.MODE_ECB)  # Use ECB for single block encryption
    ciphertext = b''
    feedback = iv
    
    for i in range(0, len(plaintext), block_size):
        # Encrypt the feedback register
        encrypted_feedback = cipher.encrypt(feedback)
        
        # Get current plaintext block
        plaintext_block = plaintext[i:i+block_size]
        
        # XOR plaintext with encrypted feedback
        ciphertext_block = bytes(a ^ b for a, b in zip(plaintext_block, encrypted_feedback))
        ciphertext += ciphertext_block
        
        # Update feedback register with ciphertext
        feedback = ciphertext_block + feedback[len(ciphertext_block):]
    
    return ciphertext
```

```python
def cfb_decrypt(ciphertext, key, iv, block_size=16):
    '''
    CFB mode decryption
    
    Args:
        ciphertext: Data to decrypt (bytes)
        key: Decryption key (bytes)  
        iv: Initialization vector (bytes)
        block_size: Block size in bytes (default: 16 for AES)
    
    Returns:
        Decrypted plaintext (bytes)
    '''
    cipher = AES.new(key, AES.MODE_ECB)  # Same as encryption!
    plaintext = b''
    feedback = iv
    
    for i in range(0, len(ciphertext), block_size):
        # Encrypt the feedback register (same as encryption)
        encrypted_feedback = cipher.encrypt(feedback)
        
        # Get current ciphertext block
        ciphertext_block = ciphertext[i:i+block_size]
        
        # XOR ciphertext with encrypted feedback
        plaintext_block = bytes(a ^ b for a, b in zip(ciphertext_block, encrypted_feedback))
        plaintext += plaintext_block
        
        # Update feedback register with received ciphertext
        feedback = ciphertext_block + feedback[len(ciphertext_block):]
    
    return plaintext
```
""")

st.info("🔍 **Key Insight**: CFB decryption uses the block cipher's **encryption** function, not decryption!")

st.markdown("---")

st.subheader("📊 Security Considerations")

st.markdown("""
1. **IV Uniqueness**: Each encryption must use a unique IV to prevent identical plaintext blocks from producing identical ciphertext.

2. **Error Propagation**: A single bit error in ciphertext affects the current block and shifts the error to subsequent blocks until it "falls out" of the feedback register.

3. **Bit-flipping Attacks**: Attackers can flip specific bits in the ciphertext to cause predictable changes in the plaintext.

4. **Parallel Processing**: While encryption must be sequential, decryption can be parallelized since each block depends only on the previous ciphertext block.
""")

st.markdown("---")

st.subheader("🔄 CFB Mode Diagram")

st.write("""
**Encryption Flow:**
```
IV → [Block Cipher] → Output₁
                        ↓ (XOR)
Plaintext₁ → → → → Ciphertext₁
                        ↓ (Feedback)
Ciphertext₁ → [Block Cipher] → Output₂  
                        ↓ (XOR)
Plaintext₂ → → → → Ciphertext₂
```

**Decryption Flow:**
```
IV → [Block Cipher] → Output₁
                        ↓ (XOR)
Ciphertext₁ → → → → Plaintext₁
     ↓ (Feedback)
[Block Cipher] → Output₂
     ↓ (XOR)
Ciphertext₂ → → → → Plaintext₂
```
""")

st.success("✨ **Notice**: The same block cipher encryption operation is used for both encryption and decryption!")