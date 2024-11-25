# app.py
import streamlit as st
import os
from aisetup import get_llm_response, authenticate
import pdfplumber

# Page config
st.set_page_config(page_title="Financial Statement Analyzer", layout="wide")

# Your FinancialDocumentAnalyzer class here
class FinancialDocumentAnalyzer:
    def __init__(self):
        pass

    #----------- this function defined the logic to extract text from pdf -------- #
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error extracting PDF text: {str(e)}"

    
    # ----------this function defines the main prompt that is passed to the LLM for financial statement analysis & insights -------- #

    def analyze_document(self, text, analysis_type="Financial Statements Only"):
    
    # Different prompts for different analysis types
        prompts = {
            "Financial Statements Only": """
            Analyze the financial statements section focusing only on numerical data and metrics.
            
            Provide analysis of:
            1. Key Financial Metrics:
            - Revenue, Profit margins
            - Cash flow metrics
            - Balance sheet ratios
            
            2. Performance Indicators:
            - YoY growth rates
            - Profitability trends
            - Liquidity position
            
            3. Financial Health:
            - Key ratios analysis
            - Working capital
            - Debt metrics
            
            Focus only on quantitative analysis and financial metrics.
            """,
            
            "Management Commentary Analysis": """
            Analyze the management discussion section focusing on:
            
            1. Strategic Initiatives:
            - Key business strategies
            - Market expansion plans
            - Product/Service initiatives
            
            2. Business Outlook:
            - Future projections
            - Market conditions
            - Growth expectations
            
            3. Key Developments:
            - Major business updates
            - Operational changes
            - Strategic decisions
            
            Focus on qualitative analysis from management's perspective.
            """,
            
            "Risk Factors Assessment": """
            Analyze the risk factors and provide:
            
            1. Key Risk Categories:
            - Market risks
            - Operational risks
            - Financial risks
            - Regulatory risks
            
            2. Risk Impact Analysis:
            - Potential business impact
            - Mitigation strategies
            - Risk prioritization
            
            Focus on identifying and analyzing disclosed risks.
            """,
            
            "Management Commentary vs Financial Performance": """
            Compare management's commentary with actual financial performance:
            
            1. Alignment Analysis:
            - Stated objectives vs results
            - Growth projections vs actual
            - Strategic goals vs achievements
            
            2. Gap Analysis:
            - Identify discrepancies
            - Explain variations
            - Highlight achievements
            
            Focus on correlation between management statements and financial results.
            """
        }
        
        # Get appropriate prompt
        selected_prompt = prompts[analysis_type]
        
        # Add document text to prompt
        full_prompt = f"""
        {selected_prompt}

        Document Text:
        {text}

        Provide analysis in clear, structured format with headers and bullet points.
        """
        
        try:
            return get_llm_response(full_prompt)
        except Exception as e:
            return f"Error in analysis: {str(e)}"
    
    # ----------this function defines the prompt for LLM to compare two financial statement and then provides a comparative analysis.  -------- #
  
    def compare_statements(self, text1, text2, period1="Current", period2="Previous"):
        """Compare two financial statements"""
        compare_prompt = f"""
        Compare these two financial statements and provide structured analysis:

        1. Key Metrics Comparison:
           - Revenue comparison
           - Profit metrics
           - Key ratios
           
        2. Major Changes:
           - Significant increases
           - Notable decreases
           - Important shifts
           
        3. Performance Analysis:
           - Overall health comparison
           - Risk assessment
           - Opportunity areas

        Statement 1 ({period1}):
        {text1}

        Statement 2 ({period2}):
        {text2}

        Provide analysis in clear, structured format with numbers and percentages.
        """

        # ----------this is where prompts are passed to LLM and response from the LLM is returned in the get_llm_response()  -------- #

        try:
            return get_llm_response(compare_prompt)
        except Exception as e:
            return f"Error in comparison: {str(e)}"
            

# Main app logic
def main():
    st.title("📊 Financial Statement Analyzer")
    st.write("Upload financial statements for automated analysis")

    # Single instance of selectbox
    analysis_type = st.selectbox(
        "Select Analysis Type",
        [
            "Financial Statements Only",
            "Management Commentary Analysis",
            "Risk Factors Assessment",
            "Management Commentary vs Financial Performance",
        ],
        key="analysis_type_select"  # Add unique key
    )

    # Description
    analysis_descriptions = {
        "Financial Statements Only": "Analysis of key financial metrics, ratios, and performance indicators",
        "Management Commentary Analysis": "Review of management's discussion, strategic outlook, and key initiatives",
        "Risk Factors Assessment": "Analysis of disclosed risks and their potential impact",
        "Management Commentary vs Financial Performance": "Alignment between management's narrative and actual financial results"
    }

    st.write(analysis_descriptions[analysis_type])

    # Single file uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="pdf_uploader")

    if uploaded_file is not None:
        with st.spinner('Analyzing document...'):
            text = analyzer.extract_text_from_pdf(uploaded_file)
            if text.startswith("Error"):
                st.error(text)
            else:
                analysis = analyzer.analyze_document(text, analysis_type)
                st.write(analysis)

if __name__ == "__main__":
    main()