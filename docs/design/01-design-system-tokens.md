# Design System Tokens

## 1. Brand Identity
- **Product Name:** LexiForge AI
- **Tagline:** Write Better. Think Smarter.
- **Personality:** Intelligent, Trustworthy, Premium, Academic, Professional.

## 2. Color System
The color system maps semantically to Tailwind classes used across the application.

| Name | Hex Value | CSS Variable | Tailwind Usage |
|------|-----------|--------------|----------------|
| **Primary Light** | `#A855F7` | `--primary-light` | `bg-primary-light`, `text-primary-light` |
| **Primary Main** | `#9333EA` | `--primary-main` | `bg-primary`, `text-primary` |
| **Primary Dark** | `#6B21A8` | `--primary-dark` | `bg-primary-dark`, `text-primary-dark` |
| **Background** | `#FFFFFF` | `--background` | `bg-background` |
| **Surface** | `#F8FAFC` | `--surface` | `bg-surface` |
| **Border** | `#E5E7EB` | `--border` | `border-border` |
| **Text Primary** | `#111827` | `--text-primary` | `text-text-primary` |
| **Text Secondary**| `#6B7280` | `--text-secondary`| `text-text-secondary` |
| **Success** | `#22C55E` | `--success` | `bg-success`, `text-success` |
| **Warning** | `#F59E0B` | `--warning` | `bg-warning`, `text-warning` |
| **Error** | `#EF4444` | `--error` | `bg-error`, `text-error` |

## 3. Typography
- **Primary Font:** Inter
- **Fallback Font:** System Sans

### Typography Scale
| Level | Font Size | CSS Variable |
|-------|-----------|--------------|
| **H1** | 48px | `--text-h1` |
| **H2** | 40px | `--text-h2` |
| **H3** | 32px | `--text-h3` |
| **H4** | 24px | `--text-h4` |
| **Body Large** | 18px | `--text-body-lg` |
| **Body Base** | 16px | `--text-body` |
| **Caption** | 14px | `--text-caption` |

## 4. Layout System
- **Desktop Container:** Max-width 1440px
- **Tablet Breakpoint:** 768px (Tailwind `md:`)
- **Mobile Breakpoint:** 375px Base

## 5. Spacing System
Based on a 4px Grid System. Maps to standard Tailwind spacing.

- `4px` (Tailwind `1`)
- `8px` (Tailwind `2`)
- `12px` (Tailwind `3`)
- `16px` (Tailwind `4`)
- `24px` (Tailwind `6`)
- `32px` (Tailwind `8`)
- `48px` (Tailwind `12`)
- `64px` (Tailwind `16`)
- `96px` (Tailwind `24`)
