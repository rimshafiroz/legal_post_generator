from PIL import Image, ImageDraw, ImageFont
import os

def write_text_on_image(image, text, output_path=None, *, is_holiday: bool = False, style_variant: int = 0):
    from PIL import ImageFilter
    import random
    draw = ImageDraw.Draw(image)
    width, height = image.size
    font_path = "Montserrat-Bold.ttf"
    font_size = max(48, width // 16)
    try:
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
        font_size = 32
    max_width = width - 120
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test_line = line + (" " if line else "") + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    bbox = draw.textbbox((0, 0), "A", font=font)
    line_height = (bbox[3] - bbox[1]) + 18  # More line spacing
    total_height = line_height * len(lines)
    # Decide placement and alignment based on variant
    placement_modes = ["bottom_center", "center_left", "center"]
    mode = placement_modes[style_variant % len(placement_modes)]
    if mode == "bottom_center":
        y_text = height - total_height - max(height // 12, 40)
    elif mode == "center_left":
        y_text = (height - total_height) / 2
    else:  # center
        y_text = (height - total_height) / 2
    gradient_height = int(height * 0.38)
    base_tint = (0, 0, 0)
    if is_holiday:
        # subtle warm tint for holiday vibe
        base_tint = (22, 18, 8)  # very dark warm tone
    gradient = Image.new("RGBA", (width, gradient_height), (0,0,0,0))
    for y in range(gradient_height):
        alpha = int(220 * (y / gradient_height))
        ImageDraw.Draw(gradient).rectangle([0, y, width, y+1], fill=(base_tint[0], base_tint[1], base_tint[2], alpha))
    overlay = Image.new("RGBA", image.size, (0,0,0,0))
    if mode == "bottom_center":
        overlay.paste(gradient, (0, height - gradient_height), gradient)
    else:
        from PIL import ImageOps
        g_rot = gradient.rotate(90, expand=True)
        if mode == "center_left":
            overlay.paste(g_rot, (0, (height - g_rot.size[1]) // 2), g_rot)
        else:  # center
            overlay.paste(gradient, (0, height - gradient_height), gradient)
    if is_holiday:
        import random
        bokeh_layer = Image.new("RGBA", image.size, (0,0,0,0))
        bokeh_draw = ImageDraw.Draw(bokeh_layer)
        num_dots = max(12, (width * height) // 180000)  # scale with size
        palette = [
            (212,175,55,90),   # soft gold
            (200,200,200,70),  # silver
            (230, 60, 60, 60), # deep red
            (70, 160, 120, 60) # emerald
        ]
        for _ in range(num_dots):
            r = random.randint(6, 16)
            x = random.randint(0, width)
            y = random.randint(int(height*0.55), height)  # mostly lower half
            color = random.choice(palette)
            bokeh_draw.ellipse((x-r, y-r, x+r, y+r), fill=color)
        overlay = Image.alpha_composite(overlay, bokeh_layer)

    combined = Image.alpha_composite(image, overlay)
    draw = ImageDraw.Draw(combined)
    # Always use white text
    text_color = (255,255,255)
    # Draw text lines
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        if mode == "center_left":
            x = max(40, width * 0.08)
        else:
            x = (width - w) / 2
        # Draw glow (multiple blurred shadows)
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,2),(-2,2),(2,-2)]:
            draw.text((x+dx, y_text+dy), line, font=font, fill=(0,0,0,90))
        # Draw main text
        draw.text((x, y_text), line, font=font, fill=text_color + (255,))
        y_text += line_height
    if output_path is None:
        output_path = "final_post.png"
    combined.convert("RGB").save(output_path)
    return output_path