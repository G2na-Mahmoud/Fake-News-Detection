# 📰 Fake News Detection System (Web Application)

## 📌 Project Overview

The **Fake News Detection System** is a web-based application developed using **Python and Flask**. It allows users to verify the credibility of news articles by entering the news text into a website.

The system works by analyzing the user-provided news content, searching for related information online, validating it against the given data, and then returning a final decision indicating whether the news is **Real** or **Fake**.

---

## 🎯 Project Objectives

* Detect and reduce the spread of fake news
* Provide an easy-to-use web interface for news verification
* Apply rule-based logic instead of complex ML models
* Verify news credibility using online sources

---

## 💡 Project Idea

With the massive growth of online news and social media platforms, misinformation has become a major issue. This project aims to help users check the authenticity of news articles by combining **rule-based analysis** with **online search verification**.

---

## 🛠️ Technologies Used

* **Programming Language:** Python
* **Framework:** Flask
* **Frontend:** HTML, CSS
* **Verification Method:**

  * Rule-Based Detection
  * Google Search Verification

---

## ⚙️ System Workflow

1. User enters the news text on the website
2. Flask application receives the input
3. Rule-based logic analyzes the news content
4. The system searches online (Google) for related information
5. Results are compared with the provided data
6. Final result is displayed to the user (Real or Fake)

---

## 📂 Project Structure

```
Fake-News-Detection/
│── app.py              # Main Flask application file
│── config.py           # Application configuration
│── rule_detector.py    # Rule-based fake news detection logic
│── google_checker.py   # Online news verification module
│── templates/          # HTML templates
│   ├── index.html      # Home page
│   ├── login.html      # Login page
│   ├── history.html    # Search history page
│── static/
│   ├── style.css       # Website styling
│── README.md
```

---

## 🚀 How to Run the Project

1. Clone the repository:

```bash
git clone https://github.com/AhmedFarh5/Fake-News-Detection.git
```

2. Navigate to the project directory:

```bash
cd Fake-News-Detection
```

3. Install required dependencies:

```bash
pip install flask
```

4. Run the application:

```bash
python app.py
```

5. Open your browser and go to:

```
http://127.0.0.1:5000
```

---

## ✅ Output

* The system displays a clear result:

  * ✅ Real News
  * ❌ Fake News
* The result is based on rule-based analysis and online verification

---

## 🔮 Future Improvements

* Integrate Machine Learning models
* Improve accuracy of verification
* Add Arabic language support
* Use trusted news APIs


---

## 📜 License

This project is open-source and intended for educational purposes.
