"""
Создание иконки пива для SkufUp
"""

import struct
import zlib

def create_beer_ico():
    """Создаёт ICO файл с пивной кружкой"""
    
    # 32x32 пиксельное изображение пивной кружки (RGBA)
    width, height = 32, 32
    
    # Цвета
    TRANSPARENT = (0, 0, 0, 0)
    GOLD = (234, 179, 8, 255)       # Пиво
    GOLD_DARK = (180, 140, 6, 255)  # Тень пива
    WHITE = (255, 255, 255, 255)    # Пена
    WHITE_LIGHT = (255, 255, 240, 255)  # Светлая пена
    GRAY = (80, 80, 80, 255)        # Ручка
    
    pixels = [[TRANSPARENT for _ in range(width)] for _ in range(height)]
    
    # Рисуем кружку (прямоугольник)
    for y in range(8, 28):
        for x in range(6, 22):
            if y < 12:
                # Пена сверху
                if 7 <= x <= 20:
                    pixels[y][x] = WHITE if (x + y) % 3 != 0 else WHITE_LIGHT
            else:
                # Пиво
                pixels[y][x] = GOLD if (x + y) % 5 != 0 else GOLD_DARK
    
    # Ручка справа
    for y in range(12, 24):
        for x in range(22, 26):
            if y == 12 or y == 23:
                if 22 <= x <= 25:
                    pixels[y][x] = GRAY
            elif 12 < y < 23:
                if x == 22 or x == 25:
                    pixels[y][x] = GRAY
    
    # Пузырьки в пиве
    bubbles = [(10, 16), (14, 20), (12, 24), (16, 18), (8, 22), (18, 23)]
    for bx, by in bubbles:
        if 0 <= by < height and 0 <= bx < width:
            pixels[by][bx] = WHITE_LIGHT
    
    # Конвертируем в BMP данные (BGRA, снизу вверх)
    bmp_data = bytearray()
    for y in range(height - 1, -1, -1):
        for x in range(width):
            r, g, b, a = pixels[y][x]
            bmp_data.extend([b, g, r, a])
    
    # AND маска (1 бит на пиксель, снизу вверх)
    and_mask = bytearray()
    for y in range(height - 1, -1, -1):
        row_bits = 0
        for x in range(width):
            if pixels[y][x][3] == 0:  # Прозрачный
                row_bits |= (1 << (31 - x))
        and_mask.extend(struct.pack('>I', row_bits))
    
    # ICO структура
    ico_data = bytearray()
    
    # ICONDIR header
    ico_data.extend(struct.pack('<HHH', 0, 1, 1))  # Reserved, Type=1 (ICO), Count=1
    
    # ICONDIRENTRY
    bmp_size = 40 + len(bmp_data) + len(and_mask)  # BITMAPINFOHEADER + pixels + mask
    ico_data.extend(struct.pack('<BBBBHHII',
        width if width < 256 else 0,   # Width
        height if height < 256 else 0,  # Height
        0,    # Color count
        0,    # Reserved
        1,    # Color planes
        32,   # Bits per pixel
        bmp_size,  # Size of image data
        22    # Offset to image data (6 + 16)
    ))
    
    # BITMAPINFOHEADER
    ico_data.extend(struct.pack('<IIIHHIIIIII',
        40,           # Header size
        width,        # Width
        height * 2,   # Height (XOR + AND)
        1,            # Planes
        32,           # Bits per pixel
        0,            # Compression
        0,            # Image size
        0,            # X pixels per meter
        0,            # Y pixels per meter
        0,            # Colors used
        0             # Important colors
    ))
    
    # Pixel data
    ico_data.extend(bmp_data)
    ico_data.extend(and_mask)
    
    return bytes(ico_data)


if __name__ == "__main__":
    ico_data = create_beer_ico()
    with open("beer.ico", "wb") as f:
        f.write(ico_data)
    print("✅ Создан файл beer.ico")
