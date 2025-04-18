import streamlit as st
import nbformat
import os
from io import BytesIO
from PIL import Image
import tempfile
from pdf2docx import Converter
from PyPDF2 import PdfMerger
import streamlit.components.v1 as components
import moviepy.editor as mp

st.set_page_config(page_title="ToolFusion: Convert, Resize, Record & PDFs", layout="wide")
st.title("ToolFusion: Convert, Resize, Record & PDFs")

# --- First Row: Notebook Converter & Image Resizer ---
col1, col2 = st.columns(2)

# Left Column: Notebook-to-Script Converter
with col1:
    st.header("📝 Notebook to Script Converter")
    uploaded_nb = st.file_uploader(
        "Upload a Jupyter Notebook (.ipynb)",
        type=["ipynb"],
        key="notebook_uploader"
    )
    if uploaded_nb is not None:
        try:
            notebook = nbformat.read(uploaded_nb, as_version=4)
            code_cells = [cell["source"] for cell in notebook.cells if cell["cell_type"] == "code"]
            code_str = "\n\n".join(code_cells)
            if not code_str.strip():
                st.warning("No code cells found in the notebook!")
            else:
                py_buffer = BytesIO()
                py_buffer.write(code_str.encode("utf-8"))
                py_buffer.seek(0)
                fname = os.path.splitext(uploaded_nb.name)[0] + ".py"
                st.success("Notebook converted successfully!")
                st.download_button(
                    label="📥 Download Python Script",
                    data=py_buffer,
                    file_name=fname,
                    mime="text/x-python"
                )
        except Exception as e:
            st.error(f"❌ Failed to convert notebook: {e}")

# Right Column: Image Resizer
with col2:
    st.header("🖼️ Image Resizer")
    uploaded_img = st.file_uploader(
        "Upload an image to resize",
        type=["png", "jpg", "jpeg", "bmp", "gif"],
        key="image_uploader"
    )
    if uploaded_img:
        image = Image.open(uploaded_img)
        st.image(image, caption="Original Image", use_column_width=True)
        new_w = st.number_input("New width (px)", min_value=1, value=image.width, step=1)
        new_h = st.number_input("New height (px)", min_value=1, value=image.height, step=1)
        if st.button("🔄 Resize Image", key="resize_btn"):
            resized = image.resize((new_w, new_h))
            st.image(resized, caption="Resized Image", use_column_width=True)
            buf = BytesIO()
            resized.save(buf, format="PNG")
            buf.seek(0)
            base, _ = os.path.splitext(uploaded_img.name)
            out_name = f"{base}_{new_w}x{new_h}.png"
            st.download_button(
                label="📥 Download Resized Image",
                data=buf,
                file_name=out_name,
                mime="image/png"
            )

# --- Second Row: Image Format & PDF to DOCX Converters ---
st.markdown("---")
col3, col4 = st.columns(2)

# Left of Second Row: Image Format Converter
with col3:
    st.header("🔄 Image Format Converter")
    uploaded_img2 = st.file_uploader(
        "Upload an image to convert format",
        type=["png", "jpg", "jpeg", "bmp", "gif", "tiff", "webp"],
        key="format_uploader"
    )
    if uploaded_img2:
        img2 = Image.open(uploaded_img2)
        st.image(img2, caption="Original Image", use_column_width=True)
        choices = ["PNG", "JPEG", "GIF", "BMP", "TIFF", "WEBP"]
        out_fmt = st.selectbox("Select output format", choices)
        if st.button("🔄 Convert Image Format", key="format_btn"):
            buf2 = BytesIO()
            img2.save(buf2, format=out_fmt)
            buf2.seek(0)
            base, _ = os.path.splitext(uploaded_img2.name)
            out_name2 = f"{base}.{out_fmt.lower()}"
            st.download_button(
                label="📥 Download Converted Image",
                data=buf2,
                file_name=out_name2,
                mime=f"image/{out_fmt.lower()}"
            )

# Right of Second Row: PDF to DOCX Converter
with col4:
    st.header("📄 PDF to DOCX Converter")
    uploaded_pdf = st.file_uploader(
        "Upload a PDF to convert to DOCX",
        type=["pdf"],
        key="pdf_uploader"
    )
    if uploaded_pdf:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_in:
                tmp_in.write(uploaded_pdf.read())
                in_path = tmp_in.name
            out_path = in_path.replace(".pdf", ".docx")
            cv = Converter(in_path)
            cv.convert(out_path)
            cv.close()
            with open(out_path, "rb") as f:
                docx_bytes = f.read()
            out_name3 = os.path.splitext(uploaded_pdf.name)[0] + ".docx"
            st.download_button(
                label="📥 Download DOCX",
                data=docx_bytes,
                file_name=out_name3,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"❌ PDF conversion failed: {e}")

# --- Third Row: PDF Merger & Images-to-PDF ---
st.markdown("---")
col5, col6 = st.columns(2)

# Merge PDFs
with col5:
    st.header("🔗 Merge PDF Files")
    uploaded_pdfs = st.file_uploader(
        "Upload PDF files to merge",
        type=["pdf"],
        accept_multiple_files=True,
        key="merge_pdfs"
    )
    if uploaded_pdfs:
        try:
            merger = PdfMerger()
            for pdf_file in uploaded_pdfs:
                merger.append(pdf_file)
            pdf_buffer = BytesIO()
            merger.write(pdf_buffer)
            merger.close()
            pdf_buffer.seek(0)
            st.download_button(
                label="📥 Download Merged PDF",
                data=pdf_buffer,
                file_name="merged.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"❌ Failed to merge PDFs: {e}")

# Images to PDF
with col6:
    st.header("📷 Images to PDF Converter")
    uploaded_imgs = st.file_uploader(
        "Upload images to convert to PDF",
        type=["png", "jpg", "jpeg", "bmp", "gif", "tiff", "webp"],
        accept_multiple_files=True,
        key="images_to_pdf"
    )
    if uploaded_imgs:
        try:
            imgs = [Image.open(img).convert("RGB") for img in uploaded_imgs]
            pdf_bytes = BytesIO()
            imgs[0].save(
                pdf_bytes,
                format="PDF",
                save_all=True,
                append_images=imgs[1:]
            )
            pdf_bytes.seek(0)
            st.download_button(
                label="📥 Download Images as PDF",
                data=pdf_bytes,
                file_name="images_to_pdf.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"❌ Failed to convert images to PDF: {e}")
# --- Fifth Row: WebM to MP4 Converter ---
st.markdown("---")
st.header("🎬 WebM to MP4 Converter")

uploaded_webm = st.file_uploader(
    "Upload a WebM video to convert to MP4",
    type=["webm"],
    key="webm_uploader"
)

if uploaded_webm:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(uploaded_webm.read())
        webm_path = tmp.name
    try:
        clip = mp.VideoFileClip(
            webm_path,
            ffmpeg_params=["-probesize", "100M", "-analyzeduration", "100M"]
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp2:
            mp4_path = tmp2.name
        clip.write_videofile(mp4_path, codec="libx264", audio_codec="aac")
        clip.close()
        with open(mp4_path, "rb") as f:
            mp4_bytes = f.read()
        out_name = os.path.splitext(uploaded_webm.name)[0] + ".mp4"
        st.download_button(
            label="📥 Download MP4",
            data=mp4_bytes,
            file_name=out_name,
            mime="video/mp4"
        )
    except Exception as e:
        st.error(f"❌ Conversion failed: {e}")

# --- Fourth Row: Screen Recorder ---
st.markdown("---")
st.header("📹 Screen Recorder")

components.html("""
<style>
  #startBtn, #stopBtn {
    font-size: 16px;
    padding: 10px 20px;
    margin: 10px 10px 10px 0;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s ease;
  }
  #startBtn {
    background-color: #4CAF50;
    color: white;
  }
  #startBtn:hover {
    background-color: #45a049;
  }
  #stopBtn {
    background-color: #f44336;
    color: white;
  }
  #stopBtn:hover {
    background-color: #da190b;
  }
  #player {
    width: 100%;
    max-height: 300px;
    border-radius: 12px;
    margin-bottom: 10px;
  }
  a[download] {
    display: inline-block;
    margin-top: 15px;
    background: #0066cc;
    color: white;
    padding: 10px 15px;
    text-decoration: none;
    border-radius: 6px;
    font-weight: 600;
  }
  a[download]:hover {
    background: #0055aa;
  }
</style>

<video id="player" controls></video><br/>
<button id="startBtn">Start Recording</button>
<button id="stopBtn" disabled>Stop Recording</button>

<script>
  const startBtn = document.getElementById('startBtn');
  const stopBtn = document.getElementById('stopBtn');
  const player = document.getElementById('player');
  let mediaRecorder;
  let recordedChunks = [];

  startBtn.onclick = async () => {
    const stream = await navigator.mediaDevices.getDisplayMedia({ video: true, audio: true });
    player.srcObject = stream;
    mediaRecorder = new MediaRecorder(stream);
    recordedChunks = [];

    mediaRecorder.ondataavailable = e => {
      if (e.data.size > 0) recordedChunks.push(e.data);
    };

    mediaRecorder.onstop = () => {
      const blob = new Blob(recordedChunks, { type: 'video/webm' });
      const url = URL.createObjectURL(blob);
      player.srcObject = null;
      player.src = url;

      const dl = document.createElement('a');
      dl.href = url;
      dl.download = 'recording.webm';
      dl.textContent = '📥 Download Recording';
      document.body.appendChild(dl);
    };

    mediaRecorder.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;
  };

  stopBtn.onclick = () => {
    mediaRecorder.stop();
    startBtn.disabled = false;
    stopBtn.disabled = true;
  };
</script>
""", height=420)

 
