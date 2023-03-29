from PIL import Image, ImageDraw
     
img = Image.new('RGB', (1000, 1000), color = (255, 255, 255))
     
d = ImageDraw.Draw(img)
d.ellipse((40, 40, 100, 100), fill = 'black', outline ='black')
img.save('pil_text.png')