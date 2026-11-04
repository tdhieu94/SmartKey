#!/usr/bin/env python3
"""Signs the release files and writes the update feeds SmartKey reads (D61):
  appcast.xml   Sparkle feed: the Mac app (Sparkle) and the Windows app (its own updater) check it daily
  release.json  the Linux settings app compares linux.version with its own and offers the download
usage: feed.py <version> <build> <dir with the release files>   (env SPARKLE_ED_KEY: base64 ed25519 seed)
Files are served from the GitHub release v<version>; the apps fetch the feeds from releases/latest/download."""
import base64, glob, json, os, sys, time
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ver, build, d = sys.argv[1], sys.argv[2], sys.argv[3]
REPO = os.environ.get("GITHUB_REPOSITORY", "tdhieu94/SmartKey")
BASE = f"https://github.com/{REPO}/releases/download/v{ver}/"
key = Ed25519PrivateKey.from_private_bytes(base64.b64decode(os.environ["SPARKLE_ED_KEY"].strip()))

def enclosure(name, extra=""):
    data = open(os.path.join(d, name), "rb").read()
    sig = base64.b64encode(key.sign(data)).decode()
    return f'<enclosure url="{BASE}{name}" {extra}sparkle:edSignature="{sig}" length="{len(data)}" type="application/octet-stream"/>'

notes = os.environ.get("NOTES", "").strip() or f"SmartKey {ver}"
notes_html = "<ul>" + "".join(f"<li>{l.strip('-* ').strip()}</li>" for l in notes.splitlines() if l.strip()) + "</ul>"
date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
def item(title, enc, extra=""):
    return (f"<item>\n<title>{title}</title>\n<pubDate>{date}</pubDate>\n<sparkle:version>{build}</sparkle:version>\n"
            f"<sparkle:shortVersionString>{ver}</sparkle:shortVersionString>\n{extra}"
            f"<description><![CDATA[{notes_html}]]></description>\n{enc}\n</item>\n")
items = []
mac = f"SmartKey-{ver}-mac.zip"
if os.path.exists(os.path.join(d, mac)):
    items.append(item(f"SmartKey {ver}", enclosure(mac), "<sparkle:minimumSystemVersion>13.0</sparkle:minimumSystemVersion>\n"))
for arch in ("x64", "arm64"):
    win = f"SmartKey-{ver}-{arch}-Setup.exe"
    if os.path.exists(os.path.join(d, win)):
        items.append(item(f"SmartKey {ver} for Windows ({arch})", enclosure(win, f'sparkle:os="windows" vikey:arch="{arch}" ')))
open(os.path.join(d, "appcast.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0" xmlns:sparkle="http://www.andymatuschak.org/xml-namespaces/sparkle" '
    'xmlns:vikey="https://vikey.app/xmlns">\n<channel>\n<title>SmartKey</title>\n'
    f"<link>https://github.com/{REPO}</link>\n" + "".join(items) + "</channel>\n</rss>\n")
rel = {"version": ver, "download_url": f"https://github.com/{REPO}/releases/latest", "linux": {"version": ver}}
for f in sorted(glob.glob(os.path.join(d, "*"))):
    n = os.path.basename(f)
    if n.endswith((".deb", ".rpm")):
        rel["linux"][("deb" if n.endswith(".deb") else "rpm") + "_x64"] = {"download_url": BASE + n}
json.dump(rel, open(os.path.join(d, "release.json"), "w"), indent=1)
print(open(os.path.join(d, "appcast.xml")).read())
