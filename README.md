# arxiv_frontend# ArXiv Similarity Search - Frontend

Professional web interface for AI-powered research paper discovery and analysis.

## Features

- **Modern UI/UX** - Clean, responsive design with dark theme
- **Dual-Mode Search** - Switch between ArXiv and Local Database modes
- **Real-time Feedback** - Live character counts, loading states, progress bars
- **Interactive Results** - View top papers with comparative analysis
- **On-Demand Summaries** - Generate detailed paper summaries
- **Session Statistics** - Track searches, papers analyzed, and more
- **Toast Notifications** - User-friendly error and success messages

## Tech Stack

- **HTML5** - Semantic markup
- **CSS3** - Custom properties, Grid, Flexbox, animations
- **Vanilla JavaScript** - No framework dependencies
- **Fetch API** - RESTful API communication

## Setup

1. **Install Backend** (if not done already)
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start Backend Server**
   ```bash
   cd backend
   python main.py
   # Server runs on http://localhost:8000
   ```

3. **Serve Frontend**
   
   **Option A: Using Python**
   ```bash
   cd frontend
   python -m http.server 3000
   # Open http://localhost:3000
   ```
   
   **Option B: Using Node.js**
   ```bash
   cd frontend
   npx serve -p 3000
   # Open http://localhost:3000
   ```
   
   **Option C: Using VS Code Live Server**
   - Install "Live Server" extension
   - Right-click `index.html` → "Open with Live Server"

## File Structure

```
frontend/
├── index.html              # Main HTML file
├── assets/
│   ├── css/
│   │   ├── main.css       # Core styles
│   │   ├── components.css # Component styles
│   │   └── animations.css # Animations
│   └── js/
│       ├── main.js        # Main application logic
│       ├── api.js         # API service
│       ├── components.js  # UI components
│       └── utils.js       # Utility functions
└── README.md
```

## Configuration

**API Endpoint**: Edit `assets/js/api.js` to change the backend URL:

```javascript
const API_BASE_URL = 'http://localhost:8000';  // Change if needed
```

## Usage

1. **Select Mode**
   - Choose between "Local Database" or "ArXiv Mode"

2. **Enter Abstract**
   - Paste your research abstract (minimum 50 characters)
   - Press "Search Papers" or Ctrl+Enter

3. **View Results**
   - Browse top 5 similar papers
   - Read comparative analysis

4. **Generate Summaries**
   - Click "View Summary" on any paper
   - Wait 30-60 seconds for detailed summary

5. **New Search**
   - Click "New Search" to start over

## Keyboard Shortcuts

- `Ctrl + Enter` - Submit search
- `Esc` - Close modals

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance

- **Initial Load**: < 1s
- **Search**: 10-25s (Local), 50-90s (ArXiv)
- **Summary Generation**: 30-60s per paper

## Troubleshooting

**Backend Not Responding**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`

**Slow Searches**
- First local search builds index (60-90s)
- Subsequent searches use cached index (10-16s)

**Summary Not Loading**
- Summary generation takes 30-60 seconds
- Check backend logs for errors

## Development

**Hot Reload**: Use Live Server or similar tool for automatic reloads during development.

**Debugging**: Open browser DevTools (F12) and check:
- Console for JavaScript errors
- Network tab for API calls
- Application tab for storage

## License

MIT License - See LICENSE file for details