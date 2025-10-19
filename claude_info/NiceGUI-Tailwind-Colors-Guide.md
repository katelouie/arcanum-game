# NiceGUI & Tailwind CSS Colors Guide

A practical guide to understanding and using colors in NiceGUI with Tailwind CSS.

---

## Color Naming System

Tailwind uses a **color-shade** naming pattern:

```
{color}-{shade}
```

**Examples:**
- `purple-900` - Very dark purple
- `amber-400` - Medium-light amber/gold
- `slate-200` - Very light gray

---

## Shade Numbers (50-950)

The number indicates **lightness/darkness** from 50 (lightest) to 950 (darkest):

| Shade | Description | Use Cases |
|-------|-------------|-----------|
| **50** | Palest tint | Subtle backgrounds, highlights |
| **100-200** | Very light | Hover states, soft accents |
| **300-400** | Light-medium | Borders, icons, secondary text |
| **500** | Base color | Primary buttons, key accents |
| **600-700** | Medium-dark | Darker buttons, active states |
| **800-900** | Very dark | Dark backgrounds, strong text |
| **950** | Darkest | Near-black, deep backgrounds |

**Rule of thumb:**
- **Lower numbers** = lighter (more white mixed in)
- **Higher numbers** = darker (more black mixed in)

---

## Opacity Modifiers

Add `/##` after any color to control transparency:

```
bg-purple-900/95   →   Purple-900 at 95% opacity (5% transparent)
bg-purple-900/50   →   Purple-900 at 50% opacity (semi-transparent)
bg-purple-900/10   →   Purple-900 at 10% opacity (very transparent)
```

**Common opacity values:**
- `/100` - Fully opaque (default)
- `/95` - Barely transparent (subtle depth)
- `/80` - Noticeably transparent (layers show through)
- `/50` - Half transparent (good for overlays)
- `/20` - Very transparent (subtle tints)
- `/10` - Almost invisible (ghost effects)

**Tip:** Use opacity to create atmospheric depth without changing the base color!

---

## Color Prefixes

Different prefixes apply colors to different properties:

| Prefix | Property | Example |
|--------|----------|---------|
| `bg-` | Background | `bg-purple-900` |
| `text-` | Text color | `text-amber-400` |
| `border-` | Border color | `border-purple-400/30` |
| `from-` / `to-` | Gradients | `from-purple via-purple-950 to-black` |
| `ring-` | Focus rings | `ring-amber-300` |
| `divide-` | Divider lines | `divide-purple-400/20` |

---

## Arcanum Color Palette

Here are the colors currently used in your game:

### Primary Colors

**Purple (mystical, magical)**
```
purple-950/90  →  Drawer background (almost black, subtle purple)
purple-900     →  Dark backgrounds, cards
purple-800     →  Hover states, active elements
purple-700     →  Buttons, interactive elements
purple-600     →  Primary buttons, key actions
purple-400/30  →  Borders (transparent)
purple-300     →  Meta text, subtle accents
purple-200     →  Secondary text
purple-100     →  Light text on dark backgrounds
```

**Amber/Gold (tarot, mystical)**
```
amber-600/30   →  Button backgrounds (subtle)
amber-500/50   →  Subdued borders
amber-400      →  Bright borders, key accents
amber-300      →  Headers, important text
amber-200      →  Position labels
```

**Black (depth, mystery)**
```
bg-black              →  Solid black backgrounds
bg-gradient-to-b      →  Gradients (from-purple via-purple-950 to-black)
from-purple via-purple-950 to-black  →  Main screen gradient
```

### Special Colors

**Blue (special clients)**
```
blue-900/20    →  Special client card backgrounds
blue-800/30    →  Hover states for special cards
blue-400/30    →  Special client borders
blue-300       →  Special section headers
blue-200       →  Special client titles
```

**Slate/Gray (neutral tones)**
```
slate-900      →  Alternative dark backgrounds (more neutral than purple)
gray-900       →  Very dark neutral backgrounds
```

---

## Practical Examples

### Creating Depth with Layers

**Layered backgrounds (light to dark):**
```python
# Outermost layer (darkest)
.classes('bg-black')

# Middle layer (dark purple, slightly transparent)
.classes('bg-purple-950/95')

# Inner layer (medium purple, more transparent)
.classes('bg-purple-900/80')

# Content area (lighter purple, very transparent)
.classes('bg-purple-800/50')
```

### Borders with Atmosphere

**From bright to subtle:**
```python
# Bright, attention-grabbing
.classes('border-2 border-amber-400')

# Medium, noticeable
.classes('border-2 border-amber-500/50')

# Subtle, atmospheric
.classes('border border-purple-400/20')
```

### Text Hierarchy

**From most to least prominent:**
```python
# Title/Header
.classes('text-amber-300')          # Bright gold, eye-catching

# Primary text
.classes('text-purple-100')         # Light purple, readable

# Secondary text
.classes('text-purple-200')         # Slightly darker, less prominent

# Tertiary text / hints
.classes('text-purple-300')         # Even more subtle
```

### Hover Effects

**Making things glow/lighten on hover:**
```python
# Before hover: dark button
.classes('bg-purple-900/30')

# On hover: lighter, more opaque
.classes('hover:bg-purple-800/50')

# Or change color entirely:
.classes('bg-purple-900 hover:bg-purple-700')
```

---

## Color Experimentation Tips

### 1. Adjusting Darkness
If something is too bright/dark, change the shade number:
```python
# Too bright:
bg-purple-500  →  bg-purple-700  (darker)

# Too dark:
bg-purple-900  →  bg-purple-700  (lighter)
```

### 2. Adjusting Intensity
If a color is too saturated/bold, add or adjust opacity:
```python
# Too intense:
bg-purple-900  →  bg-purple-900/80  (same color, more transparent)

# Too subtle:
bg-purple-900/50  →  bg-purple-900/90  (same color, less transparent)
```

### 3. Matching Adjacent Elements
Elements next to each other should have **similar shades** for cohesion:
```python
# Good (cohesive):
bg-purple-950   border-purple-900   text-purple-200

# Jarring (too much contrast):
bg-purple-200   border-purple-950   text-purple-900
```

### 4. Creating Atmosphere
For mystical/dark themes, use **high shade numbers** (800-950) with **low opacity** (50-90):
```python
# Atmospheric drawer:
bg-purple-950/90  border-amber-500/50

# Atmospheric card:
bg-purple-900/30  border-purple-400/20

# Atmospheric overlay:
bg-black/70
```

---

## Quick Reference: Common Tailwind Colors

| Color | Vibe | Good For |
|-------|------|----------|
| `slate` | Neutral, professional | Backgrounds, text |
| `gray` | Neutral, softer | Borders, dividers |
| `purple` | Mystical, royal | Arcanum primary |
| `violet` | Magical, ethereal | Alternative mystical |
| `indigo` | Deep, spiritual | Alternative primary |
| `blue` | Special, trustworthy | Special clients |
| `amber` | Warm, golden | Tarot accents |
| `yellow` | Bright, attention | Warnings, highlights |
| `orange` | Energetic, warm | Accents, CTAs |
| `red` | Urgent, passionate | Errors, warnings |
| `rose` | Romantic, soft | Love readings (future?) |
| `emerald` | Growth, nature | Success states |
| `teal` | Calm, mystical | Alternative accents |

---

## Testing Colors Live

Want to see how a color looks? Try these approaches:

### 1. Direct Testing in Player
Change a color in `nicegui_player.py` and reload the page:
```python
# Original:
.classes('bg-purple-900/95')

# Test different shades:
.classes('bg-purple-800/95')  # Lighter
.classes('bg-purple-950/95')  # Darker

# Test different opacity:
.classes('bg-purple-900/80')  # More transparent
.classes('bg-purple-900/100') # Fully opaque
```

### 2. Browser DevTools
- Right-click element → Inspect
- Edit the `class` attribute directly
- See changes instantly!

### 3. Tailwind Color Palette Tool
Visit: https://tailwindcss.com/docs/customizing-colors
- See all colors with hex codes
- Visual reference for all shades

---

## Example: Redesigning the Drawer

Let's say you want the drawer to feel **more mysterious and less purple**:

```python
# Current (subtle purple):
.classes('bg-purple-950/90 border-l-4 border-amber-500/50')

# Option 1: Near-black with purple hints
.classes('bg-slate-950/95 border-l-4 border-purple-400/30')

# Option 2: Pure black with gold accent
.classes('bg-black/90 border-l-4 border-amber-400/40')

# Option 3: Very dark indigo (different mystical)
.classes('bg-indigo-950/90 border-l-4 border-amber-500/50')
```

Try each and see which vibe you like best!

---

## Remember

- **Shade numbers**: 50 (light) → 950 (dark)
- **Opacity**: `/##` (100 = solid, 10 = almost invisible)
- **Prefixes**: `bg-`, `text-`, `border-`, etc.
- **Atmosphere = high shades + low opacity** (e.g., `purple-950/80`)
- **When in doubt, test it!** Colors look different in context.

Happy color noodling! 🎨💜

---

**Quick Cheat Sheet to Keep Handy:**

```
bg-{color}-{50-950}/{0-100}
text-{color}-{50-950}/{0-100}
border-{color}-{50-950}/{0-100}

Lower shade = lighter (50 → 200)
Mid shade = vibrant (400 → 600)
Higher shade = darker (800 → 950)

Lower opacity = more transparent (/10 → /50)
Higher opacity = more solid (/80 → /100)
```
