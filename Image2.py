from PIL import Image

def simplificar_colores(ruta_imagen, num_colores, nueva_resolucion):
    im = Image.open(ruta_imagen)

    im_resized = im.resize(nueva_resolucion, Image.LANCZOS)

    out = im_resized.convert('P', palette=Image.ADAPTIVE, colors=num_colores)

    return out



def leer_pixeles(imagen):
    
    pixeles = imagen.load()

    ancho, alto = imagen.size
    palette = imagen.getpalette()

    num_colores = len(palette) // 3

    paleta = []
    for i in range(num_colores):
        r = palette[i * 3]
        g = palette[i * 3 + 1]
        b = palette[i * 3 + 2]
        color = (r,g,b)
        paleta.append(color)

    nonograma = []

    for y in range(alto):
        row = []
        for x in range(ancho):
            indice = pixeles[x, y]
            row.append(indice)  
        nonograma.append(row)

    return paleta, nonograma