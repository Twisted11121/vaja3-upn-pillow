# Naloge za obdelavo slik s knjižnico Pillow

# Opomba: Za vsako funkcijo, ki spreminja sliko, naj se rezultat shrani
# pod imenom "originalnoIme_opisSpremembe.png" v isti mapi kot originalna slika.

from  PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import random as rand
import face_recognition

def grayscale(image_path):

    imageOpen = Image.open(image_path)
    image_finish = ImageOps.grayscale(imageOpen)
    image_finish.show()
    image_finish.save("slike/grayscale-edit.jpg", "JPEG")

    pass

def text_to_image(image_path, text, position, font_size=24, font_color=(255, 255, 255)):

    x, y = position

    imageOpen = Image.open(image_path)
    image_draw = ImageDraw.Draw(imageOpen)

    font = ImageFont.truetype(font="Ariel.ttf", size=font_size)

    image_draw.text((x,y), text, font=font, fill=font_color)
    imageOpen.show()
    imageOpen.save("slike/addedTextImage.jpg", "JPEG")


    pass

def logo_to_image(image_path, logo_path, position, scale=0.1, folder = None):

    image1 = Image.open(image_path)
    width, height = image1.size
    image2 = Image.open(logo_path)
    width2, height2 = image2.size

    if scale:
        image2 = image2.resize((round(width2 * scale), round(height2 * scale)), Image.Resampling.LANCZOS)
        width2, height2 = image2.size


    position1 = {
            "left": (0,0),
            "right": (width - width2, 0),
            "center": ((width // 2) - (width2 // 2), (height // 2)-(height2//2)),
            "leftUp": (0, 0),
            "rightUp": (width - width2, 0),
            "centerUp": ((width // 2) - (width2 // 2), 0),  
            "leftDown": (0, height-height2), 
            "rightDown": (width-width2, height-height2),
            "centerDown": ((width // 2) - (width2 // 2), height-height2 )
        }
    
    finished_image = image1.copy()
    finished_image.paste(image2, position1[position])
    finished_image.show()

    finished_image.save(f"slike/image-w-logo.jpg", "JPEG")

    if folder:
        i = 0
        for name in os.listdir(folder):
            i += 1
            imageOpen = Image.open(f"{folder}/{name}")
            finished_image2 = imageOpen.copy()
            finished_image2.paste(image2, position1[position])
            finished_image2.save(f"slike/logo-{name}", "JPEG")




def my_filter(image_path, intensity=0.5):
    """
    Funkcija ustvari učinek filtra na sliki.
    """
    
    image1 = Image.open(image_path)
    filter_image = image1.filter(ImageFilter.EMBOSS)
    enhancer = ImageEnhance.Contrast(filter_image)
    embossed_image = enhancer.enhance(intensity)

    embossed_image.show()
    embossed_image.save(f"slike/filter-image.jpg" ,"JPEG")


    pass

def merge_images(folder_path, rows=2, cols=2, userScale=False):
    """
    Funkcija združi vse slike iz podane mape v eno samo sliko.
    """
    
    #We are assuming every image is the SAME resolution/size.
    
    width, height = 0, 0

    for image1 in os.listdir(folder_path):
        image1 = Image.open(f"{folder_path}/{image1}")
        width, height = image1.size
        break

    #print(width, height)
    

    num_of_images = 0
    width_start = 0
    height_start = 0
    
    num_of_images = len(os.listdir(folder_path))
    if num_of_images % 2 != 0:
        num_of_images +=1
    
    
    img_width = width // cols
    img_height = height // rows




    real_width = img_width * cols
    real_height = img_height * rows

    merged_images = Image.new("RGB", (real_width, real_height))    

    

    if userScale == True:
        img_width = int(img_width * 1.5)


    
    for i, image in enumerate(sorted(os.listdir(folder_path))):



        img = Image.open(f"{folder_path}/{image}")
        img = img.resize((img_width,img_height), Image.Resampling.LANCZOS)
        merged_images.paste(img, (width_start, height_start))
        width_start += img_width

        if (i + 1) % cols == 0:
            width_start = 0
            height_start += img_height





    
    merged_images.show()
    #merged_images.save("slike/merged_images.jpg", "JPEG")



def random_quote(image_path, quote_file, font_size=24, font_color=(255, 255, 255)):
    """
    Funkcija doda naključni citat na sliko.
    
    Parametri:
    slike/image_path (str): Pot do izvirne slike
    quote_file (str): Pot do datoteke s citati
    font_size (int): Velikost pisave
    font_color (tuple): RGB barva pisave
    
    Izhod:
    Shranjena slika z dodanim citatom
    """

    imageOpen = Image.open(image_path)
    image_draw = ImageDraw.Draw(imageOpen)

    img_width, img_height = imageOpen.size

    font = ImageFont.truetype(font="C:/Windows/Fonts/Arial.ttf", size=font_size)
    list1 = []
    with open(f"{quote_file}", "r") as qFile:
        for line in qFile:
            list1.append(line.strip())

    quote = list1[rand.randint(1,100)]
    image_draw.text((int(img_width/4)-len(quote), img_height/2), str(quote), font=font, fill=font_color)
    imageOpen.show()
    imageOpen.save("slike/quoteImage.jpg", "JPEG")



def blur_faces(image_path, blur_factor=15):
    """
    Funkcija zamegli obraze na sliki.
    Opomba: Ta funkcija bo potrebovala zunanjo knjižnico za zaznavanje obrazov.
    
    Parametri:
    slike/image_path (str): Pot do izvirne slike
    blur_factor (int): Stopnja zameglitve (višja vrednost = več zameglitve)
    
    Izhod:
    Shranjena slika z zamagljenimi obrazi
    """
    person = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(person)
    
    personOpen = Image.open(image_path)

    box = face_locations[0]
    top, right, bottom, left = box

    crop_face = personOpen.crop((left, top, right, bottom))
    crop_face = crop_face.filter(ImageFilter.BoxBlur(radius=blur_factor))
    
    personOpen.paste(crop_face, (left, top, right, bottom))
    personOpen.show()

def collage(folder_path, output_size=(1000, 1000), shape='grid'):
    """
    Funkcija ustvari kolaž iz podanih slik.
    
    Parametri:
    folder_path (string): Seznam poti do mape s slikami
    output_size (tuple): Velikost končnega kolaža (širina, višina)
    shape (str): Oblika kolaža ('grid', 'random', 'circle',...izberi sam opcije)
    
    Izhod:
    Shranjena slika kolaža
    """
    # KODA
    pass

# Dodatne pomožne funkcije po potrebi (potrebno za vse točke)

# Testni klici funkcij (zakomentirani)
if __name__ == "__main__":
    #grayscale("slika.jpg")
    #text_to_image("slika.jpg", "Primer besedila", (10, 10))
    #logo_to_image("slika.jpg", "images.jpg", "centerDown", 0.5, "slike")  #left, right, center, leftUp, rightUp, centerUp, leftDown, rightDown, centerDown)
    #my_filter("slika.jpg", intensity=1)
    #merge_images("slike")
    #random_quote("slika.jpg", "quotes.txt")
    #blur_faces("person.jpg")
    # collage("pot/do/mape")