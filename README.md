# NBA Shot Chart Visualizer 🏀

An interactive web application for visualizing and comparing NBA player shooting performance across different seasons. Built with Flask, Plotly, and the official NBA API.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Flask](https://img.shields.io/badge/flask-latest-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

### 📊 Individual Shot Charts
- Interactive Plotly visualizations showing every shot attempt
- Made shots (green circles) and missed shots (red X's)
- Detailed zone-by-zone shooting statistics
- Comparison with league average performance
- Hover tooltips with shot distance and type

### 🔄 Player Comparison
- Side-by-side shot chart comparisons
- Compare any two players across different seasons
- Zone-by-zone statistical breakdown
- Visual bar chart showing FG% differences
- Color-coded table highlighting better performance

### 🎯 Smart Features
- Autocomplete player search
- Dynamic season selection based on player career
- Real-time data from official NBA API
- Responsive design with Pico CSS
- Interactive charts (zoom, pan, hover)

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
cd nba-shot-charts
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

4. **Run the application**
```bash
python run.py
```

5. **Open your browser**
Navigate to `http://localhost:8080`

## Usage

### Generate a Shot Chart

1. Start typing a player's name in the search box
2. Select from the autocomplete suggestions
3. Choose a season from the dropdown
4. Click "Generate Chart"
5. View the interactive shot chart and statistics

### Compare Two Players

1. Click "Compare Two Players" from the home page
2. Select Player 1 and their season
3. Select Player 2 and their season
4. Click "Compare Players"
5. Analyze side-by-side charts and statistics

### Example Searches

Try these interesting comparisons:
- **Stephen Curry vs Damian Lillard** (2021-22) - Three-point snipers
- **LeBron James vs Kevin Durant** (2022-23) - All-around scorers
- **Joel Embiid vs Nikola Jokić** (2022-23) - Modern elite centers
- **Kobe Bryant vs Michael Jordan** - Legends comparison

## Project Structure

```
nba-shot-charts/
├── NBA_Shot_Charts/
│   ├── __init__.py           # Flask app factory
│   ├── routes.py             # URL routes and endpoints
│   ├── data.py               # NBA API data fetching
│   ├── plotting.py           # Plotly chart generation
│   └── templates/
│       ├── base.html         # Base template
│       ├── index.html        # Home/search page
│       ├── result.html       # Individual shot chart
│       ├── comparison.html   # Comparison form
│       └── comparison_result.html  # Comparison results
├── .env                      # Environment variables
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

### Frontend
- **Plotly** - Interactive shot chart visualizations
- **Chart.js** - Comparison bar charts
- **Pico CSS** - Minimal, semantic CSS framework
- **Vanilla JavaScript** - Dynamic UI interactions

## Data Source

All data is sourced from the official NBA Stats API via the `nba_api` Python library. This includes:
- Player information and career history
- Shot location data (X, Y coordinates)
- Shot outcomes (made/missed)
- Shot types and distances
- League average statistics

## Performance Notes

- Player list is cached on application startup to minimize API calls
- Shot data is fetched on-demand (typically takes 3-5 seconds)
- Charts are generated client-side for smooth interactions
- Consider implementing Redis/Flask-Caching for production deployments

## Known Limitations

- Only includes Regular Season data
- API rate limits may affect heavy usage
- Some historical players may have incomplete data
- Court dimensions are standardized (doesn't account for historical changes)

## Future Enhancements

- [ ] Add playoff data support
- [ ] Implement shot heatmaps
- [ ] Add filtering by shot type (2PT, 3PT, etc.)
- [ ] Multi-season player comparisons
- [ ] Export charts as PNG/PDF
- [ ] Add caching for improved performance
- [ ] Mobile app version
- [ ] Team-level shot chart aggregations

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
- The Python and Flask communities

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Author

Ankit Tumuluri - https://www.linkedin.com/in/ankit-tumuluri/

Created with ❤️ for basketball analytics enthusiasts

---

**Note**: This application is for educational and analytical purposes only. It is not affiliated with or endorsed by the NBA.
