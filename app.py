import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="PixelForge AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for maroon and cream theme
st.markdown("""
<style>
    /* Import elegant fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;600&display=swap');
    
    /* Main theme colors */
    :root {
        --primary-maroon: #7d3c4d;
        --deep-maroon: #5a2a36;
        --light-maroon: #9d5063;
        --cream: #f5e6d3;
        --light-cream: #faf5ed;
        --dark-cream: #e8d5b7;
        --accent-gold: #d4af37;
    }
    
    /* Global styles */
    .main {
        background: linear-gradient(135deg, #5a2a36 0%, #7d3c4d 50%, #8b4356 100%);
        font-family: 'Lato', sans-serif;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header */
    .main-header {
        background: linear-gradient(135deg, rgba(90, 42, 54, 0.95) 0%, rgba(125, 60, 77, 0.95) 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
        border: 2px solid rgba(212, 175, 55, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .main-header h1 {
        color: var(--cream);
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        font-family: 'Playfair Display', serif;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5);
        letter-spacing: 2px;
    }
    
    .main-header p {
        color: var(--light-cream);
        font-size: 1.2rem;
        margin-top: 0.8rem;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(125, 60, 77, 0.9) 0%, rgba(90, 42, 54, 0.9) 100%);
        padding: 2rem;
        border-radius: 15px;
        color: var(--cream);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(212, 175, 55, 0.2);
        transition: all 0.4s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 35px rgba(212, 175, 55, 0.3);
        border-color: rgba(212, 175, 55, 0.5);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: var(--accent-gold);
        font-family: 'Playfair Display', serif;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.95;
        color: var(--light-cream);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 300;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #3d1f28 0%, #5a2a36 100%);
        border-right: 2px solid rgba(212, 175, 55, 0.2);
    }
    
    [data-testid="stSidebar"] * {
        color: var(--cream) !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #7d3c4d 0%, #9d5063 100%);
        color: var(--cream);
        border: 2px solid var(--accent-gold);
        border-radius: 12px;
        padding: 0.8rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.4s ease;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.5);
        background: linear-gradient(135deg, #9d5063 0%, #b86578 100%);
        border-color: var(--accent-gold);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(125, 60, 77, 0.3);
        border: 3px dashed var(--accent-gold);
        border-radius: 15px;
        padding: 2.5rem;
        backdrop-filter: blur(5px);
    }
    
    [data-testid="stFileUploader"] label {
        color: var(--cream) !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(90, 42, 54, 0.4);
        padding: 10px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(125, 60, 77, 0.5);
        border-radius: 10px;
        padding: 12px 24px;
        color: var(--cream);
        font-weight: 600;
        border: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7d3c4d 0%, #9d5063 100%);
        color: var(--accent-gold);
        border: 2px solid var(--accent-gold);
    }
    
    /* Image container */
    .image-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
        border: 3px solid rgba(212, 175, 55, 0.3);
        transition: all 0.4s ease;
    }
    
    .image-container:hover {
        transform: scale(1.03);
        box-shadow: 0 20px 50px rgba(212, 175, 55, 0.4);
        border-color: var(--accent-gold);
    }
    
    /* Text styling */
    h1, h2, h3, h4, h5, h6 {
        color: var(--cream) !important;
        font-family: 'Playfair Display', serif !important;
    }
    
    p, span, div, label {
        color: var(--light-cream) !important;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        background: rgba(125, 60, 77, 0.2);
        border-radius: 12px;
        border: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    /* Slider styling */
    .stSlider [data-baseweb="slider"] {
        background: rgba(125, 60, 77, 0.3);
    }
    
    .stSlider [role="slider"] {
        background: var(--accent-gold) !important;
        border: 2px solid var(--cream) !important;
    }
    
    /* Select box styling */
    [data-baseweb="select"] {
        background: rgba(125, 60, 77, 0.8) !important;
        border: 2px solid rgba(212, 175, 55, 0.5) !important;
        border-radius: 10px !important;
    }
    
    [data-baseweb="select"] > div {
        background: rgba(125, 60, 77, 0.8) !important;
        color: var(--cream) !important;
    }
    
    /* Select dropdown */
    [role="listbox"] {
        background: rgba(90, 42, 54, 0.95) !important;
        border: 2px solid var(--accent-gold) !important;
    }
    
    [role="option"] {
        background: rgba(125, 60, 77, 0.8) !important;
        color: var(--cream) !important;
    }
    
    [role="option"]:hover {
        background: rgba(157, 80, 99, 0.9) !important;
        color: var(--accent-gold) !important;
    }
    
    /* Download button specific styling */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%) !important;
        color: #3d1f28 !important;
        border: 2px solid #f5e6d3 !important;
        border-radius: 12px;
        padding: 0.8rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.4s ease;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.6);
        background: linear-gradient(135deg, #f5c84c 0%, #d4af37 100%) !important;
        border-color: var(--cream) !important;
    }
    
    /* Info/success boxes */
    .stAlert {
        background: rgba(125, 60, 77, 0.6) !important;
        color: var(--cream) !important;
        border: 2px solid var(--accent-gold) !important;
        border-radius: 12px !important;
    }
    
    /* Color palette display */
    .color-box {
        border-radius: 10px;
        border: 2px solid var(--accent-gold);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .color-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_images' not in st.session_state:
    st.session_state.processed_images = []
if 'image_history' not in st.session_state:
    st.session_state.image_history = []

# Header
st.markdown("""
<div class="main-header">
    <h1>PixelForge AI</h1>
    <p>Professional Image Analysis & Enhancement Platform</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=80)
    st.title("Control Panel")
    
    st.markdown("---")
    
    app_mode = st.selectbox(
        "Select Mode",
        ["Upload & Analyze", "Image Enhancement", "Batch Analysis", "Analytics Dashboard"]
    )
    
    st.markdown("---")
    
    if app_mode in ["Upload & Analyze", "Image Enhancement"]:
        st.subheader("Settings")
        
        quality = st.slider("Quality", 1, 100, 85)
        show_metadata = st.checkbox("Show Metadata", value=True)
        auto_enhance = st.checkbox("Auto Enhance", value=False)

# Main content area
if app_mode == "Upload & Analyze":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'webp'],
            help="Upload an image to analyze"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(image, caption="Original Image", width=None)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Store in history
            if uploaded_file.name not in [img['name'] for img in st.session_state.image_history]:
                st.session_state.image_history.append({
                    'name': uploaded_file.name,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'size': uploaded_file.size
                })
    
    with col2:
        if uploaded_file:
            st.subheader("Image Analysis")
            
            # Get image properties
            width, height = image.size
            mode = image.mode
            format_type = image.format if hasattr(image, 'format') else 'N/A'
            file_size = uploaded_file.size / 1024  # KB
            
            # Display metrics in cards
            metric_col1, metric_col2 = st.columns(2)
            
            with metric_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Dimensions</div>
                    <div class="metric-value">{width}x{height}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">File Size</div>
                    <div class="metric-value">{file_size:.2f} KB</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Color Mode</div>
                    <div class="metric-value">{mode}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Format</div>
                    <div class="metric-value">{format_type}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Color analysis
            st.subheader("Color Analysis")
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image_rgb = image.convert('RGB')
            else:
                image_rgb = image
            
            # Sample colors
            img_array = np.array(image_rgb.resize((100, 100)))
            colors = img_array.reshape(-1, 3)
            
            # Get dominant colors
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            kmeans.fit(colors)
            dominant_colors = kmeans.cluster_centers_.astype(int)
            
            # Display color palette
            color_cols = st.columns(5)
            for idx, (col, color) in enumerate(zip(color_cols, dominant_colors)):
                with col:
                    st.markdown(f"""
                    <div class="color-box" style="background-color: rgb({color[0]}, {color[1]}, {color[2]}); 
                                height: 100px; margin: 5px;"></div>
                    <p style="text-align: center; font-size: 0.9rem; margin-top: 8px; color: var(--accent-gold); font-weight: 600;">
                        #{color[0]:02x}{color[1]:02x}{color[2]:02x}
                    </p>
                    """, unsafe_allow_html=True)

elif app_mode == "Image Enhancement":
    st.subheader("Image Enhancement Tools")
    
    uploaded_file = st.file_uploader("Upload image to enhance", type=['png', 'jpg', 'jpeg', 'webp'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Original")
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(image, width=None)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Enhanced")
            
            # Enhancement options
            tabs = st.tabs(["Brightness", "Contrast", "Sharpness", "Saturation", "Filters"])
            
            enhanced_image = image.copy()
            
            with tabs[0]:
                brightness = st.slider("Brightness", 0.0, 2.0, 1.0, 0.1)
                enhancer = ImageEnhance.Brightness(enhanced_image)
                enhanced_image = enhancer.enhance(brightness)
            
            with tabs[1]:
                contrast = st.slider("Contrast", 0.0, 2.0, 1.0, 0.1)
                enhancer = ImageEnhance.Contrast(enhanced_image)
                enhanced_image = enhancer.enhance(contrast)
            
            with tabs[2]:
                sharpness = st.slider("Sharpness", 0.0, 2.0, 1.0, 0.1)
                enhancer = ImageEnhance.Sharpness(enhanced_image)
                enhanced_image = enhancer.enhance(sharpness)
            
            with tabs[3]:
                saturation = st.slider("Saturation", 0.0, 2.0, 1.0, 0.1)
                enhancer = ImageEnhance.Color(enhanced_image)
                enhanced_image = enhancer.enhance(saturation)
            
            with tabs[4]:
                filter_option = st.selectbox(
                    "Apply Filter",
                    ["None", "Blur", "Contour", "Detail", "Edge Enhance", "Smooth"]
                )
                
                if filter_option == "Blur":
                    enhanced_image = enhanced_image.filter(ImageFilter.BLUR)
                elif filter_option == "Contour":
                    enhanced_image = enhanced_image.filter(ImageFilter.CONTOUR)
                elif filter_option == "Detail":
                    enhanced_image = enhanced_image.filter(ImageFilter.DETAIL)
                elif filter_option == "Edge Enhance":
                    enhanced_image = enhanced_image.filter(ImageFilter.EDGE_ENHANCE)
                elif filter_option == "Smooth":
                    enhanced_image = enhanced_image.filter(ImageFilter.SMOOTH)
            
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(enhanced_image, width=None)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Download button
            buf = io.BytesIO()
            enhanced_image.save(buf, format='PNG')
            btn = st.download_button(
                label="Download Enhanced Image",
                data=buf.getvalue(),
                file_name=f"enhanced_{uploaded_file.name}",
                mime="image/png"
            )

elif app_mode == "Batch Analysis":
    st.subheader("Batch Image Analysis")
    
    uploaded_files = st.file_uploader(
        "Upload multiple images",
        type=['png', 'jpg', 'jpeg', 'webp'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"{len(uploaded_files)} images uploaded successfully!")
        
        # Create analysis dataframe
        analysis_data = []
        
        cols = st.columns(4)
        for idx, file in enumerate(uploaded_files):
            image = Image.open(file)
            width, height = image.size
            
            analysis_data.append({
                'Filename': file.name,
                'Width': width,
                'Height': height,
                'Aspect Ratio': f"{width/height:.2f}",
                'Size (KB)': f"{file.size/1024:.2f}",
                'Mode': image.mode
            })
            
            with cols[idx % 4]:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(image, caption=file.name, width=None)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Display analysis table
        st.markdown("---")
        st.subheader("Analysis Results")
        df = pd.DataFrame(analysis_data)
        st.dataframe(df, use_container_width=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(df, x='Filename', y='Width', title='Image Widths Comparison',
                        color_discrete_sequence=['#d4af37'])
            fig.update_layout(
                plot_bgcolor='rgba(90, 42, 54, 0.3)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f5e6d3')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            sizes = [float(s) for s in df['Size (KB)']]
            fig = px.pie(values=sizes, names=df['Filename'], title='File Size Distribution',
                        color_discrete_sequence=px.colors.sequential.Sunset)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f5e6d3')
            )
            st.plotly_chart(fig, use_container_width=True)

elif app_mode == "Analytics Dashboard":
    st.subheader("Analytics Dashboard")
    
    if len(st.session_state.image_history) == 0:
        st.info("No images processed yet. Upload some images to see analytics!")
    else:
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Images</div>
                <div class="metric-value">{len(st.session_state.image_history)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_size = sum([img['size'] for img in st.session_state.image_history]) / (1024 * 1024)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Size</div>
                <div class="metric-value">{total_size:.2f} MB</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_size = sum([img['size'] for img in st.session_state.image_history]) / len(st.session_state.image_history) / 1024
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Size</div>
                <div class="metric-value">{avg_size:.2f} KB</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Status</div>
                <div class="metric-value">Active</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # History table
        st.subheader("Processing History")
        df = pd.DataFrame(st.session_state.image_history)
        st.dataframe(df, use_container_width=True)
        
        # Timeline chart
        st.subheader("Processing Timeline")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['size_mb'] = df['size'] / (1024 * 1024)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['size_mb'],
            mode='lines+markers',
            name='File Size',
            line=dict(color='#d4af37', width=3),
            marker=dict(size=12, color='#d4af37', line=dict(color='#f5e6d3', width=2))
        ))
        
        fig.update_layout(
            title='Image Upload Timeline',
            xaxis_title='Time',
            yaxis_title='Size (MB)',
            plot_bgcolor='rgba(90, 42, 54, 0.3)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f5e6d3'),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem;'>
    <p style='font-size: 1.5rem; font-weight: 600; color: var(--accent-gold); font-family: "Playfair Display", serif;'>
        PixelForge AI
    </p>
    <p style='color: var(--cream); opacity: 0.8; font-size: 1rem; letter-spacing: 1px;'>
        Built with Streamlit • Powered by Python
    </p>
    <p style='color: var(--dark-cream); opacity: 0.6; font-size: 0.9rem; margin-top: 0.5rem;'>
        Where Pixels Meet Artificial Intelligence
    </p>
</div>
""", unsafe_allow_html=True)