import pymupdf, sys
from PIL import Image
pdf, out, dpi, per = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
d = pymupdf.open(pdf)
imgs=[]
for p in d:
    pm=p.get_pixmap(dpi=dpi); imgs.append(Image.frombytes("RGB",[pm.width,pm.height],pm.samples))
for g in range(0,len(imgs),per):
    grp=imgs[g:g+per]; w,h=grp[0].size; cols=2; rows=(len(grp)+1)//2
    sheet=Image.new("RGB",(w*cols+10,h*rows+10*(rows-1)),"#888")
    for i,im in enumerate(grp): sheet.paste(im,((i%2)*(w+10),(i//2)*(h+10)))
    sheet.save(f"{out}_{g//per+1}.png")
