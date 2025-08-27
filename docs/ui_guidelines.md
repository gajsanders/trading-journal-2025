# User Interface Guidelines

## Overview

The Trading Journal Streamlit application includes several UI components designed to prevent common user mistakes and provide clear error guidance.

## Common User Mistakes Prevention

### 1. Unsupported File Formats

The file upload component restricts file selection to CSV files only using the `type=["csv"]` parameter. This prevents users from uploading unsupported file formats.

### 2. Invalid Strategy Names

The strategy input component validates strategy names to ensure they only contain:
- Letters (a-z, A-Z)
- Numbers (0-9)
- Spaces
- Hyphens (-)
- Underscores (_)

Invalid characters trigger clear error messages explaining the allowed characters.

### 3. Incomplete Forms

The form validation component checks that all required fields are properly filled:
- Strategy names (if provided) must be valid
- Time periods must have valid start and end dates
- Start dates must be before end dates

### 4. Misselected Time Periods

The time period selector component includes validation that ensures:
- Start date is before end date
- Clear warning messages are displayed for invalid date ranges

## Error Handling and User Guidance

### Error Messages

The application provides clear, actionable error messages for each type of user mistake:

1. **Invalid Strategy Names**: "Strategy name contains invalid characters. Only letters, numbers, spaces, hyphens, and underscores are allowed."

2. **Invalid Date Ranges**: "Start date must be before end date."

3. **Multiple Errors**: All validation errors are displayed simultaneously so users can fix all issues at once.

### UI Components

1. **File Upload Component**: Restricts file selection to CSV files only.

2. **Strategy Input Component**: Includes help text explaining valid characters and real-time validation.

3. **Time Period Selector Component**: Shows warnings for invalid date ranges.

4. **Form Validation Component**: Centralized validation logic that checks all form data and returns a list of errors.

## Best Practices

1. **Clear Error Messages**: All error messages are specific and actionable.

2. **Real-time Validation**: Validation happens as users interact with the UI.

3. **Multiple Error Display**: All errors are shown at once rather than one at a time.

4. **Help Text**: Components include help text to guide users.

5. **Visual Feedback**: Different message types (error, warning, info, success) use appropriate Streamlit components.