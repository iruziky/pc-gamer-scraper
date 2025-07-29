# PC Gamer Scraper

This project is a web scraper developed in Python to monitor and collect prices of computer components (CPU, GPU, Motherboard, etc.) from major Brazilian e-commerce sites, such as Kabum!, Pichau, and TerabyteShop.

## ✨ Core Features

- **Multiple Sources**: Collects data from over 10 major online retailers.
- **Efficient Scraping**: Uses `requests` for lightweight and fast collection, focusing on search pages to minimize server load and costs.
- **Dual-Frequency Strategy**:
    - Scans the first few pages every 5 minutes to capture sales and "hot" items.
    - Performs a full daily scan across all categories of interest.
- **Data Validation**: Employs `Selenium` in a daily test to ensure the integrity of the data collected via `requests`.
- **Modular Architecture**: Designed with Object-Oriented principles for easy maintenance and expansion.

## 🚀 Getting Started

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/iruziky/pc-gamer-scraper.git](https://github.com/iruziky/pc-gamer-scraper.git)
    cd pc-gamer-scraper
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    - Rename the `.env.example` file to `.env`.
    - Fill in the necessary configurations.

## 🛠️ Tech Stack

- **Language**: Python 3
- **Scraping**:
    - `requests`
    - `BeautifulSoup4`
- **Integrity Tests**:
    - `Selenium`
    - `undetected-chromedriver`
- **Framework**: Planned to use a web framework (Flask/Django) and a queue system (Celery/RQ).