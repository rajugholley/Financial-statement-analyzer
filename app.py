# app.py
import streamlit as st
import os
from aisetup import get_llm_response, authenticate
import pdfplumber

# Page config
st.set_page_config(page_title="Financial Statement Analyzer", layout="wide")

analysis_descriptions = {
    "Financial Statements Only": "Analysis of key financial metrics, ratios, and performance indicators",
    "Management Commentary Analysis": "Review of management's discussion, strategic outlook, and key initiatives",
    "Risk Factors Assessment": "Analysis of disclosed risks and their potential impact",
    "Management Commentary vs Financial Performance": "Alignment between management's narrative and actual financial results"
}

# Your FinancialDocumentAnalyzer class here
class FinancialDocumentAnalyzer:
    def __init__(self):
        pass

    #----------- this function defined the logic to extract text from pdf -------- #
    def extract_text_from_pdf(self, pdf_file, start_page=1, end_page=None):
        """Extract text from specific pages of PDF file"""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                # Adjust page numbers to 0-based index
                start_idx = start_page - 1
                end_idx = end_page if end_page is not None else len(pdf.pages)
                
                # Get text from selected pages
                for page_num in range(start_idx, end_idx):
                    if page_num < len(pdf.pages):
                        text += pdf.pages[page_num].extract_text() + "\n"
                return text
        except Exception as e:
            return f"Error extracting PDF text: {str(e)}"
        
    # ----------this function defines the main prompt that is passed to the LLM for financial statement analysis & insights -------- #

    def analyze_document(self, text, analysis_type="Financial Statements Only"):
    
    # Different prompts for different analysis types
        prompts = {
            "Financial Statements Only": """
            Analyze the financial data and provide SPECIFIC NUMERICAL calculations:

        1. Revenue Analysis:
           - Extract exact revenue numbers
           - Calculate YoY growth rates with percentages
           - Show all calculations explicitly

        2. Profitability Metrics:
           - Gross Profit Margin = (Revenue - COGS) / Revenue × 100
           - Operating Margin = Operating Income / Revenue × 100
           - Net Profit Margin = Net Income / Revenue × 100
           [Show all calculations with actual numbers]

        3. Balance Sheet Ratios:
           - Current Ratio = Current Assets / Current Liabilities
           - Quick Ratio = (Current Assets - Inventory) / Current Liabilities
           - Debt-to-Equity = Total Liabilities / Total Equity
           [Calculate using actual numbers]

        4. Cash Flow Analysis:
           - Operating Cash Flow Ratio
           - Free Cash Flow calculations
           [Show detailed calculations]

        Important: 
        - Extract and use actual numbers from the text
        - Show all calculations step by step
        - Present results in table format where possible
        - Include numerical values for all metrics

        Document Text:
        {text}
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
    # Initialize OpenAI first
    authenticate(st.secrets["openai"])
    
    st.title("📊 Financial Statement Analyzer")
    st.write("Upload financial statements for automated analysis")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="pdf_uploader")

    if uploaded_file is not None:
        try:
            # Create analyzer instance
            analyzer = FinancialDocumentAnalyzer()
            
            # First get total pages
            with pdfplumber.open(uploaded_file) as pdf:
                total_pages = len(pdf.pages)
                st.write(f"Total pages in document: {total_pages}")

            # Section selection
            section_option = st.selectbox(
                "Select Document Section to Analyze",
                [
                    "Financial Tables Only",
                    "Management Discussion Section",
                    "Risk Factors Section",
                    "Custom Page Range"
                ],
                key="section_select"
            )

            # Page range selection based on section
            if section_option == "Custom Page Range":
                col1, col2 = st.columns(2)
                with col1:
                    start_page = st.number_input("Start Page", min_value=1, max_value=total_pages, value=1)
                with col2:
                    end_page = st.number_input("End Page", min_value=1, max_value=total_pages, value=min(5, total_pages))
            else:
                # Default ranges based on section (these should be adjusted based on document structure)
                page_ranges = {
                    "Financial Tables Only": (1, 5),
                    "Management Discussion Section": (6, 10),
                    "Risk Factors Section": (11, 15)
                }
                start_page, end_page = page_ranges.get(section_option, (1, 5))

            # Analysis type selection
            analysis_type = st.selectbox(
                "Select Analysis Type",
                [
                    "Financial Statements Only",
                    "Management Commentary Analysis",
                    "Risk Factors Assessment",
                    "Management Commentary vs Financial Performance",
                ],
                key="analysis_type_select"
            )

            if st.button("Analyze"):
                with st.spinner('Analyzing document...'):
                    # Extract text from selected pages only
                    text = analyzer.extract_text_from_pdf(uploaded_file, start_page, end_page)
                    if text.startswith("Error"):
                        st.error(text)
                    else:
                        analysis = analyzer.analyze_document(text, analysis_type)
                        st.write(analysis)

        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")

if __name__ == "__main__":
    main()