# CFB (Cipher Feedback) Mode Implementation

## Overview
This project demonstrates the implementation of **CFB (Cipher Feedback) mode**, one of the standard block cipher modes of operation. CFB mode converts block ciphers into stream ciphers, enabling encryption of variable-length data streams.

## Features
- 🔐 **Complete CFB Implementation**: Full encryption and decryption algorithms
- 🎯 **Interactive Simulation**: Web-based GUI for hands-on learning
- 📊 **Educational Content**: Comprehensive theory and step-by-step procedures
- 📁 **File Operations**: Encrypt and decrypt files of any size
- 🔧 **Configurable Parameters**: Variable segment sizes and secure key generation
- 🎓 **Learning Focused**: Designed for educational purposes with detailed explanations

## Project Structure
```
├── Home.py                 # Main landing page
├── pages/
│   ├── 1_Introduction.py   # CFB mode introduction and applications
│   ├── 2_Objective.py      # Project objectives and learning outcomes
│   ├── 3_Theory.py         # Mathematical theory and core concepts
│   ├── 4_Simulation.py     # Interactive CFB encryption/decryption tool
│   ├── 5_Procedure.py      # Step-by-step implementation guide
│   └── 6_Conclusion.py     # Summary and practical applications
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd CFB-Mode-Implementation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run Home.py
   ```

## Dependencies
- **streamlit**: Web application framework
- **pycryptodome**: Cryptographic library for AES implementation
- **numpy**: Numerical computations

## Key Features

### 🔐 CFB Mode Implementation
- **AES-256 encryption**: Uses industry-standard Advanced Encryption Standard
- **Variable segment sizes**: Support for 1, 8, or 16-byte segments
- **Secure key generation**: Cryptographically secure random key and IV generation
- **Stream cipher behavior**: Processes data of arbitrary length

### 🎓 Educational Components
- **Theory Section**: Mathematical foundations and algorithm explanation
- **Interactive Simulation**: Real-time encryption/decryption with visual feedback
- **Step-by-step Procedure**: Detailed implementation guide
- **Security Considerations**: Best practices and common pitfalls

### 💻 Practical Applications
- **Text Encryption**: Encrypt and decrypt messages
- **File Operations**: Handle files of any size and format
- **Round-trip Verification**: Automatic verification of encryption/decryption cycles
- **Parameter Experimentation**: Try different segment sizes and observe effects

## How CFB Mode Works

CFB (Cipher Feedback) mode transforms a block cipher into a stream cipher:

1. **Initialization**: Uses an Initialization Vector (IV) to start the process
2. **Feedback Loop**: Each ciphertext block feeds back into the next encryption step
3. **Stream Processing**: Can handle data of any length without padding
4. **Self-Synchronizing**: Automatically recovers from transmission errors

### Key Characteristics:
- ✅ **No Padding Required**: Unlike CBC mode
- ✅ **Real-time Processing**: Encrypt data as it arrives
- ✅ **Error Recovery**: Self-synchronizing property
- ⚠️ **Sequential Encryption**: Cannot parallelize encryption (but can parallelize decryption)

## Security Notes

⚠️ **Important**: This implementation is for educational purposes. For production use:
- Use authenticated encryption (e.g., GCM mode)
- Implement proper key management
- Add integrity verification (HMAC)
- Follow security best practices

## Usage Examples

### Text Encryption
1. Navigate to the "Simulation" page
2. Enter text in the encryption tab
3. Click "Encrypt Text" to see the CFB encryption in action
4. Switch to decryption tab to recover the original text

### File Operations
1. Go to the "File Operations" tab in the simulation
2. Upload any file for encryption
3. Download the encrypted file
4. Upload the encrypted file back to decrypt and recover the original

## Learning Outcomes

After completing this project, you will understand:
- Block cipher modes of operation
- The difference between block and stream ciphers
- Initialization vectors and their importance
- Error propagation in cryptographic systems
- Practical cryptographic implementation
- Security considerations in cipher mode design

## Contributing
This is an educational project. Feel free to:
- Suggest improvements to the explanation
- Add additional cipher modes for comparison
- Enhance the user interface
- Add more comprehensive testing

## License
Educational use - please refer to your institution's guidelines for academic projects.

**Create virtual environment:**

```sh
uv venv
```

**Install streamlit:**

```sh
uv pip install streamlit
```

**Run:**

```sh
streamlit run app.py
```
