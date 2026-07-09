# Component Specifications

This document defines the structural requirements for complex reusable UI components for LexiForge AI.

## 1. Modals
- **Backdrop:** rgba(17, 24, 39, 0.5) (Black with 50% opacity)
- **Container:** Border radius 12px (xl), bg-white, shadow-xl.
- **Header:** Sticky top, title using `text-h4` font size, close button (X icon) aligned to the right.
- **Body:** Scrollable on Y-axis. 24px padding.
- **Footer:** Sticky bottom, border-t, action buttons aligned to the right.

## 2. Tables
- **Header Row:** `bg-surface`, `text-sm`, uppercase tracking wider, `text-text-secondary`.
- **Rows:** `bg-white` transitioning to `bg-surface` on hover. Bottom border `border-border`.
- **Pagination:** Bottom right aligned. Next/Prev ghost buttons.

## 3. Tooltips
- **Container:** `bg-text-primary`, `text-white`, `text-xs`, 4px border radius.
- **Behavior:** Delay of 200ms before showing. Should dynamically flip position if clipping browser window bounds.

## 4. File Upload Components
- **Drag & Drop Zone:** Dashed border `border-primary-light`, `bg-surface`.
- **Active State:** Solid border `border-primary`, `bg-primary/5`.
- **Content:** Cloud upload icon, primary action link "Browse files", supporting text indicating max size (e.g., "Max 10MB, PDF/DOCX").
- **Progress State:** Show file name, progress bar (see below), and cancel button (X).

## 5. Progress Bars
- **Track:** `bg-surface` or `bg-gray-200`, rounded full.
- **Fill:** `bg-primary`, animated transition on width change.
- **Text:** Optional percentage label aligned to the right.

## 6. Alerts
- **Success:** `bg-success/10`, `border-success`, `text-success-dark`. Check icon.
- **Warning:** `bg-warning/10`, `border-warning`, `text-warning-dark`. Alert triangle icon.
- **Error:** `bg-error/10`, `border-error`, `text-error-dark`. X-circle icon.
- **Info:** `bg-primary/10`, `border-primary`, `text-primary-dark`. Info icon.

## 7. Skeleton Loaders
- **Animation:** Pulse (`animate-pulse`).
- **Color:** `bg-gray-200`.
- **Shapes:** Rounded rectangles matching the component they replace (e.g., circular for avatars, varying width bars for text lines).
