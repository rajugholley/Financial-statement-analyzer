# app.py
import streamlit as st
import os
from aisetup import get_llm_response, authenticate
import pdfplumber

# Page config
st.set_page_config(page_title="Financial Statement Analyzer", layout="wide")

# Title
st.title("📊 Financial Statement Analyzer")
st.write("Upload financial statements for automated analysis")

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

    def analyze_document(self, text, document_type="financial_statement"):
        prompt = f"""
        You are a senior financial analyst. Analyze this {document_type} and provide analysis.
    Present calculations in simple format, like "Gross Profit Margin = $1.9M / $4.8M = 39.58%"
    Do NOT use LaTeX formatting or backslashes.
        
        1. Financial Health Indicators:
           - Profitability ratios
           - Liquidity assessment
           - Operational efficiency
        
        2. Business Performance:
           - Year-over-year growth rates
           - Industry benchmark comparison
           - Key performance trends
        
        3. Risk Assessment:
           - Financial leverage
           - Cash flow stability
           - Operational risks
        
        4. Strategic Recommendations:
           - Areas for improvement
           - Potential opportunities
           - Suggested actions
        
        Document Text:
        {text}
        
        Provide detailed analysis with specific metrics where possible. Use industry standard calculations.
        """   
        try:
            return get_llm_response(prompt)
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

    authenticate(st.secrets["openai"]) 

    analyzer = FinancialDocumentAnalyzer()
    
    # File upload
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner('Analyzing document...'):
            # Extract text
            text = analyzer.extract_text_from_pdf(uploaded_file)
            
            # Show analysis
            if text.startswith("Error"):
                st.error(text)
            else:
                analysis = analyzer.analyze_document(text)
                st.write(analysis)

if __name__ == "__main__":
    main()