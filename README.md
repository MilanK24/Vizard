
# Vizard

Vizard is an intelligent tool designed to analyze CSV files and provide comprehensive insights through a chatbot interface. This project integrates Gemini and Pandas AI for interactive and intuitive data exploration. Key features include:

* Automated Summary: Quickly generate a descriptive summary of your dataset.
* Graphical Visualizations: Create custom graphs to represent data visually.
* CSV Operations: Perform operations like filtering, grouping, and aggregations to extract meaningful information.
* Chatbot Interaction: Ask questions about your data and receive detailed, actionable insights.
This project enables users to understand and manipulate datasets effortlessly, making data exploration efficient and user-friendly.

**TechStack** 

[![My Skills](https://skillicons.dev/icons?i=docker,py,vscode,windows)](https://skillicons.dev)


## Table of Contents

1. [Demo](#demo)
2. [Project Structure](#project-structure)
2. [Technology Used](#technology-used)
4. [Getting Started](#getting-started)
    1. [Prerequisites](#prerequisites)
    2. [Using CMD (Command Line)](#using-cmd-command-line)
    3. [Using Docker](#using-docker)
5. [Meet the Team](#meet-the-team)
6. [Benefits](#benefits)
7. [License](#license)

## Demo
Watch Video Here

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/8i9jTCctU3U/0.jpg)](https://www.youtube.com/watch?v=8i9jTCctU3U)


## Project Structure
The project is divided into the following components:

1. Frontend: Built using Streamlit for an intuitive user interface.
2. Backend: Developed in Python for data processing and chatbot interactions.
3. Data Operations: Powered by Pandas AI and Gemini for intelligent analysis.
4. Visualization: Utilizes libraries like Matplotlib and Seaborn for graph generation.
5. Unit Testing: Ensures the reliability and correctness of functionalities.

## Technology Used
**Programming & Scripting Languages:**
- **Python**: For backend processing, model training, and feature extraction.

**Frameworks & Libraries:**
- **Streamlit**: Frontend framework for building user interfaces.

**API:**
- **Gemini**: It provides the API key for advancing the results

- **Pandas AI**: It provides the agent as a back-up for gemini
    

## Getting Started

**Prerequisites**

Before getting started, make sure you have the following installed and set up:

**1. Python**

Installing Python and Setting Up PATH on Windows
- Visit the [official Python download page](https://www.python.org/downloads/) and download the latest version for Windows.

- **Important**: Ensure the **"Add Python to PATH"** option is checked and click **"Install Now"**
- Open Command Prompt (`Win + R`, type `cmd`) and check Python version:  
```bash
python --version
  ```

**2. Git (Optional)**

Ensure that **Git** is installed and that you are logged in to GitHub.

Check if Git is installed:
```bash
git --version
```

If Git is not installed, download and install it from the official Git website:

- Download Git: [git-scm](https://git-scm.com/downloads)
Git Documentation:
- Git Docs: [git-scm.com/doc](https://git-scm.com/doc)


**3. Docker (Optional)**

Ensure that Docker is installed on your machine if you plan to use Docker for running the project.

Check if Docker is installed:
```bash
docker --version
```

If Docker is not installed, download and install it from the official Docker website:

- Download Docker: 
[www.docker.com/docker-desktop](https://www.docker.com/products/docker-desktop)
Docker Documentation:
- Docker Docs: [docs.docker](https://docs.docker.com/)

---
**Running the Project**

**1. Using CMD (Command Line)**

First, clone the frontend and backend repositories using the following commands:

```bash
git clone https://github.com/MilanK24/Vizard
cd Vizard
```

Navigate into the project directory and install the necessary dependencies.

```bash
pip install -r requirements.txt

```
Create a `.env` file in your project root and add the following:
```
GEMINI_API=
PANDAS_API=

```
(Do sign-in for both the below link and get the API Key )

Visit for Gemini API Key: [aistudio.google.com/apikey](https://aistudio.google.com/app/apikey)

Visit for Pandas Ai API Key: [www.pandabi/sign-in](https://www.pandabi.ai/auth/sign-in)

---

Once the installation is complete, you can start the frontend by running:

```bash
python -m streamlit run streamlit_app.py
```
Now you should be able to access the frontend on [http://localhost:8501/](http://localhost:8501/)

**2. Using Docker**

First, clone the frontend and backend repositories using the following commands:

```bash
git clone https://github.com/MilanK24/Vizard
cd Vizard
```

Create a `.env` file in your project root and add the following:
```
GEMINI_API=
PANDAS_API=

```
(Do sign-in for both the below link and get the API Key )

Visit for Gemini API Key: [aistudio.google.com/apikey](https://aistudio.google.com/app/apikey)

Visit for Pandas Ai API Key: [www.pandabi/sign-in](https://www.pandabi.ai/auth/sign-in)


---
To build the Docker images, first navigate into the projectand then build the Docker images

```bash
docker build -t dataset_insights .

```

After building the images, you can verify that they were created successfully using:
```bash
docker images
```

After building the images, run the containers for frontend
```bash
docker run -d -p 3000:3000 dataset_insights
```

Now you should be able to access the frontend on [http://localhost:3000](http://localhost:3000)

## Meet the Team

- **G V Amaresh**: [GVAmaresh ](https://github.com/GVAmaresh)
- **Milan Kumar**: [MilanK24](https://github.com/MilanK24)

## Benefits
- Privacy-Focused: The Gemini protocol emphasizes user privacy by minimizing tracking and analytics, ensuring a cleaner, more secure browsing experience.

- Simplicity and Minimalism: Designed for efficiency, Gemini uses a simplified text-based format, which reduces complexity and eliminates unnecessary features like JavaScript, making it lightweight and faster.

- Low Resource Requirements: Gemini's streamlined approach is ideal for devices with limited resources or low bandwidth, making it accessible for older systems and low-powered hardware.

- Content-Centric: Prioritizes the presentation of information rather than flashy design elements, fostering distraction-free reading and improving accessibility..

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/MilanK24/Vizard/blob/main/LICENSE) file for details.
