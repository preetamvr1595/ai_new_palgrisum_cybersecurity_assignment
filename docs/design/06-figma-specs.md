# Figma-Ready Specifications

This document translates the code-based design tokens into instructions for a UI designer setting up the Figma file.

## 1. Local Variables (Variables Panel)

### Color Collections
Create a collection named "LexiForge Colors":
- `Background/Default`: `#FFFFFF`
- `Surface/Default`: `#F8FAFC`
- `Border/Default`: `#E5E7EB`
- `Primary/Light`: `#A855F7`
- `Primary/Main`: `#9333EA`
- `Primary/Dark`: `#6B21A8`
- `Text/Primary`: `#111827`
- `Text/Secondary`: `#6B7280`

### Spacing Collections
Create a collection named "Spacing":
- `Spacing/1`: `4px`
- `Spacing/2`: `8px`
- `Spacing/3`: `12px`
- `Spacing/4`: `16px`
- `Spacing/6`: `24px`
- `Spacing/8`: `32px`

## 2. Text Styles (Text Panel)
Create these styles using the `Inter` font family:
- `Heading/H1`: Bold, 48px, 120% Line Height
- `Heading/H2`: Bold, 40px, 120% Line Height
- `Heading/H3`: Semibold, 32px, 130% Line Height
- `Heading/H4`: Semibold, 24px, 130% Line Height
- `Body/Large`: Regular, 18px, 150% Line Height
- `Body/Base`: Regular, 16px, 150% Line Height
- `Caption`: Regular, 14px, 140% Line Height

## 3. Component Architecture (Auto Layout)
All components MUST use Auto Layout to mimic CSS Flexbox.

### Button Component
- **Properties:** Variant (Primary, Secondary, Outline, Ghost, Danger), Size (Sm, Md, Lg), State (Default, Hover, Disabled, Loading).
- **Auto Layout:** Horizontal, Center-Center, 8px gap.

### Input Component
- **Properties:** State (Default, Focused, Error, Disabled), Icon (Left, None).
- **Auto Layout:** Vertical, Top-Left, 4px gap between label and field. Field has 16px horizontal padding, 12px vertical padding.

## 4. Exporting Assets
- Icons should be drawn in a 24x24px bounding box.
- Export icons as SVG with `currentColor` fill to allow developers to override colors using Tailwind.
