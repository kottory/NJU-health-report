import ddddocr

def detect(input):
    ocr = ddddocr.DdddOcr(show_ad=0)
    with input as f:
        res = ocr.classification(f.read())
    return res