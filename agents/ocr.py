from doctr.io import DocumentFile
from doctr.models import ocr_predictor

class OCRProcessor:
    def __init__(self) -> None:
        # 1. Load a lightweight OCR predictor (detection + recognition)
        # mintee variant: smaller/faster model
        self.model = ocr_predictor(det_arch="db_mobilenet_v3_large", reco_arch="crnn_mobilenet_v3_small", pretrained=True)

    def read_image_list(self, images):
        # 2. Load a document (PDF or images)
        # doc = DocumentFile.from_images(["page1.png", "page2.png"])
        doc = DocumentFile.from_images(images)
        # 3. Run OCR
        self.result = self.model(doc)

    def read_pdf(self, pdf):
        # ="input/contract.pdf"
        doc = DocumentFile.from_pdf(pdf)
        self.result = self.model(doc)

    def render_text(self):
        # 4. Export results as text
        text_output = self.result.render()   # plain text
        return text_output

    def render_blocks(self):
        # Or structured JSON with bounding boxes
        json_output = self.result.export()
        return json_output
