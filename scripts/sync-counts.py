"""Copies the library counts from public/data/catalog.json to every place outside the app that shows them.
Runs at the end of build-catalog.py, so adding packs needs no manual edits."""
import json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'public/data/catalog.json').read_text('utf8'))
packs, images, animated = catalog['packCount'], f"{catalog['imageCount']:,}", f"{catalog['animatedCount']:,}"
WORDS = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split()
total = len({p['platform'] for p in catalog['packs']})
platforms = WORDS[total] if total < len(WORDS) else str(total)
N = r'[\d,]+'

TEXTS = {
    'index.html': [
        (rf'Explore {N} community avatar packs and {N} images', f'Explore {packs} community avatar packs and {images} images'),
        (rf'content="{N} packs\. {N} avatars\.', f'content="{packs} packs. {images} avatars.'),
    ],
    'README.md': [
        (rf'alt="Avatarium: {N} packs, {N} avatars"', f'alt="Avatarium: {packs} packs, {images} avatars"'),
        (rf'\*\*{N} packs, {N} avatars\*\*, {N} of them animated, from \w+ platforms', f'**{packs} packs, {images} avatars**, {animated} of them animated, from {platforms} platforms'),
    ],
    'audit/pcloud-download-audit.json': [
        (r'("manifests": \{\s*"bytes": \d+,\s*"entries": )\d+', rf'\g<1>{packs}'),
    ],
}

for name, rules in TEXTS.items():
    path = ROOT / name
    with path.open(encoding='utf8', newline='') as f: before = f.read()
    text = before
    for pattern, new in rules:
        text, hits = re.subn(pattern, new, text)
        # A reworded sentence must stop the build instead of silently going stale.
        if not hits: raise SystemExit(f'{name}: count not found for {pattern!r}')
    if text != before:
        with path.open('w', encoding='utf8', newline='') as f: f.write(text)
        print('Counts updated in', name)

# The preview picture needs Pillow, which may live in another Python installed on this computer.
def pythons():
    yield sys.executable
    try: listed = subprocess.run(['py', '-0p'], capture_output=True, text=True).stdout
    except OSError: return
    for line in listed.splitlines():
        if line.strip().lower().endswith('python.exe'): yield line[line.rfind(':') - 1:].strip()

for python in pythons():
    if subprocess.run([python, '-c', 'import PIL'], capture_output=True).returncode == 0:
        subprocess.run([python, '-X', 'utf8', str(ROOT / 'scripts/build-og-image.py')], check=True)
        break
else:
    raise SystemExit('Pillow is missing, so the preview picture was not redrawn: run "python -m pip install pillow".')
