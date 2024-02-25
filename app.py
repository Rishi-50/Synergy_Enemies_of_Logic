import streamlit as st
from PIL import Image, ImageOps
import requests
import tempfile
import fitz
import io
from pdf2image import convert_from_bytes
from io import BytesIO
# import base64


# Define functions for OCR, file classification, manual review, and data extraction

def ocr(image):
    # Implement OCR logic
    # Here's a simple example using pytesseract
    import pytesseract
    text = pytesseract.image_to_string(image)
    return text

def classify_files(files):
    # Implement file classification logic
    pass

def manual_review(file_data):
    # Implement manual review interface
    pass

def data_extraction(file):
    # Implement data extraction and labeling logic
    pass


# file_data = io.BytesIO(b64decode(image_base))

# Convert PDF to image
def pdf_to_image(pdf_bytes):
    # pdf_images = convert_from_bytes(io.BytesIO(base64.b64decode(pdf_bytes)))

    images = []
    with fitz.open(pdf_bytes) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_bytes = page.get_pixmap().tobytes()
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
    return images


def annotate_pdf(pdf_bytes):
    # Convert PDF to images
    pdf_images = convert_from_bytes(pdf_bytes)
 
    # Display PDF pages for annotation
    for i, pdf_image in enumerate(pdf_images):
        st.image(pdf_image, caption=f"Page {i+1}")
 
        # Annotation using Streamlit canvas
        with st.beta_expander(f"Annotate Page {i+1}"):
            draw = st.image(pdf_image, caption=f"Page {i+1}", use_container_width=True).draw_image()
 
            # Your annotation logic here, for example:
            draw.line([(10, 10), (100, 10)], width=5, color='red')
 
            # Save the annotated image
            annotated_image = Image.fromarray(draw.to_rgba())
            st.image(annotated_image, use_container_width=True)
 
    # Save the annotated PDF
    annotated_pdf = BytesIO()
    pdf_images[0].save(annotated_pdf, save_all=True, append_images=pdf_images[1:])
    return annotated_pdf.getvalue()
 

# Define Streamlit app
def main():
    # CSS styling
    st.markdown(
        """
        <style>
            body {
                background-color: #f0f0f0;
            }
            .sidebar .sidebar-content {
                background-color: #3366ff;
                color: white;
            }
            .sidebar .sidebar-content .block-container {
                color: white;
            }
            .stRadio > div > label > div {
                color: black;
            }
            .stButton>button {
                background-color: #3366ff;
                color: white;
            }
            .stButton>button:hover {
                background-color: #2541b2;
            }
            .stTextInput>div>div>input {
                background-color: #ffffff;
                color: #000000;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title('Construction File Organization & Information Extraction')

    # Sidebar (navbar)
    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['Home', 'Upload File', 'Manual Review'])

    if page == 'Home':
        st.header('Welcome to Construction File Management App')
        # Add description and features

    elif page == 'Upload File':
        st.header('Upload File')

        # Upload file button
        uploaded_file = st.file_uploader("Upload File", type=['pdf', 'jpg', 'png'])

        if uploaded_file:
            if uploaded_file.type == 'application/pdf':
                pdf_images = pdf_to_image(uploaded_file)
                for i, image in enumerate(pdf_images):
                    st.image(image, caption=f'Page {i+1} from PDF', use_column_width=True)
            else:
                image = Image.open(uploaded_file)
                st.image(image, caption='Uploaded Image', use_column_width=True)

                # OCR button
                if st.button('Perform OCR'):
                    ocr_result = ocr(image)
                    st.write('OCR Result:', ocr_result)

    elif page == 'Manual Review':
        st.header('Manual Review and Annotations')

        # Display uploaded file
        uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
 
        if uploaded_files:
            st.header("Uploaded PDFs:")
            for file in uploaded_files:
                st.write(file.name)
    
            if st.button("Annotate PDF"):
                for file in uploaded_files:
                    annotated_pdf = annotate_pdf(file.read())
                    st.download_button(f"Download Annotated {file.name}", annotated_pdf, file_name=f"annotated_{file.name}", key=f"annotated_{file.name}")



if __name__ == '__main__':
    main()


