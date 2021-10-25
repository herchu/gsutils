import png
import os

outdir = "out"
skin = "vestimenta"
# Cuantos niveles de cada canal
# Por ejemplo 2 definiria 3*3*3 = 27 colores en total
escala = 3


os.makedirs(outdir, exist_ok=True)
colores = (escala + 1) ** 3
lines = [
    " # Vestimenta RGB {} colores".format(colores),
    "name: RGB",
    "rules:"
]
WW = 200
BB = 0
for r in range(escala + 1):
    for g in range(escala + 1):
        for b in range(escala + 1):
            r2 = max(int(256 * r / escala) - 1, 0)
            g2 = max(int(256 * g / escala) - 1, 0)
            b2 = max(int(256 * b / escala) - 1, 0)
            print(r, g, b, "->", r2, g2, b2)
            p = [(r2, g2, b2, r2, g2, b2),
                 (r2, g2, b2, r2, g2, b2)]
            imagen = 'pix{}{}{}.png'.format(r, g, b)
            f = open(os.path.join(outdir, imagen), 'wb')
            w = png.Writer(2, 2, greyscale=False)
            w.write(f, p)
            f.close()

            # Pixel especial para seleccion
            imagen_sel = 'sel{}{}{}.png'.format(r, g, b)
            f = open(os.path.join(outdir, imagen_sel), 'wb')
            p = [(WW, WW, WW, BB, BB, BB, WW, WW, WW, BB, BB, BB, WW, WW, WW),
                 (BB, BB, BB, r2, g2, b2, r2, g2, b2, r2, g2, b2, BB, BB, BB),
                 (WW, WW, WW, r2, g2, b2, r2, g2, b2, r2, g2, b2, WW, WW, WW),
                 (BB, BB, BB, r2, g2, b2, r2, g2, b2, r2, g2, b2, BB, BB, BB),
                 (WW, WW, WW, BB, BB, BB, WW, WW, WW, BB, BB, BB, WW, WW, WW)]
            w = png.Writer(5, 5, greyscale=False)
            w.write(f, p)
            f.close()

            lines += [
                "  - image: " + imagen,
                "    when:",
                "      black: 0",
                "      red: {}".format(r),
                "      green: {}".format(g),
                "      blue: {}".format(b),
                # Lo mismo con una bolita negra
                "  - image: " + imagen,
                "    when:",
                "      black: 1",
                "      red: {}".format(r),
                "      green: {}".format(g),
                "      blue: {}".format(b),
                # Dos bolitas negras: Seleccion
                "  - image: " + imagen_sel,
                "    when:",
                "      black: 2",
                "      red: {}".format(r),
                "      green: {}".format(g),
                "      blue: {}".format(b)
            ]

with open(os.path.join(outdir, "config.yml"), "w") as f:
    f.writelines('\n'.join(lines))
