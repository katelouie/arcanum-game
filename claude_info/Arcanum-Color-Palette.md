# Arcanum Color Palette

Quick reference for all colors currently used in the Arcanum game.

---

## Main Screen Backgrounds

```python
# Landing page gradient
'bg-gradient-to-b from-purple via-purple-950 to-black'

# Player screen gradient
'bg-gradient-to-b from-purple via-purple-950 to-black'

# Dashboard gradient
'bg-gradient-to-b from-purple via-purple-950 to-black'
```

**Vibe:** Deep mystical gradient from rich purple to absolute black

---

## Card Backgrounds

### Story Cards (main content)
```python
'bg-white/10 backdrop-blur-sm border border-purple-400/30'
```
**Effect:** Frosted glass with subtle purple border

### Client Cards (normal)
```python
'bg-purple-900/20 border-2 border-purple-400/30'
```
**Effect:** Dark purple with transparent background

### Client Cards (special - Nyx)
```python
'bg-blue-900/20 border-2 border-blue-400/30'
```
**Effect:** Dark blue to distinguish special clients

### Dashboard Stats Cards
```python
'bg-white/10 backdrop-blur-sm border border-purple-400/30'
```
**Effect:** Consistent frosted glass

### Tarot Card Container (in spread)
```python
'bg-purple-900/30 border-2 border-amber-400/50'
```
**Effect:** Semi-transparent purple with gold accent

---

## Drawer (Card Details)

```python
# Drawer background
'bg-purple-950/90'

# Drawer border
'border-l-4 border-amber-500/50'
```

**Vibe:** Almost black with subtle purple undertones, gentle gold border

---

## Text Colors

### Headers / Titles
```python
'text-amber-400'    # ARCANUM title (bright gold)
'text-amber-300'    # Section headers (softer gold)
'text-amber-200'    # Position labels on cards
```

### Body Text
```python
'text-purple-100'   # Main body text (light, readable)
'text-purple-200'   # Secondary text, descriptions
'text-purple-300'   # Meta options, subtle text
```

### Special Elements
```python
'text-blue-300'     # "Special Consultations" header
'text-blue-200'     # Special client names
```

---

## Buttons

### Primary Action Buttons
```python
'bg-purple-600 text-white hover:bg-purple-700'
```
**Use for:** "Begin Reading", choice buttons

### Secondary Buttons
```python
'bg-purple-900/50 text-purple-200 border border-purple-400/30 hover:bg-purple-800/50'
```
**Use for:** "Continue Journey", "Return to Table"

### Drawer Close Button
```python
'bg-amber-600/20 text-amber-300 hover:bg-amber-600/30'
```
**Use for:** Close actions in drawer

### Meta/Subtle Buttons
```python
'bg-purple-900/30 text-purple-300 border border-purple-400/20 hover:bg-purple-800/30'
```
**Use for:** "Review progress", "Study cards"

---

## Hover States

### Cards
```python
# Client cards
'hover:bg-purple-800/30 hover:shadow-2xl hover:-translate-y-1'

# Special client cards
'hover:bg-blue-800/30 hover:shadow-2xl hover:-translate-y-1'

# Tarot cards in spread
'hover:border-amber-300 hover:scale-105'
```

### Buttons
```python
# Primary
'hover:bg-purple-700 hover:scale-105'

# Secondary
'hover:bg-purple-800/50'

# Meta
'hover:bg-purple-800/30'
```

---

## Borders & Dividers

```python
# Bright accent borders
'border-amber-400'           # Tarot card containers
'border-2 border-amber-400/50'  # Semi-transparent variant

# Subtle dividers
'border-purple-400/30'       # Most cards and containers
'border-purple-400/20'       # Very subtle dividers

# Drawer dividers
'border-amber-400/20'        # Horizontal separators in drawer
'border-amber-500/50'        # Drawer left border
```

---

## Gradients

### Progress Bar
```python
'bg-gradient-to-r from-purple-500 to-amber-400'
```
**Effect:** Purple to gold gradient fill

### Screen Backgrounds
```python
'bg-gradient-to-b from-purple via-purple-950 to-black'
```
**Effect:** Vertical fade from purple to black

---

## Shadow & Glow Effects

```python
# Card shadows
'shadow-lg'         # Standard cards
'shadow-xl'         # Client cards
'shadow-2xl'        # Hovered cards, drawer images

# Combined with hover
'hover:shadow-2xl'  # Glow on hover
```

---

## Mix-and-Match Examples

### Creating a New Card Type

**Option A: Neutral mystical card**
```python
.classes(
    'bg-slate-900/30 border-2 border-slate-400/30 '
    'hover:bg-slate-800/40 transition-all'
)
```

**Option B: Warm mystical card**
```python
.classes(
    'bg-amber-900/20 border-2 border-amber-400/40 '
    'hover:bg-amber-800/30 transition-all'
)
```

**Option C: Deep purple card**
```python
.classes(
    'bg-purple-950/40 border-2 border-purple-300/30 '
    'hover:bg-purple-900/50 transition-all'
)
```

---

### Creating a New Button Style

**Option A: Gold accent button**
```python
.classes(
    'bg-amber-700/30 text-amber-200 rounded-lg '
    'hover:bg-amber-600/40 transition-all'
)
```

**Option B: Subtle ghost button**
```python
.classes(
    'bg-transparent text-purple-300 border border-purple-400/20 '
    'hover:bg-purple-900/20 transition-all'
)
```

**Option C: Bold action button**
```python
.classes(
    'bg-purple-600 text-white font-semibold rounded-lg shadow-lg '
    'hover:bg-purple-500 hover:scale-105 transition-all'
)
```

---

### Creating Different Drawer Vibes

**Option A: Current (subtle purple)**
```python
'bg-purple-950/90 border-l-4 border-amber-500/50'
```

**Option B: Near-black neutral**
```python
'bg-slate-950/95 border-l-4 border-purple-400/30'
```

**Option C: Pure black with gold**
```python
'bg-black/90 border-l-4 border-amber-400/40'
```

**Option D: Indigo mystical**
```python
'bg-indigo-950/90 border-l-4 border-amber-500/50'
```

**Option E: Very dark blue**
```python
'bg-blue-950/90 border-l-4 border-amber-600/40'
```

---

## Color Combinations That Work

### Purple + Gold (current main theme)
```python
bg-purple-900       + text-amber-300        # Dark bg, gold text ✓
border-purple-400   + border-amber-400      # Purple + gold borders ✓
bg-purple-950/90    + border-amber-500/50   # Drawer style ✓
```

### Purple + Blue (for special elements)
```python
bg-purple-900/20    + bg-blue-900/20        # Normal vs special cards ✓
text-purple-200     + text-blue-200         # Text contrast ✓
border-purple-400   + border-blue-400       # Border contrast ✓
```

### Purple + Slate (for neutral elements)
```python
bg-purple-950       + bg-slate-900          # Dark variations ✓
text-purple-200     + text-slate-200        # Readable text ✓
```

---

## Avoid These Combinations

❌ **Too much contrast:**
```python
bg-purple-50 + text-purple-950    # Too stark
bg-amber-400 + text-amber-900     # Hard to read
```

❌ **Too similar (invisible):**
```python
bg-purple-900 + text-purple-900   # Same shade = invisible
bg-purple-900 + border-purple-900 # Border won't show
```

❌ **Clashing vibes:**
```python
bg-purple-900 + border-red-400    # Red doesn't fit mystical theme
bg-amber-400 + text-green-500     # Clashing warm/cool
```

---

## Quick Copy-Paste Snippets

### Card with hover
```python
.classes(
    'bg-purple-900/30 border-2 border-purple-400/30 '
    'hover:bg-purple-800/40 hover:shadow-xl '
    'transition-all duration-300 cursor-pointer'
)
```

### Button with hover
```python
.classes(
    'px-6 py-3 bg-purple-600 text-white rounded-lg '
    'hover:bg-purple-700 hover:scale-105 '
    'transition-all duration-200'
)
```

### Text hierarchy
```python
# Header
.classes('text-2xl font-serif text-amber-300 font-bold')

# Body
.classes('text-base text-purple-100 leading-relaxed')

# Subtitle/hint
.classes('text-sm text-purple-300 italic')
```

### Divider line
```python
ui.separator().classes('bg-amber-400/20 my-4')
```

---

## Pro Tips for Color Selection

1. **Stay within shade ranges:**
   - Backgrounds: 800-950 (very dark)
   - Borders: 300-500 (medium)
   - Text: 100-300 (light)

2. **Use opacity for depth:**
   - Solid backgrounds: `/90-100`
   - Layered elements: `/50-80`
   - Subtle accents: `/20-40`

3. **Keep hover states 1-2 shades lighter:**
   ```python
   bg-purple-900  →  hover:bg-purple-800  ✓
   bg-purple-900  →  hover:bg-purple-500  ✗ (too big a jump)
   ```

4. **Border opacity < background opacity:**
   ```python
   bg-purple-900/90  border-purple-400/30  ✓  (border more transparent)
   bg-purple-900/30  border-purple-400/90  ✗  (border too solid)
   ```

---

Now you can noodle with colors to your heart's content! 🎨💜

Try swapping shades and opacities to see what vibes you like best.
