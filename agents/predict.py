from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# 1. Load a lightweight OCR predictor (detection + recognition)
# mintee variant: smaller/faster model
model = ocr_predictor(det_arch="db_mobilenet_v3_large", reco_arch="crnn_mobilenet_v3_small", pretrained=True)

# 2. Load a document (PDF or images)
# doc = DocumentFile.from_pdf("input/contract.pdf")   # or .from_images(["page1.png", "page2.png"])
doc = DocumentFile.from_images(["input/201.png","input/202.png","input/203.png"])

# 3. Run OCR
result = model(doc)

# 4. Export results as text
text_output = result.render()   # plain text
print(text_output)

# Or structured JSON with bounding boxes
json_output = result.export()
# print(json_output)
