from PIL import Image

def simplificar_colores(ruta_imagen, num_colores, nueva_resolucion):
    im = Image.open(ruta_imagen)

    im_resized = im.resize(nueva_resolucion, Image.LANCZOS)

    out = im_resized.convert('P', palette=Image.ADAPTIVE, colors=num_colores)

    return out



def leer_pixeles(imagen, f):
    
    pixeles = imagen.load()

    ancho, alto = imagen.size
    print(ancho, alto)
    paleta = imagen.getpalette()

    f.write(f'{alto};{ancho}\n')

    num_colores = len(paleta) // 3

    for i in range(num_colores):
        r = paleta[i * 3]
        g = paleta[i * 3 + 1]
        b = paleta[i * 3 + 2]
        f.write(f"{i};{r};{g};{b}\n")


    for y in range(alto):
        for x in range(ancho):
            indice = pixeles[x, y]
            r = paleta[indice * 3]
            g = paleta[indice * 3 + 1]    
            b = paleta[indice * 3 + 2]   
            f.write(f"{x};{y};{indice}\n")




if __name__ == "__main__":
    ruta_imagen = 'girasol.jpeg' 
    num_colores = 8  # Número de colores
    nueva_resolucion = (25, 15)  # Nueva resolución deseada (ancho, alto)
    point = ruta_imagen.index('.')
    ruta = ruta_imagen[:point]
    resolution = str(nueva_resolucion[0]) + 'x' + str(nueva_resolucion[1])
    txt = ruta + '_' + resolution
    imagen_simplificada = simplificar_colores(ruta_imagen, num_colores, nueva_resolucion)

    f = open(f'{txt}.txt', "w")
    leer_pixeles(imagen_simplificada, f)
    f.close()
    imagen_simplificada.show()