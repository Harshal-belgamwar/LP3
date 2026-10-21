
import random
import string
from PIL import Image, ImageDraw, ImageFont

def generate_captcha():
    #
    characters = string.ascii_uppercase + string.digits
    captcha_text = ''.join(
        random.choices(characters, k=6)
    )

   
    width, height = 240, 80
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    
    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line(
            (x1, y1, x2, y2),
            fill="gray",
            width=2
        )

    
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except OSError:
        font = ImageFont.load_default()

    draw.text(
        (35, 15),
        captcha_text,
        font=font,
        fill="blue"
    )

   
    image.save("captcha.png")
    image.show()

    return captcha_text


def verify_captcha():
    captcha = generate_captcha()

    print("CAPTCHA image generated: captcha.png")
    user_input = input("Enter the CAPTCHA shown in the image: ")

    if user_input.strip().upper() == captcha:
        print("CAPTCHA Verified Successfully!")
    else:
        print("Invalid CAPTCHA. Please try again.")


if __name__ == "__main__":
    verify_captcha()
