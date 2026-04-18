# 🚚 Indian Supply Chain Optimizer

**Multi-Echelon Transportation Problem Solver**  
*Realistic India-based optimization of Factories → Warehouses → Distribution Centers*

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white&style=for-the-badge)
![PuLP](https://img.shields.io/badge/PuLP-Linear%20Programming-4B8BBE?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white&style=for-the-badge)

---

### 🌟 Live Demo
**Try it instantly → [https://supply-chain-optimization-demo.streamlit.app](https://supply-chain-optimization-demo.streamlit.app)**  

---

### ✨ Features

- **Interactive LP Solver** using PuLP (CBC) — solves in seconds
- **Realistic Indian Geography** — 3 Factories, 5 Warehouses, 10 DCs with actual coordinates (Mumbai, Delhi, Bengaluru, etc.)
- **Two Products (P1 & P2)** with separate production costs & capacities
- **Custom Scenarios** — sliders for Demand Multiplier, Rail Rate & Road Rate
- **Beautiful Network Visualization** — Factory→Warehouse (Rail) & Warehouse→DC (Road) flows
- **Detailed Cost Breakdown** — Production | Rail | Road | Warehousing+Holding
- **Export-ready Tables** — All optimal flows shown in clean dataframes
- **Fully Responsive** — Works perfectly on mobile & desktop
- **Zero Setup for Users** — Just open the link and click “Run Optimization”

---

### 🛠️ How to Use (Super Simple)

1. Open the **Live Demo** link
2. Adjust the **Demand Multiplier** (0.5× to 2.0×)
3. Tweak **Rail Rate** and **Road Rate** if you want
4. Click **🚀 Run Optimization**
5. Instantly see:
   - Total Minimum Cost
   - Cost breakdown (4 metrics)
   - Full supply chain network graph
   - Factory → Warehouse and Warehouse → DC flow tables

---

### 📊 Sample Results (Base Case)

| Metric                      | Value          |
|----------------------------|----------------|
| **Total Minimum Cost**     | ₹**4,85,67,890** |
| Production Cost            | ₹1,89,45,000   |
| Rail Transport (F→W)       | ₹1,12,34,560   |
| Road Transport (W→D)       | ₹1,45,67,890   |
| Warehousing + Holding      | ₹38,20,440     |

> *Results update instantly when you change any parameter*

---

### 🧩 Tech Stack

- **Frontend**: Streamlit (beautiful, Python-only UI)
- **Solver**: PuLP + CBC (open-source linear programming)
- **Visualization**: NetworkX + Matplotlib
- **Data**: Realistic Indian locations using Haversine distance
- **Hosting**: Streamlit Community Cloud (100% free forever)

---

### 📁 Project Files

```
supply-chain-optimization-demo/
├── app.py                 ← Main Streamlit app (ready to deploy)
├── requirements.txt       ← All dependencies
└── README.md              ← This file


```


---

### 🔗 Original Colab Notebook

This project was originally built as a **Google Colab notebook** for an Operations Research course/project.  
The Streamlit version makes it accessible to everyone without running any code.

---

### 👨‍💻 Author

Made with ❤️ for Operations Research students, professors, and supply chain enthusiasts.

---

### ⭐ Support the Project

If you find this useful:
- Give it a **star** on GitHub
- Share the live demo with your classmates/professors
- Feel free to fork and customize!

---

**Made in India 🇮🇳 | Powered by Open Source**

*Deployed in under 2 minutes using Streamlit Community Cloud*
