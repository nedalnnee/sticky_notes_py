import os
from PIL import Image, ImageDraw

def create_sticky_note_icon(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    images = []

    for width, height in sizes:
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Padding
        pad = max(1, width // 16)
        w_box = width - 2 * pad
        h_box = height - 2 * pad

        # Main note yellow background
        shape = [(pad, pad), (width - pad, height - pad)]
        corner_radius = max(2, width // 12)

        # Shadow
        draw.rounded_rectangle(
            [(pad + 1, pad + 2), (width - pad + 1, height - pad + 2)],
            radius=corner_radius,
            fill=(0, 0, 0, 50)
        )

        # Yellow Note Body
        draw.rounded_rectangle(
            [(pad, pad), (width - pad, height - pad)],
            radius=corner_radius,
            fill="#FFF099",
            outline="#E6C200",
            width=max(1, width // 32)
        )

        # Lines on Note
        line_color = "#D9B800"
        line_margin = width // 4
        y1 = pad + height // 3
        y2 = pad + height // 2
        y3 = pad + (height * 2) // 3
        line_w = max(1, width // 32)

        draw.line([(line_margin, y1), (width - line_margin, y1)], fill=line_color, width=line_w)
        draw.line([(line_margin, y2), (width - line_margin, y2)], fill=line_color, width=line_w)
        draw.line([(line_margin, y3), (width - line_margin - width // 6, y3)], fill=line_color, width=line_w)

        # Pin circle at top-right
        pin_r = max(2, width // 10)
        pin_x = width - pad - pin_r - max(1, width // 16)
        pin_y = pad + pin_r + max(1, width // 16)
        draw.ellipse([(pin_x - pin_r, pin_y - pin_r), (pin_x + pin_r, pin_y + pin_r)], fill="#EF4444", outline="#B91C1C")

        images.append(img)

    # Save PNG & ICO
    png_path = os.path.join(output_dir, "app_icon.png")
    ico_path = os.path.join(output_dir, "app_icon.ico")

    images[-1].save(png_path, format="PNG")
    images[-1].save(ico_path, format="ICO", sizes=sizes)
    print(f"Generated icons at {png_path} and {ico_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    create_sticky_note_icon(current_dir)
