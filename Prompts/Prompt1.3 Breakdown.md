Original
**Prompt 1.3 – Error Handling Tests**
> *“Write unit/integration tests focusing on error handling for all failure modes in the project. Cover network errors, file read/write issues, invalid data formats, missing configs, and user mistakes. Include expected error messages.”*

New
Atomic Prompts - Refined for Your Spec
1. CSV File Read/Write Error Handling
Prompt A:
"Write pytest unit tests that cover file reading errors for importing TastyTrade CSVs: missing file, permission denied, malformed CSV content. Include the expected error messages shown to the user for each case."
Prompt B:
"Create tests that check error handling for exporting data as CSV and Markdown: permission denied, insufficient disk space, and file locking issues. Use pytest and include the expected output or messages."
2. Data Validation and Parsing
Prompt C:
"Generate pytest tests for validating trade entry rows in imported CSVs: missing required fields, invalid symbols, inconsistent timestamps, and duplicate order numbers. For each scenario, show the error or flag raised."
Prompt D:
"Write pytest tests for invalid option description parsing: malformed description strings, unknown strategy types, and unsupported characters. Confirm that the fallback classification is triggered and the user receives a clear message."
3. Missing Configurations
Prompt E:
"Write pytest tests covering missing or invalid environment variable configuration (e.g., WORKSPACE_ROOT unset or incorrect). Ensure that the application flags configuration errors and guides the user to fix them."
---
I need to create comprehensive pytest tests for environment variable validation, specifically targeting the WORKSPACE_ROOT variable. Since I can't read src/config.py due to tool repetition limits, I'll use a different approach.

Looking at the project structure, I can see:
- .env and .env.example files exist, suggesting environment variables are used
- The application likely loads environment variables at startup
- There are existing test files in the tests/ directory

I'll create a new test file that will:
1. Mock environment variables to test various error scenarios
2. Verify that the application raises appropriate errors for missing, malformed, or incorrect values
3. Ensure error messages are clear and actionable with guidance on how to fix issues

I'll create a new test file in the tests/ directory to cover these scenarios.
---

Prompt F:
"Create tests for missing or invalid configuration file content (if used), such as missing keys or malformed values. Use pytest assertions for user-facing error guidance."
4. User Mistakes in Streamlit UI
Prompt G:
"Devise pytest tests for common user mistakes in the Trading Journal Streamlit interface: uploading files in unsupported formats, entering invalid strategy names, submitting incomplete forms, and misselecting time periods. Check that the UI displays appropriate error or guidance messages for each case."
5. General Error Handling Framework
Prompt H:
"Generate pytest fixtures/mocks for simulating error conditions throughout the pipeline: invalid input files, parsing failures, analysis exceptions, and chart export failures. For each, write one test showing the failure is handled gracefully with a proper message."


6. (If/When Network Calls Added)
Prompt I:
"If any future features trigger HTTP requests (e.g., for LLM analysis or broker APIs), create pytest tests using requests-mock to simulate timeouts, unreachable endpoints, and invalid responses. Include expected application behavior and error messages."
Usage
Use these prompts individually in Zed Assistant with Qwen for quick turnarounds on test code.
Each focuses on a single error mode, closely matched to your spec.
All prompts specify pytest to match your tech stack and best Python practice.
When advanced config or network features arrive, use Prompts F and I above.
