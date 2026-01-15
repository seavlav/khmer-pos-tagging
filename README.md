# Khmer Joint Word Segmentation & POS Tagging System

## 1. About the project
Khmer, the official language of Cambodia, presents unique challenges for natural language processing (NLP). 
Unlike English, Khmer text does not consistently use spaces to separate words, making word segmentation a prerequisite for most NLP tasks. Additionally, 
Part-of-Speech (POS) tagging—assigning grammatical labels like noun, verb, or adjective to each word—is crucial for syntactic and semantic understanding.

## 2. problem Statement:
**1.Word Segmentation Challenge:** Khmer text is written continuously without spaces between words. A naive whitespace-based tokenization fails.

**2.POS Tagging Challenge:** POS tagging in Khmer is challenging due to morphological complexity and limited annotated corpora.

### **The goal of this project:** 
we propose a joint **Word Segmentation and POS Tagging system** specifically designed for Khmer, leveraging deep learning
techniques to achieve accurate and efficient processing.

## 3.Methodology
This system is a character-level BiLSTM neural network designed to perform word segmentation and 
POS tagging for Khmer text simultaneously.

### **1. Encoder (BiLSTM)**
The core of the system is a Bidirectional LSTM (BiLSTM) that processes text at the character level.
This is crucial for Khmer, where words may contain complex clusters and zero-width spaces.

**_Embedding Dimension: 128**

Each character is mapped to a 128-dimensional vector to capture semantic and orthographic properties.

**_Hidden Units: 256 per direction (forward + backward = 512)**

The BiLSTM combines past and future context for each character, producing a 512-dimensional context-aware representation.

For each character x(t), the BiLSTM outputs a hidden state:
**h_t = [forward_hidden_t ; backward_hidden_t]**
### **2. Dual-Head Output**

The BiLSTM encoder feeds into two separate output heads, enabling the model to perform joint 
prediction of word segmentation and POS tagging.

**a. Segmentation Head (y_seg)**

The first, the Segmentation Head (y_seg), is a binary classifier that identifies word boundaries 
for each character, labeling them as B (Beginning of a word) or 
I (Inside a word). This head allows the model to learn where words start and end,
effectively handling ambiguous or compound words in Khmer text

**b. POS Head (y_pos)**

The second, the POS Head (y_pos), is a multi-class classifier that assigns 
one of 13 grammatical categories—such as Noun, Verb, or 
Adjective—to each character. By providing syntactic information, the POS head reinforces 
segmentation predictions and improves overall accuracy, enabling the system to jointly model both tasks in a single, 
context-aware framework.

## 4. System Archicture 

### **1. Frontend**

The frontend provides a user-friendly interface for text input and output visualization.

**Responsive UI**: Built with Vanilla JavaScript and CSS3 to adapt to different screen sizes and devices.

**Input Handling**: Accepts raw Khmer text from users and sends it to the backend API.

**Output Visualization**: Displays segmented words and POS tags in a clear, readable format.

**Interface	URL**

Web UI	http://localhost

API Documentation	http://localhost:8000/docs

Direct API	http://localhost:8000

### **2. Backend**

The backend serves as the bridge between the frontend and the inference engine. 
It Built with FastAPI, leveraging asynchronous request handling for low-latency inference.

### **3. inference Engine**

**Model Loading**: Initializes and loads the trained BiLSTM model into memory for fast inference.

**Character-to-Tensor Mapping**: Converts raw Khmer characters into tensor representations compatible with the neural network.

**BiLSTM Inference**: Processes the character tensors through the BiLSTM encoder to generate contextual embeddings.

**Dual-Head Prediction**: Produces segmentation labels (B/I) and POS tags for each character simultaneously.

## 5. Deployment

The entire environment—including Python libraries like PyTorch and web servers like Nginx is containerized.
Code:

**Clone the repository**
'git clone https://github.com/your-team/khmer-pos-tagging.git'

**Move to the root directory**
'cd khmer-pos-tagging'

**Launch the services**
'docker-compose up --build'

###  Result: 

Sample of our interface and Prediction after connect to docker
<img width="1157" height="898" alt="image" src="https://github.com/user-attachments/assets/c82c10b3-50cc-4460-98a3-bfa94b0cbeda" />

















