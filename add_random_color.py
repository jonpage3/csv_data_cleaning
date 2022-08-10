import random

def hslToRgb(h,s,l):
    if s == 0:
        pass
    else:
        # var q = l < 0.5 ? l * (1 + s): l + s - l * s;
        if l < 0.5:
            q = l * (1 + s)
        else:
            q = l + s - (l*s)
        p = 2 * l - q;
        r = hue2rgb(p, q, h + 1 / 3)
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1 / 3);

    return '#' + num2chr(round(r*255)) + num2chr(round(g*255)) + num2chr(round(b*255))


def hue2rgb(p,q,t):

    if t < 0:
        t += 1
    if t > 1:
        t -= 1
    if t < 1/6:
        return p + (q - p) * 6 * t
    if t < 1/2:
        return q;
    if t < 2/3:
        return p + (q - p) * (2 / 3 - t) * 6
    return p


golden_ratio_conjugate = 0.618033988749895
h = float(f'{random.random():.17f}')
h += golden_ratio_conjugate
h %= 1


def num2chr(num):
    return hex(num)[2:]


if __name__ == "__main__":
    print(hslToRgb(h, 0.5, 0.60))