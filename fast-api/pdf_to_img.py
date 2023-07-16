import pypdfium2 as pdfium


def pdf_to_image(pdf_name, IMAGES_DIR):
    pdf = pdfium.PdfDocument(pdf_name)
    n_pages = len(pdf)

    for page_number in range(n_pages):
        page = pdf.get_page(page_number)

        scale_value = 3
        pil_image = page.render_to(
            pdfium.BitmapConv.pil_image,
            scale = scale_value,
            rotation = 0,
            fill_colour=(255, 255, 255, 255),
            crop=(0, 0, 0, 0),
            greyscale=False,
            optimise_mode=pdfium.OptimiseMode.NONE,)

        imagename = IMAGES_DIR + str(page_number + 1) + ".png"
        print(imagename)
        pil_image.save(imagename)
        return imagename
        
# pdf_to_image('junks\\Attention is all u need.pdf')