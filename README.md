# NBA Shot Chart Visualizer 🏀

An interactive web application for visualizing and comparing NBA player shooting performance across different seasons. Built with Flask, Plotly, and the official NBA API. Enhanced with AI-powered analysis using Google Gemini.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Flask](https://img.shields.io/badge/flask-latest-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Update #1 - AI Analysis & Enhanced Features ✨

### What's New
- 🤖 **AI-Powered Performance Analysis** - Get intelligent insights from Google Gemini 2.5 Pro
  - Comprehensive individual player analysis with strengths, weaknesses, and key insights
  - Concise head-to-head player comparisons with clear verdicts
  - Markdown-formatted reports with proper styling
    
 <img width="1841" height="652" alt="image" src="https://github.com/user-attachments/assets/96f9a8a8-97ac-4eff-badc-e19b9b344405" />

  
- 📅 **Modern Era Focus** - Data filtered to 2000 onwards
  - Season selection limited to 2000-present for better data quality
  - Clear disclaimers on season dropdowns
  - Validation to prevent pre-2000 season selection
  
- 📊 **Enhanced Visualizations**
  - Improved Chart.js comparison charts with better formatting
  - Clean, readable AI analysis sections with white text on gradient backgrounds
  - Removed duplicate content for streamlined user experience
  
- 🎨 **UI/UX Improvements**
  - Professional gradient backgrounds for AI analysis sections
  - Properly formatted Markdown rendering (headings, lists, bold/italic text)
  - Responsive design enhancements across all pages

## Features

### 🤖 AI-Powered Analysis (NEW!)
- **Individual Player Analysis**: Deep dive into a player's shooting performance with AI-generated insights
  - Overall shooting efficiency assessment vs league average
  - Top 2 shooting strengths and main weakness identification
  - Key insights about playing style and shot selection
  - Concise 100-150 word summaries powered by Gemini 2.0 Flash

- **Comparative Analysis**: Intelligent player-vs-player analysis
  - Clear verdict on which player performed better
  - Specific reasoning backed by percentages and statistics
  - Notable differences in shooting styles
  - Comprehensive yet concise 100-150 word comparisons

### 📊 Individual Shot Charts
- Interactive Plotly visualizations showing every shot attempt
- Made shots (green circles) and missed shots (red X's)
- Detailed zone-by-zone shooting statistics
- Comparison with league average performance (2000+ seasons only)
- Hover tooltips with shot distance and type

### 🔄 Player Comparison
- Side-by-side shot chart comparisons
- Compare any two players across different seasons (2000 onwards)
- Zone-by-zone statistical breakdown
- Visual bar chart showing FG% differences
- Color-coded table highlighting better performance
- AI-powered comparison analysis with clear verdicts

### 🎯 Smart Features
- Autocomplete player search
- Dynamic season selection based on player career (2000+ only)
- Real-time data from official NBA API
- Responsive design with Pico CSS
- Interactive charts (zoom, pan, hover)
- Markdown-formatted AI reports with proper styling

## Screenshots
<img width="1846" height="966" alt="image" src="https://github.com/user-attachments/assets/a4f051f9-ad16-473a-848a-7e9e0c26ccf1" />

<img width="1545" height="1027" alt="image" src="https://github.com/user-attachments/assets/2177d8d8-956c-4860-96e8-cb274aa35a79" />

<img width="1526" height="1022" alt="image" src="https://github.com/user-attachments/assets/717e7408-7bc9-42e2-a927-7ef0e6f4c2fd" />

<img width="1457" height="1025" alt="image" src="https://github.com/user-attachments/assets/d640ec03-ef29-4f18-8806-9b55b614e8b8" />





## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/ankit-tumu/NBA_Visualize.git
cd NBA_Visualize
```

2. **Create a virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```
To get a Gemini API key:
- Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
- Sign in with your Google account
- Click "Create API Key"
- Copy and paste into your `.env` file

5. **Run the application**
```bash
python run.py
```

6. **Open your browser**
Navigate to `http://localhost:8080`

## Usage

### Generate a Shot Chart

1. Start typing a player's name in the search box
2. Select from the autocomplete suggestions
3. Choose a season from the dropdown (2000 onwards only)
4. Click "Generate Chart"
5. View the interactive shot chart, statistics, and AI-powered analysis

### Compare Two Players

1. Click "Compare Two Players" from the home page
2. Select Player 1 and their season (2000+ only)
3. Select Player 2 and their season (2000+ only)
4. Click "Compare Players"
5. Analyze side-by-side charts, statistics, and AI comparative analysis

### Example Searches

Try these interesting comparisons:
- **Stephen Curry vs Damian Lillard** (2021-22) - Three-point snipers
- **LeBron James vs Kevin Durant** (2022-23) - All-around scorers
- **Joel Embiid vs Nikola Jokić** (2022-23) - Modern elite centers
- **Kobe Bryant 2005-06 vs Michael Jordan 2002-03** - Legends comparison (modern seasons only)

## Project Structure

```
NBA_Visualize/
├── NBA_Shot_Charts/
│   ├── __init__.py           # Flask app factory
│   ├── routes.py             # URL routes and endpoints
│   ├── data.py               # NBA API data fetching (2000+ filter)
│   ├── plotting.py           # Plotly chart generation
│   ├── ai_analysis.py        # Gemini AI analysis (NEW!)
│   └── templates/
│       ├── base.html         # Base template with AI styling
│       ├── index.html        # Home/search page
│       ├── result.html       # Individual shot chart + AI analysis
│       ├── comparison.html   # Comparison form
│       └── comparison_result.html  # Comparison results + AI
├── .env                      # Environment variables (Gemini API key)
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore rules
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
└── README.md                 # This file
```

## API Endpoints

### Web Routes
- `GET /` - Home page with player search
- `POST /result` - Generate individual shot chart
- `GET /compare` - Player comparison form
- `POST /comparison-result` - Generate comparison charts

### API Endpoints
- `GET /api/players` - List all NBA players
- `GET /api/player/<player_id>/seasons` - Get player's seasons
- `GET /api/player-comparison/<player_id>/<season_id>` - Get comparison data

## Technologies Used

### Backend
- **Flask** - Web framework
- **nba_api** - Official NBA stats API wrapper
- **pandas** - Data manipulation and analysis
- **python-dotenv** - Environment variable management
- **google-generativeai** - Google Gemini AI integration (NEW!)
- **markdown** - Markdown to HTML conversion for AI reports (NEW!)

### Frontend
- **Plotly** - Interactive shot chart visualizations
- **Chart.js** - Comparison bar charts
- **Pico CSS** - Minimal, semantic CSS framework
- **Vanilla JavaScript** - Dynamic UI interactions

### AI & Analytics
- **Google Gemini 2.0 Flash** - AI-powered performance analysis
- **Markdown rendering** - Professional formatting for AI insights

## Data Source

All data is sourced from the official NBA Stats API via the `nba_api` Python library. AI analysis is powered by Google Gemini 2.0 Flash. This includes:
- Player information and career history
- Shot location data (X, Y coordinates)
- Shot outcomes (made/missed)
- Shot types and distances
- League average statistics
- **Data Restriction**: Only seasons from 2000 onwards are available for analysis

## Performance Notes

- Player list is cached on application startup to minimize API calls
- Shot data is fetched on-demand (typically takes 3-5 seconds)
- AI analysis generation takes 2-4 seconds per request
- Charts are generated client-side for smooth interactions
- Season data is filtered to 2000+ for better data quality and performance
- Consider implementing Redis/Flask-Caching for production deployments

## Known Limitations

- Only includes Regular Season data
- **Data limited to 2000-present seasons** for consistency and quality
- API rate limits may affect heavy usage
- Some historical players may have incomplete data
- Court dimensions are standardized (doesn't account for historical changes)
- AI analysis requires valid Gemini API key
- AI responses may occasionally be unavailable due to API limits

## Future Enhancements

- [ ] Add playoff data support
- [ ] Implement shot heatmaps
- [ ] Add filtering by shot type (2PT, 3PT, etc.)
- [ ] Multi-season player comparisons
- [ ] Export charts as PNG/PDF
- [ ] Add caching for improved performance
- [ ] Mobile app version
- [ ] Team-level shot chart aggregations
- [ ] Historical data expansion (pre-2000 seasons)
- [ ] More AI analysis features (trend analysis, predictions)
- [ ] User accounts to save favorite comparisons

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NBA Stats API for providing comprehensive basketball data
- The `nba_api` library maintainers
- Plotly for excellent visualization tools
- Google Gemini AI for intelligent analysis capabilities
- The Python and Flask communities

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Environment Variables

Required environment variables in `.env`:
```
GEMINI_API_KEY=your_api_key_here
```

## Author

Ankit Tumuluri - https://www.linkedin.com/in/ankit-tumuluri/

Created with ❤️ for basketball analytics enthusiasts

---

**Note**: This application is for educational and analytical purposes only. It is not affiliated with or endorsed by the NBA.
