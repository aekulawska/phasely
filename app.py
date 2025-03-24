import streamlit as st
import requests
import time
from dotenv import dotenv_values

# Configuration and Setup
st.set_page_config(
    page_title="Phasely 🌙",
    page_icon="🌸",
    layout="wide"
)

# Custom CSS for Boho-Chic Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
    
    body {
        background-color: #e7dbc7;
        font-family: 'Quicksand', sans-serif;
    }
    
    .stApp {
        background: #e7dbc7;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.7);
        border: 2px solid #E6C7B3;
        border-radius: 15px;
        color: #6D4C3D;
        font-family: 'Quicksand', sans-serif;
    }
    
    .stMultiSelect > div > div {
        background-color: rgba(255, 255, 255, 0.7);
        border: 2px solid #E6C7B3;
        border-radius: 15px;
        color: #6D4C3D;
    }
    
    .stButton > button {
        background-color: #E6C7B3;
        color: #6D4C3D;
        border: none;
        border-radius: 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #D2B48C;
        transform: scale(1.05);
    }
    
    .stExpander {
        border: 2px solid #E6C7B3;
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.6);
    }
    
    .nutrition-card h2 {
        margin-bottom: 25px;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    .nutrition-card h3 {
        margin-bottom: 20px;
        border-bottom: 2px solid #E6C7B3;
        padding-bottom: 10px;
    }
    
    .nutrition-card {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
        border: 2px solid #E6C7B3;
    }
    </style>
""", unsafe_allow_html=True)

# Main Application
def main():
    # Replace the title with centered logo
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <img src="https://raw.githubusercontent.com/aekulawska/phasely/refs/heads/main/Screenshot%202025-03-24%20at%2020.59.35.png" 
                 alt="Phasely Logo" 
                 style="width: 250px; margin-bottom: 2rem;">
        </div>
    """, unsafe_allow_html=True)

    # Cycle Day Input
    col1, col2 = st.columns([2, 1])
    with col1:
        cycle_day = st.slider(
            "What day of your menstrual cycle are you on?", 
            min_value=1, 
            max_value=30, 
            value=14
        )
    
    with col2:
        st.markdown("### Cycle Insights")
        if cycle_day <= 6:
            st.markdown("**Menstrual Phase**\nRest & Replenish")
        elif cycle_day <= 11:
            st.markdown("**Follicular Phase**\nEnergy Building")
        elif cycle_day <= 16:
            st.markdown("**Ovulation Phase**\nPeak Performance")
        else:
            st.markdown("**Luteal Phase**\nNourish & Balance")

    # Food Preferences Multi-Select
    food_preferences = st.multiselect(
        "Select your food preferences and dietary restrictions 🍽️",
        [
            "Vegetarian", 
            "Low-Carb", 
            "High-Protein",
            "Anti-Inflammatory"
        ]
    )

    # Dummy API Parameters (Replace with actual SnapLogic endpoint)
    URL = "https://emea.snaplogic.com/api/1/rest/slsched/feed/ConnectFasterInc/Aleksandra%20Kulawska/shared/nutrition_api"
    BEARER_TOKEN = "Uv83gcXtG0SOxmBXJ66NTTXHrKykYEeC"

    if st.button("Get Personalized Guidance"):
        with st.spinner("Crafting your personalized wisdom..."):
            # Prepare API Request
            data = {
                "cycle_day": cycle_day,
                "food_preferences": food_preferences
            }
            print(data)
            headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}

            try:
                response = requests.post(
                    url=URL,
                    json=data,
                    headers=headers,
                    timeout=300
                )

                print(response)

                if response.status_code == 200:
                    result = response.json()
                    
                    # Handle the specific response structure
                    if isinstance(result, list) and len(result) > 0:
                        if isinstance(result[0].get('answer'), list) and len(result[0]['answer']) > 0:
                            content = result[0]['answer'][0]
                            
                            # Split content into nutrition and lifestyle sections
                            sections = content.split('\n\n')
                            nutrition_content = []
                            lifestyle_content = []
                            current_section = None
                            
                            for section in sections:
                                if '1. NUTRITION GUIDANCE' in section:
                                    current_section = 'nutrition'
                                    # Skip the header itself
                                    continue
                                elif '2. LIFESTYLE RECOMMENDATIONS' in section:
                                    current_section = 'lifestyle'
                                    # Skip the header itself
                                    continue
                                elif section.strip():
                                    if current_section == 'nutrition':
                                        nutrition_content.append(section)
                                    elif current_section == 'lifestyle':
                                        lifestyle_content.append(section)
                            
                            # Format text helper function
                            def format_section_text(text):
                                # Split by newlines to handle each line
                                lines = text.split('\n')
                                formatted_lines = []
                                for line in lines:
                                    if line.startswith('- '):
                                        # Format bullet points with proper spacing
                                        formatted_line = f"• {line[2:]}"
                                        formatted_lines.append(f'<p style="color: #6D4C3D; margin-bottom: 10px; margin-left: 20px;">{formatted_line}</p>')
                                    else:
                                        # Regular text
                                        formatted_lines.append(f'<p style="color: #6D4C3D; margin-bottom: 15px;">{line}</p>')
                                return '\n'.join(formatted_lines)

                            # Display Nutrition Section
                            nutrition_html = f"""
                                <div class="nutrition-card">
                                    <h2 style="color: #8b654c; font-family: 'Quicksand', sans-serif; text-align: center;">
                                        ✨ Nourish Your Body ✨
                                    </h2>
                                    {''.join([format_section_text(section) for section in nutrition_content])}
                                </div>
                            """
                            st.markdown(nutrition_html, unsafe_allow_html=True)
                            
                            # Display Lifestyle Section
                            lifestyle_html = f"""
                                <div class="nutrition-card">
                                    <h2 style="color: #8b654c; font-family: 'Quicksand', sans-serif; text-align: center;">
                                        ✨ Nurture Your Spirit ✨
                                    </h2>
                                    {''.join([format_section_text(section) for section in lifestyle_content])}
                                </div>
                            """
                            st.markdown(lifestyle_html, unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="nutrition-card">', unsafe_allow_html=True)
                            st.markdown("No specific recommendations available.")
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="nutrition-card">', unsafe_allow_html=True)
                        st.markdown("No specific recommendations available.")
                        st.markdown('</div>', unsafe_allow_html=True)

                else:
                    st.error("Unable to fetch personalized recommendations.")

            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")

    # Footer Section
    st.markdown("---")
    st.markdown("""
    ### 💫 About Lunar Cycle Nutrition
    Every menstrual cycle is unique. Our guide helps you understand 
    your body's changing nutritional needs throughout your cycle.
    """)

if __name__ == "__main__":
    main()