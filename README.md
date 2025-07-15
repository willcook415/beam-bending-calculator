# Beam Bending Calculator

An interactive Python app that calculates and visualizes shear force and bending moment diagrams for **simply supported beams** with **point loads**. Built using [Streamlit](https://streamlit.io/) as a personal engineering tool and portfolio project.

> Developed by William Cook (@willcook415) – Mechanical Engineering student at the University of Leeds

---

## Features

- Input beam length and point load parameters
- Calculate reaction forces at supports
- Generate:
  - Shear Force Diagram (SFD)
  - Bending Moment Diagram (BMD)
- Visualize results instantly
- Simple, responsive UI with Streamlit

---

## How It Works

The app uses static equilibrium principles to calculate:
- Reaction forces at supports using ∑F = 0 and ∑M = 0
- Shear force values at each segment of the beam
- Bending moment values based on load positions

---

## Getting Started

### 1. Clone the repo
"```bash
git clone https://github.com/willcook415/beam-bending-calculator.git
cd beam-bending-calculator"

### 2. Install dependencies
"pip install -r requirements.txt"

### 3. Run the app
"streamlit run app.py"

---

## Built With

- Python
- Streamlit
- NumPy
- Matplotlib

---

## Preview

---

## License

This project is open source under the MIT license.

---

## Author

William Cook
GitHub: @willcook415
LinkedIn: https://www.linkedin.com/in/william-g-cook/
