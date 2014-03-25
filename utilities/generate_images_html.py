__author__ = 'Zhenyu'

import os
from utilities import markup

if __name__ == "__main__":
    os.chdir(os.getcwd() + "/..")
    data_path = "views/"

    images = [im for im in os.listdir(data_path) if im.endswith("m.png")]

    page = markup.page()
    page.init(title="test")

    page.table(border=2)
    c = 0
    page.tr()
    for im in images:
        c += 1
        page.td()
        page.a(im[:-5], href=im)
        page.br()
        page.img(src=im, width=300)
        page.td.close()
        if c % 5 ==0:
            page.tr.close()
            page.tr()


    f = open(data_path + 'images.html', 'w')
    f.write(str(page))
    f.close()
    print images
