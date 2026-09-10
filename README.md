# BIS — BIS Standards AI Assistant

BIS (Bureau of Indian Standards) Assistant is a small desktop application that helps businesses identify potential Indian Standards and BIS certification guidance for products. It uses a PyQt6 GUI and an LLM (configured via the Google GenAI client) to analyze product information and provide structured recommendations, testing and certification guidance.

This repository contains:

- bis_assistant_ui.py — PyQt6 user interface and application entry point
- core.py — core logic that builds the LLM prompt, calls the GenAI API, and saves responses to notes.json
- notes.json — (created at runtime) stores past analysis responses for debugging and audit

Features

- Simple form-based UI to enter business & product details
- Uses Google GenAI (Gemini) to generate structured JSON guidance
- Saves each LLM response to notes.json for review
- Clear separation between UI (bis_assistant_ui.py) and analysis logic (core.py)

--------------------------------------------------------------------------------

Table of Contents

- Installation
- Configuration
- Usage
- How it works
- Development
- Troubleshooting
- Contributing
- License
- Contact

--------------------------------------------------------------------------------

Installation

1. Ensure Python 3.10+ is installed on your system.
2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate     # Windows (PowerShell)
```

3. Install the required Python packages. There is no requirements.txt in the repo, but the project depends on the following packages:

```bash
pip install PyQt6 python-dotenv google-genai
```

Note: The package name for the GenAI client may vary depending on distribution; the code imports `from google import genai`. If pip cannot find `google-genai`, consult the official Google GenAI SDK documentation for the correct package name for your environment.

--------------------------------------------------------------------------------

Configuration

Create a .env file in the project root with your Gemini/GenAI API key. Example `.env`:

```text
GEMINI_API_KEY=sk-xxxx-your-api-key-xxxx
```

Security: Do NOT commit your API key to version control. Keep `.env` in .gitignore.

--------------------------------------------------------------------------------

Usage

Run the application from the repository root:

```bash
python bis_assistant_ui.py
```

The UI fields are:

- Business / Industry — e.g. "Electrical manufacturing"
- Product — e.g. "Electric water heater"
- Product Description — short multi-line description
- Intended Use — e.g. "Residential use"
- Target Market — defaults to "India"
- Existing Certification — optional (e.g. "ISO 9001")

Click "Analyze Product" to send the inputs to the GenAI model. The app expects the model to return a JSON object matching a well-defined schema; results are displayed in cards in the right-hand pane.

Notes:
- The app saves each LLM response (raw or structured) into notes.json in the project root for auditing and debugging.
- The core prompt explicitly instructs the model not to invent standard numbers, schemes, or legal requirements — still verify recommendations with official BIS sources.

--------------------------------------------------------------------------------

How it works (internals)

- bis_assistant_ui.py provides the PyQt6 GUI and a Worker thread that calls analyze_product(...) in core.py so the UI stays responsive.
- core.py builds a multi-line prompt containing the product details and calls genai.Client(...).models.generate_content(...) with model="gemini-3.6-flash".
- The code expects the model to return JSON. If the model returns non-JSON, the raw response is saved and a ValueError is raised.
- Responses are appended to notes.json via save_response(...).

Important implementation details found in core.py:

- Environment variable: GEMINI_API_KEY — required to authenticate to the GenAI client.
- The LLM prompt contains strict rules and an exact JSON structure the model must return. Modify core.py if you want to change the output schema or model behavior.

--------------------------------------------------------------------------------

Development

- To change the LLM model or model parameters, edit core.py (search for `client.models.generate_content`).
- To change the JSON schema or prompt wording, edit the prompt string in analyze_product(...) in core.py.
- To add logging or persist responses in a different location (database, file per-analysis), modify save_response and save_data in core.py.
- UI changes: bis_assistant_ui.py is a single-file PyQt6 UI — edit the layout, styles or fields directly there. The UI uses ResultCard and a Worker QThread for background work.

Testing

- There are no automated tests included. Manual testing steps:
  - Start the app and submit a simple product description.
  - Verify notes.json is created and contains a saved JSON response.
  - Test behavior when GEMINI_API_KEY is missing — the GenAI client will likely raise an authentication/connection error.

--------------------------------------------------------------------------------

Troubleshooting

- ModuleNotFoundError: If imports fail, ensure the virtual environment is active and dependencies are installed (see Installation).
- Authentication / API errors: Verify GEMINI_API_KEY is set in .env and that network access is available.
- Invalid JSON from Gemini: The application saves the raw response into notes.json and raises an error. Check notes.json to inspect the model output.
- If PyQt6 windows fail to render or crash, try updating PyQt6 or run the app from a terminal to see traceback output.

--------------------------------------------------------------------------------

Security & Privacy

- The app sends product and business details to an external LLM service — treat sensitive product information accordingly.
- Do not store API keys in the repository. Add `.env` to .gitignore.

--------------------------------------------------------------------------------

Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository.
2. Create a topic branch for your change.
3. Open a pull request with a clear description and any manual test steps.

If adding new dependencies, update this README with installation instructions and consider adding a requirements.txt.

--------------------------------------------------------------------------------

License

This project has no license file in the repository. If you want to apply an open-source license, add a LICENSE file (e.g., MIT) and update this section.

--------------------------------------------------------------------------------

Contact

Project maintainer: replace with your name and contact email.

--------------------------------------------------------------------------------

If you want the README to include example screenshots, CI badges, or a requirements.txt file generated from the current environment, tell me and the preferred license and I will update the repository accordingly.