import streamlit as st
from src.app.ui_components import (
    file_upload_component, progress_component, error_message_component, 
    section_header, strategy_input_component, time_period_selector_component,
    form_validation_component, info_message_component, success_message_component
)
import pandas as pd
from datetime import datetime
from src.app.main_controller import MainController
from src.config import Config
from src.config_loader import ConfigLoader
import os

def main():
    st.set_page_config(page_title="Trading Journal Analytics", layout="wide")
    
    # Validate environment configuration at startup
    is_valid, error_message = Config.validate()
    if not is_valid:
        st.error(f"Configuration Error: {error_message}")
        st.info("Please check your environment variables and try again.")
        return
    
    # Load application configuration
    try:
        # Determine config file path
        workspace_root = Config.get_workspace_root()
        if workspace_root:
            config_path = os.path.join(workspace_root, "data", "config.json")
        else:
            config_path = "data/config.json"
        
        config_loader = ConfigLoader(config_path)
        app_config = config_loader.load_config()
        st.session_state.app_config = app_config
    except FileNotFoundError as e:
        st.error(f"Configuration File Error: {str(e)}")
        st.info("Please ensure the configuration file exists at the expected location.")
        return
    except Exception as e:
        st.error(f"Configuration Error: {str(e)}")
        st.info("Please check your configuration file format and content.")
        return
    
    st.title("Trading Journal Analytics")
    
    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["📁 Upload & Process", "📊 Analysis", "⚙️ Settings"])
    
    with tab1:
        section_header("📁 Upload TastyTrade CSV")
        uploaded_file = file_upload_component()
        
        # Additional form elements for strategy and time period
        st.subheader("Analysis Parameters")
        strategy_name = strategy_input_component("Strategy Name (Optional)")
        
        st.subheader("Time Period")
        start_date, end_date = time_period_selector_component()
        
        # Validate form data
        form_data = {
            "strategy_name": strategy_name,
            "start_date": start_date,
            "end_date": end_date
        }
        form_errors = form_validation_component(form_data)
        
        if form_errors:
            for error in form_errors:
                error_message_component(error)
        
        # Store form data in session state with unique keys
        if 'stored_strategy_name' not in st.session_state:
            st.session_state.stored_strategy_name = strategy_name
        if 'stored_start_date' not in st.session_state:
            st.session_state.stored_start_date = start_date
        if 'stored_end_date' not in st.session_state:
            st.session_state.stored_end_date = end_date
        
        controller = MainController()
        if uploaded_file and not form_errors:
            try:
                progress_component(0.1, "Processing CSV...")
                if not controller.process_csv(uploaded_file):
                    error_message_component(controller.get_error())
                    return
                progress_component(0.3, "Analyzing trades...")
                if not controller.analyze_trades():
                    error_message_component(controller.get_error())
                    return
                progress_component(0.5, "Generating LLM insights...")
                if not controller.generate_llm_insights():
                    error_message_component(controller.get_error())
                    return
                progress_component(0.7, "Generating charts...")
                if not controller.generate_charts():
                    error_message_component(controller.get_error())
                    return
                progress_component(0.85, "Assembling report...")
                if not controller.assemble_report():
                    error_message_component(controller.get_error())
                    return
                progress_component(1.0, "Exporting report...")
                download_link = controller.export_report()
                if not download_link:
                    error_message_component(controller.get_error())
                    return
                success_message_component("Report generated successfully!")
                section_header("💾 Download Markdown Report")
                st.markdown(download_link, unsafe_allow_html=True)
            except Exception as e:
                error_message_component(f"Error: {e}")
        elif uploaded_file and form_errors:
            error_message_component("Please fix the form errors before processing.")
        else:
            info_message_component("Upload a CSV file and fill in the analysis parameters to get started.")
    
    with tab2:
        section_header("📊 Performance Metrics Dashboard")
        st.info("Performance metrics and charts will appear here after upload.")
        section_header("📈 Static Charts Display")
        st.info("Charts will appear here after analysis.")
        section_header("📝 LLM Analysis & Reflection Questions")
        st.info("LLM-generated insights will appear here after analysis.")
    
    with tab3:
        section_header("⚙️ Application Settings")
        st.info("Configuration settings will appear here.")

if __name__ == "__main__":
    main() 