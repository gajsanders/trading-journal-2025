# Configuration Guide

## Required Environment Variables

### WORKSPACE_ROOT
The `WORKSPACE_ROOT` environment variable must be set to the absolute path of your project root directory. This is used by the application to locate data files and other resources.

Example:
```
WORKSPACE_ROOT=/Users/yourname/Documents/2025.07 Trading Journal
```

## Validation

The application validates the configuration at startup and will display an error message if:
1. `WORKSPACE_ROOT` is not set
2. `WORKSPACE_ROOT` is set to an empty string
3. The path specified in `WORKSPACE_ROOT` does not exist
4. The path specified in `WORKSPACE_ROOT` is not a directory

## Setup Instructions

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and set the `WORKSPACE_ROOT` variable to the absolute path of your project directory.

3. Optionally, set other environment variables like `OPENAI_API_KEY` if you plan to use LLM features.

4. Run the application:
   ```bash
   ./run.sh
   ```

## Error Messages

If the configuration is invalid, the application will display a clear error message indicating what needs to be fixed.