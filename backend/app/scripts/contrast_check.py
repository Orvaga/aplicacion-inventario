import re
import colorsys

CSS_PATH = r"d:\huilawed\aplicacion_app\backend\app\static\css\theme.css"

VAR_RE = re.compile(r'--([a-zA-Z0-9_-]+):\s*([^;]+);')
HEX_RE = re.compile(r'#([0-9a-fA-F]{6})')


def hex_to_rgb(h):
    h = h.strip().lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def sRGB_to_linear(c):
    c = c/255.0
    if c <= 0.03928:
        return c/12.92
    return ((c+0.055)/1.055) ** 2.4


def relative_luminance(rgb):
    r, g, b = [sRGB_to_linear(x) for x in rgb]
    return 0.2126*r + 0.7152*g + 0.0722*b


def contrast_ratio(fg, bg):
    L1 = relative_luminance(fg)
    L2 = relative_luminance(bg)
    lighter, darker = (L1, L2) if L1 > L2 else (L2, L1)
    return (lighter + 0.05) / (darker + 0.05)


if __name__ == '__main__':
    with open(CSS_PATH, 'r', encoding='utf-8') as f:
        css = f.read()

    vars = dict()
    for m in VAR_RE.finditer(css):
        name, value = m.groups()
        h = HEX_RE.search(value)
        if h:
            vars[name] = '#' + h.group(1)

    checks = [
        # (foreground, background, description)
        ('bg', 'surface', 'Body text on surface (body bg vs surface bg)'),
        ('surface', 'primary', 'White text on primary (buttons) - should be white text on primary bg'),
        ('surface', 'primary-dark', 'White text on primary-dark (button hover) - white text on darker background'),
        ('primary-dark', 'accent', 'Primary-dark text on accent bg (badge on accent) - dark text on yellow bg'),
        ('bg', 'accent', 'Default body text on accent bg (muted text on accent if any)'),
        ('bg', 'primary', 'Default body text on primary bg (rare)')
    ]

    print('Detected variables:')
    for k, v in vars.items():
        print(f'  --{k}: {v}')
    print('\nContrast checks (ratio): (WCAG AA for normal text >= 4.5)')

    for fgvar, bgvar, desc in checks:
        fghex = vars.get(fgvar) or '#ffffff'
        bghex = vars.get(bgvar) or '#ffffff'
        fg = hex_to_rgb(fghex)
        bg = hex_to_rgb(bghex)
        ratio = contrast_ratio(fg, bg)
        print(f'{desc}: fg={fghex} bg={bghex} => ratio={ratio:.2f} -> {"PASS" if ratio >= 4.5 else "FAIL"}')

    # Additionally check primary & accent with white text or dark text depending on usage
    white = (255, 255, 255)
    primary = hex_to_rgb(vars.get('primary', '#0b5ed7'))
    primary_dark = hex_to_rgb(vars.get('primary-dark', '#073b9a'))
    accent = hex_to_rgb(vars.get('accent', '#ffc107'))
    body_text = hex_to_rgb(vars.get('text', '#22303c') if 'text' in vars else '#22303c')

    print('\nAdditional relevant pairs:')
    pairs = [
        (white, primary, 'white on primary (button text)'),
        (white, primary_dark, 'white on primary-dark (hover) '),
        (body_text, accent, 'dark on accent (badges) '),
        (body_text, white, 'body text on white (default)')
    ]
    for fg, bg, desc in pairs:
        ratio = contrast_ratio(fg, bg)
        print(f'{desc}: fg={fg} bg={bg} => ratio={ratio:.2f} -> {"PASS" if ratio >= 4.5 else "FAIL"}')
