# https://www.pentacom.jp/pentacom/bitfontmaker2/
# http://czyborra.com/



import argparse
import os


true = True;

OFFSET = 2

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help',
                    add_help=False)

parser.add_argument('fontfile')           # positional argument
parser.add_argument('-h', '--height', default=8)      # option that takes a value
parser.add_argument('-w', '--width', default=8)      # option that takes a value
parser.add_argument('-r', '--rotate', default="none", choices=["none", "left", "right", "half"])      # option that takes a value
parser.add_argument('-H', '--hflip', action="store_true", help="horizontal flip")      # on/off flag
parser.add_argument('-V', '--vflip', action="store_true", help="vartical flip")      # on/off flag
parser.add_argument('-t', '--topoffset', default=0)      # option that takes a value
parser.add_argument('-l', '--leftoffset', default=0)      # option that takes a value
parser.add_argument('-c', '--charmap', default="")      # option that takes a value

parser.add_argument('-v', '--verbose', action='store_true')  # on/off flag

args = parser.parse_args()
print(args.fontfile, args.verbose)

f = open(args.fontfile, "r")
chars = f.read()
f.close()

p = os.path.dirname(os.path.realpath(__file__))
print(p)

p = os.path.join(p, "maps", args.charmap + ".txt")
print(p)

chmap = {}
for c in range(256):
    chmap[c] = c

try:
    f = open(p, "r")

    for l in f.readlines():
        s = l.split()
        if (s[0][:1] == "=") and (s[1][:2] == "U+"):
            chmap[int(s[0][1:], 16)] = int(s[1][2:], 16)

except:
    pass
finally:
    pass



g = dict()
g["true"] = True
g["false"] = False

exec("font = " + chars, g)
print(g["font"])

fontdata = {}

(grmin, grmax, gcmin, gcmax) = (-1, -1, -1, -1)
(gwmax, ghmax) = (-1, -1)
tchars = 0



resh = int(args.height)
resw = int(args.width)

wmask = 0
for i in range(resw):
    wmask = (wmask << 1) | 1

for key in g["font"].keys():

    if key.isdigit():

        t = []
        for i in range(resh):
            try:
                d = g["font"][key][i + int(args.topoffset)]
            except:
                d = 0
            l = int(args.leftoffset)
            d = ((d >> l) if (l > 0) else (d << -l)) & wmask
            r = 0
            if bool(not args.hflip) != bool(args.rotate == "half"):
                for j in range(resw):
                    r <<= 1
                    r |= d & 1
                    d >>= 1
                d = r
            if bool(args.vflip) != bool(args.rotate == "half"):
                t.insert(0, d)
            else:
                t.append(d)

        if args.rotate in ["left", "right"]:
            q = []
            for i in range(resw):
                mask = (1 << i) if args.rotate == "left" else 1 << (resw - i)
                d = 0
                bit = 1 if args.rotate == "left" else (1 << (resh - 1))
                for j in range(resh):
                    d = (d << 1) if args.rotate == "left" else (d >> 1)
                    d |= bit if t[j] & mask else 0
                q.append(d)

            t = q

        g["font"][key] = t


        (rmin, rmax, cmin, cmax) = (-1, -1, -1, -1)
        for i in range(g["font"][key].__len__()):

            row = g["font"][key][i]
            if row != 0:

                rmin = i if (i < rmin) or (rmin == -1) else rmin
                rmax = i if (i > rmax) else rmax
                bit = 0

                while row != 0:

                    if (row & 1):
                        cmin = bit if (bit < cmin) or (cmin == -1) else cmin
                        cmax = bit if (bit > cmax) else cmax

                    bit += 1
                    row >>= 1

        numkey = int(key)
        fontdata[numkey] = {}

        fontdata[numkey]["data"] = t
        fontdata[numkey]["rmin"] = rmin
        fontdata[numkey]["rmax"] = rmax
        fontdata[numkey]["cmin"] = cmin
        fontdata[numkey]["cmax"] = cmax

        grmin = rmin if (rmin < grmin) or (grmin == -1) else grmin
        grmax = rmax if (i > grmax) else grmax

        gcmin = cmin if (cmin < gcmin) or (gcmin == -1) else gcmin
        gcmax = cmax if (cmax > gcmax) else gcmax

        ghmax = rmax - rmin + 1 if (ghmax < rmax - rmin + 1) else ghmax
        gwmax = cmax - cmin + 1 if (gwmax < cmax - cmin + 1) else gwmax

        tchars += 1

if args.rotate in ["left", "right"]:
    (resw, resh) = (resh, resw)


print("number of chars: {:d}".format(tchars))
print("font min row: {:d}".format(grmin))
print("font max row: {:d}".format(grmax))
print("font min col: {:d}".format(gcmin))
print("font max col: {:d}".format(gcmax))
print("max char height: {:d}".format(ghmax))
print("max char widht: {:d}".format(gwmax))

n = 0
m = 0
mm = 0

print("\n\n// generated character bitmaps\n".format(n))

e = "{"

for c in range(0, 256):
    n += 1

    if (chmap[c] in fontdata) and (chmap[c] != c):
        mc = chmap[c]
        s = "mapped unicode {:04X}".format(mc)
        data = fontdata[mc]["data"]
        mm += 1

    elif c in fontdata:
        s = "not mapped"
        data = fontdata[c]["data"]

    else:
        m += 1
        s = "generated blank"
        data = []
        for d in range(resh):
            data.append(0)

    print("\n// code {:d}, 0x{:02X} - {}".format(c, c, s))
    e += '"{}":['.format(c)

    for d in range(resh):
        print("0b{:0{w}b}, ".format(data[d], w=resw), end="")
        e += '{},'.format(data[d])

    e = e[:-1] + '],'

print("\n\n// total {:d} characters, {:d} substituted with blank\n\n".format(n, m))



e += '"name":"","copy":"","letterspace":"64","basefont_size":"251","basefont_left":"75","basefont_top":"-133","basefont":"Verdana","basefont2":""}'

print(e)
