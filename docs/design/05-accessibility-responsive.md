# Accessibility & Responsive Rules

## 1. Accessibility (WCAG 2.1 AA)

### Contrast Ratios
- Normal Text (`--text-secondary`): Must meet a 4.5:1 contrast ratio against the background.
- Large Text (Headings): Must meet a 3.0:1 contrast ratio.
- UI Components (Buttons/Inputs): Boundaries must meet a 3.0:1 contrast ratio against the background.

### Keyboard Navigation
- All interactive elements (buttons, links, inputs, dropdowns) must be reachable via `Tab`.
- Provide a "Skip to Content" link at the top of the page for screen reader users.

### Focus States
- Use `focus:ring-2 focus:ring-primary focus:ring-offset-2` on all interactive elements.
- Do NOT use `outline: none` without providing an alternative focus indicator.

### Screen Reader Support
- Ensure proper use of `aria-labels` on icon-only buttons.
- Use semantic HTML (`<nav>`, `<main>`, `<section>`, `<article>`).
- Use `aria-live="polite"` for dynamic result updates (e.g., when AI Analysis finishes).

## 2. Responsive Rules

### Breakpoints
- **Mobile (`< 768px`)**: Stack layouts vertically. Sidebar converts into a Hamburger menu (bottom sheet or sliding drawer). Padding reduces to 16px.
- **Tablet (`768px - 1024px`)**: Side-by-side elements can collapse or scale down. Sidebar can become a collapsed icon-only sidebar.
- **Desktop (`> 1024px`)**: Full sidebar visible. Max width container centers content on ultra-wide screens.

### Touch Targets
- Mobile buttons and links must have a minimum touch target area of `44x44px`.
- Increase spacing between interactive elements on mobile devices to prevent accidental taps.
