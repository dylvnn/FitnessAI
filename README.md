# FitAI

**An intelligent fitness recommendation system using A* search algorithm to generate personalized workout plans.**

## Features

- **Intelligent Workout Planning**: Uses A* search algorithm to optimize training plans  
- **Automatic Split Selection**: Recommends the optimal training split based on available days  
- **Personalized Nutrition Plans**: Generates meal plans based on dietary needs  
- **Scientific Approach**: Implements evidence-based training volume distribution  
- **Flexible UI**: Clean PyQt5 interface with intuitive controls  

---

## Installation

```bash
# Clone the repository
git clone https://github.com/dylvnn/FitnessAI.git

# Navigate to the project directory
cd FitnessAI

# Install required packages
pip install PyQt5
```

---

## Usage

Run the application:

```bash
python main.py
```

---

## Quick Start

1. Fill in your personal information in the **"User Profile"** tab  
2. Select your fitness goals and any dietary restrictions  
3. Choose your preferred workout frequency in the **"Settings"** tab  
4. Click **"Generate Recommendations"**

The system automatically selects the optimal training split based on your frequency:

- **2 days/week** → Full Body  
- **3 days/week** → Push/Pull/Legs  
- **4 days/week** → Upper/Lower  
- **5 days/week** → PPL + Upper/Lower  
- **6 days/week** → PPL (2x weekly)  

---

## How It Works

The core of FitAI is an **A*** search algorithm that generates optimized workout plans:

- **State**: Dictionary tracking training volume per muscle group  
- **Goal**: Adequate volume across all muscle groups  
- **Cost Function**: Estimated workout duration  
- **Heuristic**: Estimated time to reach target volume  
- **Successors**: Different workout types optimized for each day  

---

## Project Structure

- `main.py`: PyQt5 interface and application entry point  
- `fitai_core.py`: Core logic for user profiles and AI algorithms  
  - `UserProfile`: Handles user data and calculates fitness metrics  
  - `MealPlanCSP`: Generates meal plans using constraint satisfaction  
  - `WorkoutPlanGenerator`: Creates workout plans using A* search  

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Acknowledgements

- Russell & Norvig's *Artificial Intelligence: A Modern Approach* for A* search algorithm  
- Schoenfeld et al. for training volume recommendations in exercise science research
