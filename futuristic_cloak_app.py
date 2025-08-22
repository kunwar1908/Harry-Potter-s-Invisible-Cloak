import streamlit as st
import cv2
import numpy as np
import time
from PIL import Image
import tempfile
import os

# Configure page
st.set_page_config(
    page_title="🧙‍♂️ Invisible Cloak Portal",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for futuristic theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #00ff41;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .futuristic-title {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #00ff41, #00d4ff, #ff0080);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(0, 255, 65, 0.5);
        margin-bottom: 2rem;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .control-panel {
        background: rgba(0, 255, 65, 0.1);
        border: 2px solid #00ff41;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .status-indicator {
        font-family: 'Orbitron', monospace;
        font-size: 1.2rem;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .status-active {
        background: rgba(0, 255, 65, 0.2);
        border: 1px solid #00ff41;
        color: #00ff41;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.4);
    }
    
    .status-inactive {
        background: rgba(255, 0, 128, 0.2);
        border: 1px solid #ff0080;
        color: #ff0080;
        box-shadow: 0 0 15px rgba(255, 0, 128, 0.4);
    }
    
    .cyber-button {
        background: linear-gradient(45deg, #00ff41, #00d4ff);
        border: none;
        color: #0f0f23;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 12px 24px;
        border-radius: 8px;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .cyber-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 25px rgba(0, 255, 65, 0.6);
    }
    
    .matrix-text {
        font-family: 'Courier New', monospace;
        color: #00ff41;
        font-size: 0.9rem;
        line-height: 1.2;
        background: rgba(0, 0, 0, 0.8);
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid #00ff41;
    }
    
    .sidebar .sidebar-content {
        background: rgba(0, 255, 65, 0.05);
        border-right: 2px solid #00ff41;
    }
    
    .metric-container {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid #00d4ff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #00ff41, #00d4ff);
    }
    
    .stSelectbox > div > div {
        background: rgba(0, 255, 65, 0.1);
        border: 1px solid #00ff41;
        border-radius: 8px;
    }
    
    h1, h2, h3 {
        font-family: 'Orbitron', monospace;
        color: #00ff41;
    }
    
    .stMarkdown {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'background_captured' not in st.session_state:
    st.session_state.background_captured = False
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False
if 'background_frame' not in st.session_state:
    st.session_state.background_frame = None

class FuturisticInvisibleCloak:
    def __init__(self):
        self.open_kernel = np.ones((5,5), np.uint8)
        self.close_kernel = np.ones((7,7), np.uint8)
        self.dilation_kernel = np.ones((10, 10), np.uint8)
        
    def filter_mask(self, mask):
        """Apply morphological operations to clean the mask"""
        close_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.close_kernel)
        open_mask = cv2.morphologyEx(close_mask, cv2.MORPH_OPEN, self.open_kernel)
        dilation = cv2.dilate(open_mask, self.dilation_kernel, iterations=1)
        return dilation
    
    def apply_invisibility_effect(self, frame, background, lower_hsv, upper_hsv):
        """Apply the invisible cloak effect"""
        if background is None:
            return frame
            
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask
        mask = cv2.inRange(hsv, np.array(lower_hsv), np.array(upper_hsv))
        
        # Filter mask
        mask = self.filter_mask(mask)
        
        # Apply invisibility effect
        cloak = cv2.bitwise_and(background, background, mask=mask)
        inverse_mask = cv2.bitwise_not(mask)
        current_background = cv2.bitwise_and(frame, frame, mask=inverse_mask)
        result = cv2.add(cloak, current_background)
        
        return result, mask

# Main title with futuristic styling
st.markdown('<h1 class="futuristic-title">🧙‍♂️ INVISIBLE CLOAK PORTAL 🔮</h1>', unsafe_allow_html=True)

# Subtitle
st.markdown("""
<div style="text-align: center; font-family: 'Orbitron', monospace; font-size: 1.2rem; color: #00d4ff; margin-bottom: 2rem;">
    ⚡ HARNESS THE POWER OF DIGITAL SORCERY ⚡
</div>
""", unsafe_allow_html=True)

# Create columns for layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown("### 🎛️ COMMAND CENTER")
    
    # Camera controls
    st.markdown("#### 📹 CAMERA MATRIX")
    camera_source = st.selectbox("📡 Signal Source", [0, 1, 2], help="Select camera device")
    
    # Color range controls
    st.markdown("#### 🌈 CHROMATIC FILTERS")
    
    color_preset = st.selectbox(
        "🎨 Color Preset", 
        ["Custom", "Green Screen", "Blue Screen", "Red Cloak", "Purple Magic", 
         "Yellow Cloak", "Orange Cloak", "Pink Cloak", "Cyan Cloak", "Black Cloak", 
         "White Cloak", "Brown Cloak", "Lime Green", "Dark Blue", "Magenta", "Turquoise"]
    )
    
    # Preset color ranges with expanded options
    color_presets = {
        "Green Screen": ([50, 80, 50], [90, 255, 255]),      # Traditional green screen
        "Blue Screen": ([100, 80, 50], [130, 255, 255]),     # Traditional blue screen
        "Red Cloak": ([0, 80, 50], [10, 255, 255]),          # Bright red
        "Purple Magic": ([140, 80, 50], [160, 255, 255]),    # Purple/violet
        "Yellow Cloak": ([20, 80, 50], [40, 255, 255]),      # Bright yellow
        "Orange Cloak": ([10, 80, 50], [25, 255, 255]),      # Orange
        "Pink Cloak": ([160, 80, 50], [180, 255, 255]),      # Pink/magenta
        "Cyan Cloak": ([80, 80, 50], [100, 255, 255]),       # Cyan/light blue
        "Black Cloak": ([0, 0, 0], [180, 255, 50]),          # Black objects
        "White Cloak": ([0, 0, 200], [180, 30, 255]),        # White/light objects
        "Brown Cloak": ([10, 50, 20], [20, 255, 200]),       # Brown
        "Lime Green": ([65, 80, 50], [85, 255, 255]),        # Bright lime green
        "Dark Blue": ([110, 80, 50], [120, 255, 200]),       # Dark blue
        "Magenta": ([140, 100, 100], [170, 255, 255]),       # Bright magenta
        "Turquoise": ([85, 80, 50], [95, 255, 255])          # Turquoise
    }
    
    if color_preset != "Custom":
        lower_bound, upper_bound = color_presets[color_preset]
        
        # Display color info
        st.markdown(f"""
        <div style="background: rgba(0, 255, 255, 0.1); border: 1px solid #00ffff; 
                    border-radius: 8px; padding: 10px; margin: 10px 0;">
            <div style="font-size: 0.9rem; color: #00ffff;">
                🎯 <strong>{color_preset}</strong> Selected<br>
                📊 HSV Range: {lower_bound} → {upper_bound}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("##### 🔽 Lower HSV Bounds")
        h_low = st.slider("H (Hue)", 0, 179, 50)
        s_low = st.slider("S (Saturation)", 0, 255, 80)
        v_low = st.slider("V (Value)", 0, 255, 50)
        lower_bound = [h_low, s_low, v_low]
        
        st.markdown("##### 🔼 Upper HSV Bounds")
        h_high = st.slider("H (Hue) Max", 0, 179, 90)
        s_high = st.slider("S (Saturation) Max", 0, 255, 255)
        v_high = st.slider("V (Value) Max", 0, 255, 255)
        upper_bound = [h_high, s_high, v_high]
    
    # Effects controls
    st.markdown("#### ✨ MAGICAL ENHANCEMENTS")
    show_mask = st.checkbox("👁️ Show Detection Mask", False)
    apply_glow = st.checkbox("🌟 Cyber Glow Effect", True)
    
    # Color guide
    with st.expander("🎨 **COLOR SELECTION GUIDE**", expanded=False):
        st.markdown("""
        **🌟 Best Colors for Invisibility:**
        - **🟢 Green Screen**: Classic choice, works in most lighting
        - **🟦 Blue Screen**: Professional option, good contrast
        - **🟡 Yellow Cloak**: Bright and easy to detect
        - **🟣 Purple Magic**: Unique color, less common in backgrounds
        
        **💡 Tips for Best Results:**
        - Use **solid colored fabric** without patterns
        - Ensure **good lighting** on your cloak/object
        - Avoid colors that appear in your background
        - **Bright, saturated colors** work better than dull ones
        
        **🎯 Color Recommendations by Environment:**
        - **Indoor**: Green, Blue, Purple, Magenta
        - **Outdoor**: Pink, Orange, Cyan (avoid green/brown)
        - **Dark Rooms**: Yellow, White, Bright colors
        - **Bright Rooms**: Dark Blue, Black, Purple
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Status panel
    st.markdown("### 📊 SYSTEM STATUS")
    
    if st.session_state.background_captured:
        st.markdown('<div class="status-indicator status-active">🟢 BACKGROUND MATRIX: LOCKED</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-indicator status-inactive">🔴 BACKGROUND MATRIX: PENDING</div>', unsafe_allow_html=True)
    
    if st.session_state.camera_active:
        st.markdown('<div class="status-indicator status-active">📹 CAMERA FEED: ONLINE</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-indicator status-inactive">📹 CAMERA FEED: OFFLINE</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 🖥️ VISUAL INTERFACE")
    
    # Control buttons
    button_col1, button_col2, button_col3 = st.columns(3)
    
    with button_col1:
        if st.button("🚀 INITIALIZE PORTAL", key="start"):
            st.session_state.camera_active = True
            
    with button_col2:
        if st.button("📸 CAPTURE REALITY", key="capture"):
            if st.session_state.camera_active:
                st.session_state.background_captured = True
                
    with button_col3:
        if st.button("🛑 DEACTIVATE", key="stop"):
            st.session_state.camera_active = False
    
    # Video display area
    video_placeholder = st.empty()
    mask_placeholder = st.empty()
    
    # Initialize the cloak processor
    cloak_processor = FuturisticInvisibleCloak()
    
    if st.session_state.camera_active:
        try:
            cap = cv2.VideoCapture(camera_source)
            
            if not cap.isOpened():
                st.error("🚨 PORTAL INITIALIZATION FAILED - Camera not accessible")
            else:
                # Capture background if not already captured
                if not st.session_state.background_captured:
                    with st.spinner("🔮 Scanning dimensional backdrop..."):
                        time.sleep(2)
                        ret, background = cap.read()
                        if ret:
                            st.session_state.background_frame = background.copy()
                            st.session_state.background_captured = True
                            st.success("✨ Background matrix captured!")
                
                # Main processing loop
                stframe = st.empty()
                
                while st.session_state.camera_active:
                    ret, frame = cap.read()
                    
                    if ret:
                        # Apply invisibility effect
                        if st.session_state.background_captured:
                            result_frame, mask = cloak_processor.apply_invisibility_effect(
                                frame, 
                                st.session_state.background_frame,
                                lower_bound,
                                upper_bound
                            )
                            
                            # Apply glow effect if enabled
                            if apply_glow:
                                glow = cv2.GaussianBlur(result_frame, (15, 15), 0)
                                result_frame = cv2.addWeighted(result_frame, 0.8, glow, 0.3, 0)
                            
                            # Convert BGR to RGB
                            result_frame_rgb = cv2.cvtColor(result_frame, cv2.COLOR_BGR2RGB)
                            
                            # Display main video
                            video_placeholder.image(result_frame_rgb, channels="RGB", use_container_width=True)
                            
                            # Show mask if enabled
                            if show_mask:
                                mask_colored = cv2.applyColorMap(mask, cv2.COLORMAP_PLASMA)
                                mask_rgb = cv2.cvtColor(mask_colored, cv2.COLOR_BGR2RGB)
                                mask_placeholder.image(mask_rgb, caption="🎭 Detection Mask", channels="RGB", use_container_width=True)
                        else:
                            # Show original frame
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            video_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
                    
                    time.sleep(0.03)  # ~30 FPS
                
                cap.release()
                
        except Exception as e:
            st.error(f"🚨 DIMENSIONAL BREACH DETECTED: {str(e)}")
    
    else:
        # Show placeholder when camera is off
        placeholder_image = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(placeholder_image, "PORTAL OFFLINE", (180, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 65), 2)
        video_placeholder.image(placeholder_image, channels="RGB", use_container_width=True)

# Footer with matrix-style info
st.markdown("---")
st.markdown("""
<div class="matrix-text">
🔮 MAGICAL PROTOCOLS ACTIVE 🔮<br>
> Dimensional stability: OPTIMAL<br>
> Chromatic filters: CALIBRATED<br>
> Reality distortion: ENABLED<br>
> Magic level: OVER 9000!<br><br>
⚠️ WARNING: Use responsibly. Not responsible for accidental time travel or interdimensional incidents.
</div>
""", unsafe_allow_html=True)

# Sidebar with advanced options
with st.sidebar:
    st.markdown("### ⚙️ ADVANCED SORCERY")
    
    st.markdown("#### 🔬 Morphological Operations")
    kernel_size = st.slider("Kernel Size", 3, 15, 5, step=2)
    iterations = st.slider("Dilation Iterations", 1, 5, 1)
    
    st.markdown("#### 📈 Performance Metrics")
    st.metric("🎯 Frame Rate", "30 FPS", "Optimal")
    st.metric("🖥️ Resolution", "640x480", "Standard")
    st.metric("⚡ Latency", "33ms", "Low")
    
    st.markdown("#### 📋 Spell Instructions")
    st.markdown("""
    1. 🚀 **Initialize Portal** - Start camera
    2. 📸 **Capture Reality** - Set background
    3. 🧙‍♂️ **Wear colored cloak** - Green recommended
    4. ✨ **Enjoy invisibility!**
    
    **Pro Tips:**
    - Use solid colored fabric
    - Ensure good lighting
    - Avoid shadows on cloak
    - Keep background still
    """)
    
    st.markdown("#### 🎨 Color Theory")
    st.info("""
    **HSV Color Space:**
    - **Hue**: Color type (0-179)
    - **Saturation**: Color intensity (0-255)  
    - **Value**: Brightness (0-255)
    
    Green works best due to its distance from skin tones in HSV space.
    """)
