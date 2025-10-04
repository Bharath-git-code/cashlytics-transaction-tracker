from PIL import Image, ImageDraw, ImageFont
import os


# Create a simple logo for the app
def create_logo():
    # Create a 512x512 image with a blue background
    size = (512, 512)
    img = Image.new("RGBA", size, (32, 150, 255, 255))  # Blue background
    draw = ImageDraw.Draw(img)

    # Draw a white circle
    circle_margin = 80
    draw.ellipse(
        [
            circle_margin,
            circle_margin,
            size[0] - circle_margin,
            size[1] - circle_margin,
        ],
        fill=(255, 255, 255, 255),
        outline=(255, 255, 255, 255),
    )

    # Add text
    try:
        # Try to use a nice font
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        # Fallback to default font
        font = ImageFont.load_default()

    # Draw the "C" for Cashlytics
    text = "C"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2 - 20

    draw.text((text_x, text_y), text, fill=(32, 150, 255, 255), font=font)

    # Add subtitle
    try:
        small_font = ImageFont.truetype("arial.ttf", 30)
    except:
        small_font = ImageFont.load_default()

    subtitle = "₹"
    bbox = draw.textbbox((0, 0), subtitle, font=small_font)
    sub_width = bbox[2] - bbox[0]

    sub_x = (size[0] - sub_width) // 2
    sub_y = text_y + text_height + 10

    draw.text((sub_x, sub_y), subtitle, fill=(32, 150, 255, 255), font=small_font)

    # Save the logo
    logo_path = "assets/icons/logo.png"
    os.makedirs(os.path.dirname(logo_path), exist_ok=True)
    img.save(logo_path)
    print(f"Logo created and saved to {logo_path}")


if __name__ == "__main__":
    create_logo()
