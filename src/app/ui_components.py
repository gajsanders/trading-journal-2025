import streamlit as st
from typing import Optional, List
from datetime import datetime, date
import re

def file_upload_component(label: str = "Upload CSV") -> Optional[str]:
    uploaded_file = st.file_uploader(label, type=["csv"])
    if uploaded_file is not None:
        return uploaded_file
    return None

def strategy_input_component(label: str = "Strategy Name") -> str:
    """Input component for strategy names with validation."""
    strategy_name = st.text_input(label, help="Enter a valid strategy name (letters, numbers, spaces, hyphens, and underscores only)")
    return strategy_name

def time_period_selector_component(label: str = "Select Time Period") -> tuple[date, date]:
    """Component for selecting a time period with validation."""
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today().replace(day=1), key="start_date")
    with col2:
        end_date = st.date_input("End Date", value=date.today(), key="end_date")
    
    # Validate that start date is before end date
    if start_date > end_date:
        st.warning("Start date should be before end date")
    
    return start_date, end_date

def form_validation_component(form_data: dict) -> List[str]:
    """Validate form data and return list of errors."""
    errors = []
    
    # Validate strategy name (if provided)
    strategy_name = form_data.get("strategy_name", "")
    if strategy_name and not is_valid_strategy_name(strategy_name):
        errors.append("Strategy name contains invalid characters. Only letters, numbers, spaces, hyphens, and underscores are allowed.")
    
    # Validate time period
    start_date = form_data.get("start_date")
    end_date = form_data.get("end_date")
    if start_date and end_date and start_date > end_date:
        errors.append("Start date must be before end date.")
    
    return errors

def is_valid_strategy_name(name: str) -> bool:
    """Check if a strategy name is valid."""
    # Allow letters, numbers, spaces, hyphens, and underscores only
    pattern = r'^[a-zA-Z0-9 _-]+$'
    return bool(re.match(pattern, name)) and len(name.strip()) > 0

def progress_component(progress: float, text: str = "Processing..."):
    st.progress(progress)
    st.write(text)

def error_message_component(message: str):
    st.error(message)

def section_header(text: str):
    st.markdown(f"## {text}")

def info_message_component(message: str):
    st.info(message)

def success_message_component(message: str):
    st.success(message)