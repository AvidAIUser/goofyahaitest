# CoolBlock AI - Setup Instructions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repo)

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/AvidAIUser/goofyahaitest.git
cd goofyahaitest
```

2. **Create virtual environment**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
streamlit run app.py
```

5. **Open in browser**
- The app should automatically open at `http://localhost:8501`
- If not, navigate to that URL manually

### Usage

1. **Enter your location**
   - Type an address (e.g., "123 Main St, New York, NY")
   - Or use coordinates (latitude/longitude)

2. **View your heat safety map**
   - See current temperature, humidity, heat index
   - View color-coded risk zones
   - Find nearby cooling centers

3. **Report issues**
   - If a cooling center is closed or incorrect, report it
   - Your feedback helps the community

## 📦 What's Included

- `app.py` - Main Streamlit application
- `model.py` - AI model definition and utilities
- `utils.py` - Helper functions for weather and data
- `requirements.txt` - Python dependencies
- `README.md` - Full documentation
- Supporting documentation files

## 🌐 Deploy to Streamlit Cloud (Free)

1. **Push to GitHub**
```bash
git add .
git commit -m "CoolBlock AI - Ready for deployment"
git push origin main
```

2. **Go to Streamlit Cloud**
- Visit https://streamlit.io/cloud
- Sign in with GitHub
- Click "New app"
- Select your repo and `app.py`
- Deploy!

3. **Share your app**
- Get a public URL
- Share with your team
- Gather feedback

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'streamlit'`
**Solution**: Make sure you activated your virtual environment and installed requirements
```bash
pip install -r requirements.txt
```

### Issue: Port 8501 already in use
**Solution**: Run on a different port
```bash
streamlit run app.py --server.port 8502
```

### Issue: API connection errors
**Solution**: Check your internet connection. The app uses Open-Meteo API (free, no key needed)

### Issue: Slow performance on map
**Solution**: This is normal on first load. Refresh the page.

## 📝 Development Tips

### Adding Features
1. Edit `app.py` for UI changes
2. Edit `model.py` for AI model changes
3. Edit `utils.py` for data processing changes
4. Run `streamlit run app.py` to test

### Testing the Shade Detection
```python
from model import create_shade_detection_model, predict_shade_score
import numpy as np

# Create dummy image
dummy_image = np.random.rand(224, 224, 3) * 255

# Predict shade
shade_score, confidence = predict_shade_score(dummy_image)
print(f"Shade: {shade_score:.1f}%, Confidence: {confidence:.1f}%")
```

### Testing Weather API
```python
from utils import get_weather_data, calculate_heat_index

# Get weather
weather = get_weather_data(40.7128, -74.0060)  # New York
print(f"Temperature: {weather['temperature']}°F")

# Calculate heat index
hi = calculate_heat_index(weather['temperature'], weather['humidity'])
print(f"Heat Index: {hi}°F")
```

## 📊 Next Steps

1. **Collect street view images** (500+) for training
2. **Train the AI model** in Google Colab
3. **Integrate trained model** into the app
4. **Deploy to Streamlit Cloud**
5. **Record 3-5 minute pitch video**
6. **Submit on Devpost** by June 21, 11:59 PM ET

## 🎯 Important Dates

- **June 14, 10:00 AM ET**: Hackathon Kickoff
- **June 14-21**: Build period
- **June 21, 11:59 PM ET**: Submission deadline
- **June 27, 10:00 AM ET**: Awards ceremony

## 📞 Need Help?

- Check the `README.md` for full documentation
- Visit Discord: https://discord.gg/ePjenJnyh4
- Email: aihackathon@usaii.org

---

**❄️ Stay cool. Stay safe. Check on your neighbors. ❄️**
