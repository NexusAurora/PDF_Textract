# README.md

## AI-Based EOB Document Processing System  

This project is designed to process Explanation of Benefits (EOB) documents using AI and cloud-based APIs. The system extracts critical information from PDF documents, structures the data, and provides a clean, accurate output. The extracted fields enable healthcare providers to efficiently manage payments and insurance coverage data.

---

### **Features**  
The system extracts the following key fields(Parameters) from EOB documents:  
- **Payment to:** Recipient of the payment.  
- **Payment Date:** Date when the payment was made.  
- **Payment Number:** Unique identifier for the payment.  
- **Total Amount Charged:** Amount billed for the services.  
- **Total Contracted Amount:** Agreed amount as per the insurance contract.  
- **Amount Eligible for Coverage:** Amount covered by insurance.  
- **Patient Name:** Name of the patient.  
- **Patient ID:** Unique identifier for the patient.  
- **Service Provider ID:** Unique identifier for the service provider.  

---

### **Solution Overview**  
The solution uses **AWS Textract** for Optical Character Recognition (OCR) and text extraction. It processes both sequential text and tabular data efficiently.  

#### **Steps Implemented**  
1. **Preprocessing**  
   - Split multi-page PDFs into individual pages for ease of processing.  
   - Ensure proper handling of new-line-sensitive data.  

2. **OCR and Data Extraction**  
   - Utilize AWS Textract for text and table recognition.  
   - Extract structured data using regex patterns and table mapping logic.  

3. **Post-Processing**  
   - Clean and structure the extracted data.  
   - Handle multiline entries (e.g., `Patient ID` and `Service Provider ID`).  
   - Merge data from multiple pages.  

---

### **Tools and Technologies**  
- **AWS Textract:** Cloud-based OCR for text and table extraction.  
- **Python 3.10:** Primary programming language.  
- **PyPDF2:** Library for splitting and managing PDF files.  
- **Regex:** For pattern matching and text extraction.  

### **Libraries Used**
- **boto3: This library is like a bridge that connects our Python code to AWS services. I use it to interact with AWS Textract, which helps us read text from images and PDFs.

- **os: Think of this as a toolset for interacting with computer's operating system. It helps us navigate through files and directories, and perform tasks like creating, deleting, or moving files.

- **shutil: This library is a handy helper for high-level file operations. It allows us to copy, move, or delete files and directories with ease.

- **re: Short for "regular expressions," this library is like a powerful search tool. It helps us find and extract specific patterns of text from the data we process.

- **PyPDF2: This library is our go-to for working with PDF files. It allows us to split multi-page PDFs into individual pages, making it easier to process each page separately.
---

### **How to Run the Project**  
1. **Install Dependencies(from CMD)**  
   Use the provided `requirements.txt` file to set up the environment:  
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up AWS Credentials**  
   Configure AWS credentials to enable Textract API access:  
   ```bash
   aws configure
   ```

3. **Execute the Code**  
   Run the script to process an EOB PDF:  
   ```bash
   python main.py
   ```

4. **Input and Output**  
   - **Input:** EOB PDF document.  
   - **Output:** JSON file containing structured data.  

---

### **Deliverables**  
1. **AI Pipeline**  
   - A Python-based pipeline that processes any EOB PDF and extracts the specified data points.  

2. **Approach Document**  
   - Detailed explanation of methodology:  
     - **Preprocessing:** Splitting PDFs and handling multi-line text.  
     - **OCR:** Using AWS Textract to extract structured data.  
     - **Post-Processing:** Cleaning, mapping, and validating extracted data.  
   - Steps to ensure accuracy, including regex-based validation and fallback mechanisms for missing fields.  

3. **Accuracy Measures**  
   - Cross-validation of extracted fields.  
   - Handling line breaks and table inconsistencies to ensure completeness.  

---

### **Detailed Step-by-Step Procedure**

#### **1. Preprocessing**
- **Splitting PDFs:** Use `PyPDF2` to split multi-page PDFs into individual pages. This makes it easier to process each page separately.
- **Handling New-Line Sensitive Data:** Ensure that data which spans multiple lines is correctly handled. This involves checking for line breaks and concatenating lines where necessary.

#### **2. OCR and Data Extraction**
- **Using AWS Textract:** First call the AWS Textract API to perform OCR on each page. This extracts both freeform(sequential) text and tabular data.
- **Extracting Structured Data:** Use regular expressions (regex) to identify and extract specific fields from the OCR output. This includes mapping table data to the corresponding fields.

#### **3. Post-Processing**
- **Cleaning Data:** Remove any extraneous characters or formatting issues from the extracted data.
- **Handling Multiline Entries:** Ensure that fields like `Patient ID` and `Service Provider ID` which may span multiple lines are correctly merged.
- **Merging Data:** Combine data from multiple pages into a single structured output.

- *Note: There are two Python files to execute these operations, where the actual raw code is in the extract.py file and the main.py file will call the extract.py file.
---

### **Acknowledgments**  
This project was developed by **Sayanti Chatterjee**.  
