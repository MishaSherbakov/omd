class Color:
    def __init__(self, red, green, blue):
        self._red = self._proverka(red)
        self._green = self._proverka(green)
        self._blue = self._proverka(blue)

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        self._red = self._proverka(value)

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        self._green = self._proverka(value)

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value):
        self._blue = self._proverka(value)

    def _proverka(self, value):
        if not (0 <= value <= 255):
            raise ValueError("Color component must be between 0 and 255.")
        return int(value)
    
    def __repr__(self):
        END = '\033[0'
        START = '\033[1;38;2'
        MOD = 'm'
        return f'{START};{self._red};{self._green};{self._blue}{MOD}●{END}{MOD}'
    
    def __eq__(self, other):
        return self.red == other.red and self.green == other.green and self.blue == other.blue
    
    def __add__(self, other):
        if not isinstance(other, Color):
            raise ValueError()
        else:
            return Color(self.red + other.red, self.green + other.green, self.blue + other.blue)
            
    def __hash__(self):
        return hash((self.red, self.green, self.blue))
    
    def __mul__(self, other):
        c = other
        if c < 0 or c > 1:
            raise ValueError()
        cl = -256*(1 - c)
        F = 259*(cl + 255) / (255*(259 - cl))
        new_red = F*(self.red - 128) + 128
        new_green = F*(self.green - 128) + 128
        new_blue = F*(self.blue - 128) + 128
        return(Color(new_red, new_green, new_blue))
        
        
    def __rmul__(self, other):
        c = other
        if c < 0 or c > 1:
            raise ValueError()
        cl = -256*(1 - c)
        F = 259*(cl + 255) / (255*(259 - cl))
        new_red = F*(self.red - 128) + 128
        new_green = F*(self.green - 128) + 128
        new_blue = F*(self.blue - 128) + 128
        return(Color(new_red, new_green, new_blue))
    
#1 задание
END = '\033[0'
START = '\033[1;38;2'
MOD = 'm'
red_level = 100
green_level = 149
blue_level = 237
print("1-ое:", f'{START};{red_level};{green_level};{blue_level}{MOD}●{END}{MOD}')

#2 задание
red = Color(255, 0, 0)
green = Color(0, 255, 0)
print("2-ое:", red == green)
print("2-ое:", red == Color(255, 0, 0))

#3 задание
red = Color(255, 0, 0)
green = Color(0, 255, 0)
print("3-ое:", red + green)

#4 задание
orange1 = Color(255, 165, 0)
red = Color(255, 0, 0)
green = Color(0, 255, 0)
orange2 = Color(255, 165, 0)
color_list = [orange1, red, green, orange2]
print("4-ое:", set(color_list))

#5 задание
red = Color(255, 0, 0)
print("5-ое:", 0.5 * red)