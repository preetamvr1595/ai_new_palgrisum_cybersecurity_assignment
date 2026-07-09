# User Flows

## 1. Onboarding & Authentication Flow
1. **User lands on Homepage:** Clicks "Start Free".
2. **Signup Page:** Enters Email, Password, and Name.
3. **Email Verification:** System sends OTP/Magic Link. User verifies email.
4. **Onboarding Questionnaire (Optional):** Asks "What describes you best?" (Student, Professional, Writer).
5. **Dashboard Overview:** User lands on the main dashboard with a "Welcome" tooltip pointing to the AI tools.

## 2. Core Tool Flow (AI Detection / Humanizer)
1. **Tool Selection:** User clicks "AI Detector" from the sidebar.
2. **Input Stage:** User pastes text into the text area or clicks "Upload File".
3. **Processing:** User clicks "Analyze". A loading skeleton/spinner appears.
4. **Results View:** Shows AI vs Human percentage. Sentences are highlighted based on AI probability.
5. **Next Action:** User clicks "Humanize Text". System routes to Humanizer page with text pre-filled.
6. **Export:** User clicks "Export PDF Report" and downloads the file.

## 3. Subscription Upgrade Flow
1. **Trigger:** User hits the free tier word limit or tries to access a Pro feature (e.g., Plagiarism Scanner).
2. **Paywall Modal:** Appears over the current screen highlighting Pro benefits.
3. **Pricing Page:** User clicks "View Plans" and goes to Pricing.
4. **Checkout:** User selects "Pro Plan (Monthly)" and enters Stripe checkout.
5. **Success:** Confetti animation, account updated to Pro, user returns to their previous tool seamlessly.
