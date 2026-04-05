import streamlit as st
import asyncio
import os
import json
from agent_ppt import graph

st.set_page_config(
    page_title="AI PPT Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Styling (Cyberpunk/Futuristic) ---
def local_css():
    st.markdown(
        """
        <style>
        /* Page Background */
        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #ffffff;
        }

        /* Hide white top header bar */
        [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Glassmorphism Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            border-radius: 15px;
            padding: 24px;
            margin-bottom: 24px;
            transition: transform 0.3s ease, background 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.08);
        }

        .slide-title {
            color: #00f2fe;
            font-size: 1.6em;
            margin-bottom: 15px;
            font-weight: 600;
        }

        .slide-bullet {
            color: #e0e0e0;
            margin-bottom: 8px;
            font-size: 1.1em;
            line-height: 1.5;
        }

        /* Neon Header */
        .neon-text {
            font-size: 3.5em;
            font-weight: 900;
            text-transform: uppercase;
            background: -webkit-linear-gradient(#00f2fe, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0px 0px 10px rgba(79, 172, 254, 0.4);
            text-align: center;
            margin-top: 0px;
            margin-bottom: 40px;
            animation: glow 2s ease-in-out infinite alternate;
        }

        /* Adjust main app alignment to remove default top gap */
        .block-container {
            padding-top: 3rem !important;
        }

        @keyframes glow {
          from { text-shadow: 0 0 10px #00f2fe, 0 0 20px #00f2fe; }
          to { text-shadow: 0 0 20px #4facfe, 0 0 30px #4facfe; }
        }

        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #00c6ff, #0072ff) !important;
            color: white !important;
            border: none;
            border-radius: 25px;
            padding: 10px 24px;
            font-size: 1.1em;
            font-weight: bold;
            box-shadow: 0 4px 15px 0 rgba(0, 114, 255, 0.5);
            transition: all 0.3s ease 0s;
            width: 100%;
        }

        .stButton>button:hover {
            box-shadow: 0 4px 15px 0 rgba(0, 114, 255, 0.8);
            transform: translateY(-2px);
            background: linear-gradient(135deg, #0072ff, #00c6ff) !important;
        }
        
        .stDownloadButton>button {
            background: linear-gradient(135deg, #f12711, #f5af19) !important;
            box-shadow: 0 4px 15px 0 rgba(245, 175, 25, 0.5);
        }
        
        .stDownloadButton>button:hover {
            box-shadow: 0 4px 15px 0 rgba(245, 175, 25, 0.8);
            background: linear-gradient(135deg, #f5af19, #f12711) !important;
        }

        /* Sidebar Customization */
        [data-testid="stSidebar"] {
            background-color: rgba(15, 12, 41, 0.8) !important;
            backdrop-filter: blur(15px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .sidebar-title {
            color: #00c6ff;
            text-align: center;
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 20px;
        }

        .sidebar-text {
            color: #00c6ff !important;
            font-size: 1.1em;
            line-height: 1.5;
            margin-bottom: 20px;
        }
        
        /* Headers & Text */
        h1, h2, h3, p, span {
            color: #ffffff !important;
        }
        
        .stTextInput label p {
            color: #00f2fe !important;
            font-size: 1.1em;
            font-weight: 600;
        }
        
        /* Inputs */
        div[data-baseweb="input"] {
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Async Function for LangGraph ---
async def generate_ppt_async(topic, status_container):
    status_container.update(label="🚀 Planning slides...", state="running", expanded=True)
    
    final_state = None
    try:
        # We iterate over steps to give progress updates
        async for output in graph.astream({"topic": topic}):
            for node_name, state in output.items():
                if node_name == "plan":
                    status_container.update(label="📝 Generating content and Layout...", state="running")
                elif node_name == "create":
                    status_container.update(label="🎨 Compiling PPTX with MCP...", state="running")
                final_state = state
                
        status_container.update(label="✅ Presentation ready!", state="complete", expanded=False)
        return final_state
    except Exception as e:
        status_container.update(label=f"❌ Error: {str(e)}", state="error", expanded=True)
        return None

# --- Main App Logic ---
def main():
    local_css()

    if "slides" not in st.session_state:
        st.session_state.slides = []
    if "ppt_ready" not in st.session_state:
        st.session_state.ppt_ready = False
    
    # -- Sidebar --
    with st.sidebar:
        st.markdown('<div class="sidebar-title">⚡ AI PPT Generator</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-text">Generate a full PowerPoint presentation from just a topic, completely AI-powered.</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        topic_input = st.text_input("Enter a topic:", placeholder="e.g. The Future of AI in Space")
        
        generate_btn = st.button("🚀 Generate Presentation")
        
        st.markdown("---")
        st.markdown("<small style='color:#a0a0a0;'>Built with LangChain + MCP + Streamlit</small>", unsafe_allow_html=True)

    # -- Main Content --
    st.markdown('<div class="neon-text">NeuroSlides</div>', unsafe_allow_html=True)
    
    if generate_btn:
        if not topic_input.strip():
            st.error("⚠️ Please enter a topic first.")
        else:
            st.session_state.slides = []
            st.session_state.ppt_ready = False
            
            # Use status container for progress
            status = st.status("Initializing AI engine...", expanded=True)
            
            # Run the graph integration
            state_result = asyncio.run(generate_ppt_async(topic_input, status))
            
            if state_result and "slides" in state_result:
                st.session_state.slides = state_result["slides"]
                st.session_state.ppt_ready = True
                st.success("🎉 Generation Successful!")
            else:
                st.error("Failed to generate presentation. Verify your API keys and quotas.")

    # -- Display Generated Slides --
    if st.session_state.slides:
        st.markdown("### 📊 Slide Previews", unsafe_allow_html=True)
        
        # Use columns for grid layout
        col1, col2 = st.columns(2)
        
        for i, slide in enumerate(st.session_state.slides):
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                # Generate Glassmorphism Card HTML
                bullets_html = "".join([f'<li class="slide-bullet">{point}</li>' for point in slide.get("content", [])])
                
                card_html = f"""
                <div class="glass-card">
                    <div class="slide-title">Slide {i+1}: {slide.get('title', 'Unknown')}</div>
                    <ul>
                        {bullets_html}
                    </ul>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
    
    # -- Download Section --
    if st.session_state.ppt_ready:
        st.markdown("---")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("<h3 style='text-align:center;'>📁 Download your Presentation</h3>", unsafe_allow_html=True)
            
            ppt_path = "ppt_storage/output.pptx"
            if os.path.exists(ppt_path):
                with open(ppt_path, "rb") as file:
                    st.download_button(
                        label="⬇️ Download PPT as .pptx",
                        data=file,
                        file_name="AI_Presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True
                    )
            else:
                st.error("PPT file not found output directory.")

if __name__ == "__main__":
    main()
