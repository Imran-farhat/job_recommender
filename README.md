# 🎯 Smart Job Matcher

A sophisticated job recommendation system that intelligently matches candidates with job opportunities using advanced algorithms and flexible JSON input formats.

## ✨ Features

### 🧠 Smart Format Converter
- **Accepts ANY JSON format** - Job postings, candidate profiles, simple formats
- **Auto-detects input type** and converts to standard format
- **Intelligent skill extraction** from text descriptions
- **Flexible salary parsing** (supports various formats)

### 🎯 Advanced Matching Algorithm
- **Fuzzy matching** for skills, titles, and locations
- **Weighted scoring system** with detailed breakdowns
- **Remote work optimization** 
- **Multi-criteria evaluation** (skills, location, salary, values, etc.)

### 🎨 Modern UI/UX
- **Beautiful gradient design** with professional styling
- **Interactive example buttons** for quick testing
- **Responsive mobile-friendly** interface
- **Real-time form validation** and error handling
- **Animated results** with smooth transitions

### 🌍 Global Job Database
- **55+ realistic job postings** from major companies
- **Multiple industries** - Tech, Finance, Healthcare, etc.
- **Various experience levels** - Entry to Expert
- **International locations** - US, India, Europe

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Flask framework

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/job_recommender.git
   cd job_recommender
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://127.0.0.1:5000
   ```

## 📖 Usage

### 1. Standard Candidate Preferences Format

```json
{
  "values": ["Innovation & Creativity", "Remote Work Flexibility"],
  "role_types": ["Full-Time"],
  "titles": ["Software Engineer", "Frontend Developer"],
  "locations": ["Remote", "San Francisco"],
  "role_level": ["Mid-Level (3 to 5 years)"],
  "leadership_preference": "Individual Contributor",
  "company_size": ["51-200 Employees", "201-500 Employees"],
  "industries": ["Technology", "SaaS"],
  "skills": ["JavaScript", "React", "Python", "AWS"],
  "min_salary": 120000
}
```

### 2. Job Posting Format (Auto-Converted)

```json
{
  "jobTitle": "Software Engineer",
  "company": {
    "name": "Tech Innovators Inc.",
    "location": "Chennai, Tamil Nadu, India"
  },
  "requirements": {
    "skills": ["JavaScript", "Python", "React"]
  },
  "salary": {
    "range": "600000-1200000 per annum"
  },
  "employmentType": "Full-time"
}
```

### 3. Simple Profile Format (Auto-Converted)

```json
{
  "skills": ["Python", "Django", "AWS"],
  "experience": "3 years",
  "location": "Remote",
  "expectedSalary": 100000
}
```

### 4. Quick Examples Available
- 💻 **Tech Developer** - Software engineering roles
- 🎨 **UX Designer** - Design and user experience roles  
- 📈 **Marketing Pro** - Digital marketing positions
- 📊 **Data Scientist** - Analytics and ML roles
- 💼 **Sales Executive** - Business development roles

## 🏗️ Project Structure

```
job_recommender/
├── app.py                 # Main Flask application
├── matcher.py            # Job matching algorithm
├── format_converter.py   # Smart JSON format converter
├── data/
│   └── jobs.json         # Job database (55+ positions)
├── static/
│   └── styles.css        # Modern UI styling
├── templates/
│   ├── index.html        # Main input form
│   └── results.html      # Results display
└── README.md            # This file
```

## 🔧 Technical Details

### Matching Algorithm Weights
- **Skills**: 25% - Technical and soft skills matching
- **Title/Role**: 25% - Job title and employment type
- **Location**: 15% - Geographic preferences
- **Industry**: 10% - Sector alignment
- **Company Size**: 10% - Organization size preference
- **Values**: 10% - Work culture and values
- **Salary**: 5% - Compensation requirements

### Smart Converter Features
- **Format Detection**: Automatically identifies input format type
- **Skill Extraction**: Finds technical skills from text descriptions
- **Salary Parsing**: Handles various salary formats (₹6L, $100k, etc.)
- **Location Mapping**: Extracts locations from nested objects
- **Error Handling**: Provides helpful error messages

## 🌟 Example Results

When you submit preferences, you'll see results like:

```
🎉 Your Perfect Job Matches

Software Engineer at Meta
⭐ 85.3% Match
📊 View Detailed Breakdown
• skills: 90.0%
• title_role: 85.0%
• location: 100.0%
• industry: 80.0%
• company_size: 75.0%
• values: 70.0%
• salary: 100.0%
```

## 🗃️ Database Schema

### Job Entry Format
```json
{
  "job_id": "TEC-001",
  "title": "Software Engineer",
  "company": "Meta",
  "location": "Remote",
  "salary_range": [130000, 180000],
  "employment_type": "Full-Time",
  "company_size": "1000+ Employees",
  "industry": "Technology",
  "required_skills": ["JavaScript", "React", "Node.js"],
  "values_promoted": ["Innovation & Creativity", "Learning & Growth"],
  "experience_required": "3-5 years",
  "role_level": "Mid-Level"
}
```

## 🎨 UI Features

### Interactive Elements
- **Quick-load buttons** for common job profiles
- **Auto-resizing textarea** that adapts to content
- **Real-time JSON validation** with error highlighting
- **Responsive design** that works on all devices

### Visual Design
- **Modern gradient backgrounds** with professional colors
- **Card-based layouts** with elegant shadows
- **Smooth animations** and hover effects
- **Color-coded match scores** (green=excellent, blue=good, etc.)

## 🔌 API Endpoints

### POST /recommend
Submit candidate preferences and get job matches
- **Input**: Form data with JSON preferences
- **Output**: HTML results page

### POST /api/recommend  
API endpoint for programmatic access
- **Input**: JSON payload
- **Output**: JSON response with matches

```bash
curl -X POST http://127.0.0.1:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"skills": ["Python", "Django"], "location": "Remote"}'
```

## 🚧 Future Enhancements

- [ ] **Machine Learning Integration** - Improve matching with ML models
- [ ] **User Accounts** - Save preferences and match history
- [ ] **Real-time Job Data** - Integration with job APIs
- [ ] **Advanced Filters** - More granular search options
- [ ] **Email Notifications** - Alert users of new matches
- [ ] **Resume Upload** - Extract preferences from PDF resumes
- [ ] **Company Reviews** - Integration with company rating data

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

## 🐛 Troubleshooting

### Common Issues

**App won't start:**
```bash
# Check Python version
python --version

# Install Flask if missing
pip install flask

# Run with explicit path
python app.py
```

**JSON Format Errors:**
- Use the **Smart Converter** - it handles most formats automatically
- Check for missing commas, quotes, or brackets
- Try the example buttons for valid formats

**No job matches:**
- Lower your minimum salary requirement
- Add more location options (including "Remote")
- Use broader skill terms (e.g., "JavaScript" instead of "JS")

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name** - [GitHub Profile](https://github.com/your-username)

## 🙏 Acknowledgments

- **Flask** - Web framework
- **Modern CSS** - UI/UX inspiration  
- **Job Market Research** - Realistic salary and skill data

---

## 🎯 Ready to Find Your Perfect Job?

1. **Start the app**: `python app.py`
2. **Open browser**: `http://127.0.0.1:5000`
3. **Enter your preferences** in ANY JSON format
4. **Discover amazing opportunities!** 🚀

*Built with ❤️ for job seekers everywhere*