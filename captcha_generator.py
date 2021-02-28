from PIL import ImageFont, ImageDraw, Image  
import numpy as np
import random, string, cv2, os

class Captcha:

    font = []
    draw_offset = (10, -10)

    def __init__(self, width, height, text):
        self.width = width
        self.height = height
        self.text = self.random_key(5)
        self.img = None
        self.font.append(ImageFont.truetype("PrimaSansMonoBT-Roman.otf", 45))
        self.font.append(ImageFont.truetype("PrimaSansMonoBT-BoldOblique.otf", 45))
        self.font.append(ImageFont.truetype("PrimaSansBT-Oblique.otf", 45))
        self.font.append(ImageFont.truetype("Prima_Sans_Mono_Bold_BT.ttf", 45))
        

    def draw_frame(self):
        self.img = np.zeros((self.height, self.width, 3), np.uint8)
        self.img.fill(255)

    def draw_char(self, img, coords, font, char):
        color_palette = [(255,110,91), (121,229,73), (73,176,230), (152,8,15), (122,229,74), (249,207,69)]
        pil_im = Image.fromarray(img)  
        draw = ImageDraw.Draw(pil_im)

        draw.text(coords, char, font=font, fill=(*random.choice(color_palette),255))
        self.img = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR) 
    
    def get_char_size(self, font, char):
        w, h = font.getsize(char)
        ascent, descent = font.getmetrics()
        (width, baseline), (offset_x, offset_y) = font.font.getsize(char)
        tailed_chars = "gjpqy"
        compact_chars = "aceimnorsuvwxz"
        tall_chars = "bdfhklt0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if char in tailed_chars:
            return (w, ascent - offset_y + descent)
        elif char in compact_chars:
            return (w, ascent - offset_y)
        else:
            return (w, ascent - offset_y)
    
    def draw_string(self, text):
        lastwidth = 0 # Position to draw next char
        for i,char in enumerate(text):
            random_font = random.choice(self.font)
            # w, h = random_font.getsize(char)
            w, h = self.get_char_size(random_font, char)
            offset = random_font.getoffset(char)
            tail_offset = 0
            print(char, " offset", offset, "-- w, h =", w, h)
            tailed_chars = "gjpqy"
            if char in tailed_chars:
                tail_offset = int(offset[1]/2)
            lt = (lastwidth+10+offset[0] , self.height-h-13+tail_offset)
            br = (lastwidth+ w+10+offset[0], self.height-11+tail_offset)
            print(lt, br)
            # cv2.rectangle(self.img, lt , br, (0,0,0), 1)
        
            # print(lastwidth)
            self.draw_char(self.img, (10 + lastwidth, -10), random_font, char)
            # self.draw_char(self.img, (lastwidth + w, -10), random_font, char)
            lastwidth += (w-4)

    def draw_line(self, img):
        # left_x = np.random.randint(0, self.width//4)
        left_x = 15
        left_y = np.random.randint(self.height)
        right_x = np.random.randint(self.width*3//4, self.width)
        right_y = np.random.randint(self.height*1//4, self.height*3//4)
        start, end = (left_x, left_y), (right_x, right_y)
        line_color = (0,0,0)
        line_thickness = 2
        cv2.line(img, start, end, line_color, line_thickness)
    
    def random_key(self, length):
        key = ''
        for i in range(length):
            key += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
        return key
    
    def generate(self):
        self.draw_frame()
        self.draw_string(self.text)
        self.draw_line(self.img)
        scaled = cv2.resize(self.img, (224, 64) , interpolation = cv2.INTER_AREA)
        filename = os.path.abspath(os.path.dirname(__file__)) + "\\captchas\\" + self.text + ".jpg"
        print(filename)
        cv2.imshow("white", scaled)
        cv2.imwrite(filename, scaled) 
        cv2.waitKey()

if __name__ == '__main__':
    # text = "66nb2"  
    while True:
        c = Captcha(175, 50, "66nb2")
        c.generate()