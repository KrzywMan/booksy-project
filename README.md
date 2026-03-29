🎯 Hardware Hub - Booksy Assignment
A corporate hardware management system integrated with AI (Gemini 3.1).

PREVIEW LINK:
https://booksy-project-1.onrender.com

🛠️ Setup Instructions
Create a virtual environment: python -m venv venv.

Activate the environment and install libraries: pip install django google-generativeai.

Run migrations: python manage.py migrate.

(Optional) Run the seeding script: python manage.py seed_data.

Start the server: python manage.py runserver.

Tests: python manage.py test booksy.

📊 Implementation Status & Trade-offs
✅ Fully Implemented
Smart Dashboard: Real-time equipment list with filtering and statistics.

Rental Engine: Rental/return logic with blocking of damaged or reserved equipment.

AI Semantic Search: Integration with the gemini-3.1-flash-lite-preview model for business-specific search.

Admin Center: View for inventory management and creating employee accounts.

⚡ Shortcuts & “Hacks”
Vue.js via CDN: I used Vue.js directly from the CDN without a build step (Vite/Webpack) to ensure immediate project portability without complicated Node.js configuration on the recruiter’s end.

SQLite: I chose SQLite due to the “portability” requirement specified in the task.

🔍 Data Audit (Initial Dataset)
While integrating the input data, I identified and corrected the following errors in the provided JSON:

Duplicate ID: Samsung and Lenovo devices had the same ID (4).

Data Integrity: The Logitech MX Master 3 had a purchase date in the future (2027).

Typo: The brand “Appel” was corrected to “Apple”.

Consistency: The “Unknown Device” was automatically marked with the “Repair” status for safety.

🤖 AI Development Log
Tooling
Model: Gemini 3.1 Flash (via Google Generative AI SDK).

IDE: VS Code with terminal integration for gRPC debugging.

The “Correction” (Key Moment)
While implementing the AI search engine, I encountered a 404 error: models/gemini-1.5-flash is not found.

Problem: The SDK documentation suggested a model that was not available in my API version.

Solution: I manually called the list_models() function to check the available names in 2026. After identifying the gemini-3.1-flash-lite-preview model, I corrected the code in views.py, which restored system stability.

I used Gemini to help me with this task. Below is the link to the prompting history:
https://gemini.google.com/share/f062fcc4d27a

AI had a problem with files localizations, so I had to check them manually, and change to the valid ones.

Next Steps (24-Hour Roadmap)
Implement JWT for more secure API communication.

Add a rental history for each user.

Enhance the AI with an Inventory Auditor that automatically flags equipment requiring inspection based on technical notes.


