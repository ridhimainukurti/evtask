# Ev Community Portal

A Reddit-style community platform for electriv vehical enthusiats. This is a web application built with Flask and HTML/CSS/JS and a mobile demo using React Native. 

## Table of Contents
- [Web Portal](#web-portal)
    - [Setup & Run](#setup--run)
- [Mobile App (React Native)](#mobile-app-react-native)
    - [Setup & Run](#setup--run-1)
- [Demo Accounts](#demo-accounts)

--- 
## Web Portal 

### Setup & Run 

**Prerequisites:**
- Python 3.7+
- `pip` (Python package manager)
- *(Recommend)* [Virtualenv](https://docs.python.org/3/library/venv.html)

**Instructions:**
1. **Clone the repository and go to the web-portal folder:**

```bash 
git clone https://github.com/ridhimainukurti/evtask.git
cd evtask/web-portal
```
2. **Set up a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```
3. **Install dependencies:**

```bash
pip install Flask
```
4. **Run Flask:**

```bash
python3 app.py
```
The web app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000)
Visit the link in order to access the website. 

--- 
## Mobile App (React Native)

### Setup & Run 

**Prerequisites:**
- Node.js
- [Expo cli](https://docs.expo.dev/get-started/installation/)
- Android/iOS device for testing 

**Instructions:**

1. **Go to mobile-app folder:**

```bash
cd mobile-app
```
2. **Install dependencies:**

```bash
npm install
```
3. **Start app:**

```bash
expo start
```
Open the app in expo go app (scan the qr code)

---

### Demo Account
| Username | Password | Role    |
|----------|----------|---------|
| admin    | admin    | Admin   |

This account grants access to the admin dashboard feature. 

---
