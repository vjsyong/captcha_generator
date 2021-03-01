from PIL import ImageFont, ImageDraw, Image  
import numpy as np
import random, string, cv2, os
from pathlib import Path

class Captcha:

    font = []
    draw_offset = (10, -10)

    def __init__(self, width, height, text, mode):
        self.width = width
        self.height = height
        self.text = self.random_key(5)
        self.img = None
        self.font.append(ImageFont.truetype("PrimaSansMonoBT-Roman.otf", 45))
        self.font.append(ImageFont.truetype("Prima_Sans_Mono_Bold_BT.ttf", 45))
        self.font.append(ImageFont.truetype("PrimaSansMonoBT-BoldOblique.otf", 45))
        self.font.append(ImageFont.truetype("PrimaSansBT-Oblique.otf", 45))
        self.mode = "train"
        
        

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
        standard_chars = "bdfhklt0123456789ABCDEFGHIKLMNOPRSTUVWXYZ"
        tall_chars = "JQ"
        if char in tailed_chars:
            return (w, ascent - offset_y + descent)
        elif char in compact_chars:
            return (w, ascent - offset_y)
        elif char in standard_chars:
            return (w, ascent - offset_y)
        else:
            return (w, ascent - offset_y)

    def draw_string(self, text, text_file):
        lastwidth = 0 # Position to draw next char
        char_list = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        for i,char in enumerate(text):
            rand = random.randint(0, 3)
            random_font = self.font[rand]
            # w, h = random_font.getsize(char)
            w, h = self.get_char_size(random_font, char)
            offset = random_font.getoffset(char)
            tail_offset = 0
            squeeze_offset = 0
            # print(char, " offset", offset, "-- w, h =", w, h)
            tailed_chars = "gjpqy"
            if char in tailed_chars:
                tail_offset = int(offset[1]/2)
            if rand < 2: # squeeze boxes if not an oblique font
                squeeze_offset = 2 
            lt = (lastwidth+10+offset[0]+squeeze_offset, self.height-h-13+tail_offset) # lt - left top
            br = (lastwidth+ w+10+offset[0]-squeeze_offset, self.height-11+tail_offset) # br - bottom right
            x_center_scaled = (lt[0] + int(w/2)) / self.width
            y_center_scaled = (lt[1] + int(h/2) + 1) / self.height
            width_scaled = w / self.width
            height_scaled = (h+2) / self.height
            line = str(char_list.index(char)) + " " + str(x_center_scaled) + " " + str(y_center_scaled) + " " + str(width_scaled) + " " + str(height_scaled) + "\n"
            text_file.write(line)

            # print(lastwidth)
            self.draw_char(self.img, (10 + lastwidth, -10), random_font, char)
            # cv2.rectangle(self.img, lt , br, (0,0,0), 1)
            # cv2.circle(self.img, (x_center, y_center), 2, (0, 0, 255), -1)
            # self.draw_char(self.img, (lastwidth + w, -10), random_font, char)
            lastwidth += (w-4)
        text_file.close()

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

        
        filename = os.path.abspath(os.path.dirname(__file__)) + "/captchas" 
        Path(filename).mkdir(parents=True, exist_ok=True)
        Path(filename + "/images/train").mkdir(parents=True, exist_ok=True)
        Path(filename + "/labels/train").mkdir(parents=True, exist_ok=True)
        Path(filename + "/images/valid").mkdir(parents=True, exist_ok=True)
        Path(filename + "/labels/valid").mkdir(parents=True, exist_ok=True)
        
        filename_jpg = filename + "/images/" + self.mode + "/" + self.text + ".jpg"
        filename_txt = filename + "/labels/" + self.mode + "/" + self.text + ".txt"
        text_file = open(filename_txt,"w+")
        self.draw_frame()
        self.draw_string(self.text, text_file)
        self.draw_line(self.img)
        scaled = cv2.resize(self.img, (224, 64) , interpolation = cv2.INTER_AREA)
        # cv2.imshow("white", scaled)
        cv2.imwrite(filename_jpg, scaled) 
        # cv2.waitKey()

if __name__ == '__main__': 
    for i in range(10):
        c = Captcha(175, 50, "", "train")
        c.generate()
    
    for i in range(10):
        c = Captcha(175, 50, "", "valid")
        c.mode = "valid"
        c.generate()
