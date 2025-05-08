import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QComboBox,
                             QPushButton, QTabWidget, QFormLayout, QSpinBox,
                             QDoubleSpinBox, QTextEdit, QGroupBox, QRadioButton,
                             QScrollArea, QCheckBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from fitai_core import UserProfile, KnowledgeBase, MealPlanCSP, WorkoutPlanGenerator, \
    _initialize_expanded_food_database, _initialize_expanded_exercise_database


class FitAIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FitAI: Advanced Fitness & Nutrition Recommendation System")
        self.setMinimumSize(1000, 800)

        # Initialize knowledge base with expanded data
        self.kb = KnowledgeBase()
        _initialize_expanded_food_database(self)
        _initialize_expanded_exercise_database(self)

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Add title label
        title_label = QLabel("FitAI: Advanced AI-Powered Fitness & Nutrition Recommendation System")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title_label)

        # Create tab widget for different sections
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # Create the tabs
        user_profile_tab = self.create_user_profile_tab()
        recommendations_tab = self.create_recommendations_tab()
        settings_tab = self.create_settings_tab()

        # Add tabs to the tab widget
        tabs.addTab(user_profile_tab, "User Profile")
        tabs.addTab(recommendations_tab, "Recommendations")
        tabs.addTab(settings_tab, "Settings")

        # Create Generate button
        generate_btn = QPushButton("Generate Recommendations")
        generate_btn.setFont(QFont("Arial", 12))
        generate_btn.setMinimumHeight(50)
        generate_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        generate_btn.clicked.connect(self.generate_recommendations)
        main_layout.addWidget(generate_btn)

    def create_user_profile_tab(self):
        """Create the user profile input tab with enhanced options"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Create form for user details
        form_group = QGroupBox("Personal Information")
        form_layout = QFormLayout()

        # Name
        self.name_input = QLineEdit()
        form_layout.addRow("Name:", self.name_input)

        # Age
        self.age_input = QSpinBox()
        self.age_input.setRange(18, 100)
        self.age_input.setValue(30)
        form_layout.addRow("Age:", self.age_input)

        # Height - Feet and Inches
        height_layout = QHBoxLayout()
        self.height_ft_input = QSpinBox()
        self.height_ft_input.setRange(2, 7)  # Reasonable height range in feet
        self.height_ft_input.setValue(5)
        self.height_ft_input.setSuffix(" ft")

        self.height_in_input = QSpinBox()
        self.height_in_input.setRange(0, 11)  # 0 to 11 inches
        self.height_in_input.setValue(10)
        self.height_in_input.setSuffix(" in")

        height_layout.addWidget(self.height_ft_input)
        height_layout.addWidget(self.height_in_input)
        form_layout.addRow("Height:", height_layout)

        # Weight in pounds
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(50, 500)  # Reasonable weight range in pounds
        self.weight_input.setValue(165)  # Default 165 pounds
        self.weight_input.setSuffix(" lbs")
        form_layout.addRow("Weight:", self.weight_input)

        # Gender
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female"])
        form_layout.addRow("Gender:", self.gender_input)

        # Activity Level
        self.activity_input = QComboBox()
        self.activity_input.addItems([
            "Sedentary (little or no exercise)",
            "Light (light exercise 1-3 days/week)",
            "Moderate (moderate exercise 3-5 days/week)",
            "Active (hard exercise 6-7 days/week)",
            "Very Active (very hard exercise & physical job)"
        ])
        self.activity_input.setCurrentIndex(2)  # Default to moderate
        form_layout.addRow("Activity Level:", self.activity_input)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        # Create group for fitness goals
        goals_group = QGroupBox("Fitness Goals")
        goals_layout = QVBoxLayout()

        self.goal_weight_loss = QRadioButton("Weight Loss")
        self.goal_muscle_gain = QRadioButton("Muscle Gain")
        self.goal_maintenance = QRadioButton("Maintenance")
        self.goal_athletic = QRadioButton("Athletic Performance")
        self.goal_health = QRadioButton("General Health")

        self.goal_weight_loss.setChecked(True)  # Default to weight loss

        goals_layout.addWidget(self.goal_weight_loss)
        goals_layout.addWidget(self.goal_muscle_gain)
        goals_layout.addWidget(self.goal_maintenance)
        goals_layout.addWidget(self.goal_athletic)
        goals_layout.addWidget(self.goal_health)

        goals_group.setLayout(goals_layout)
        layout.addWidget(goals_group)

        # Create group for dietary restrictions
        diet_group = QGroupBox("Dietary Restrictions")
        diet_layout = QVBoxLayout()

        self.restriction_vegetarian = QCheckBox("Vegetarian")
        self.restriction_vegan = QCheckBox("Vegan")
        self.restriction_gluten_free = QCheckBox("Gluten-Free")
        self.restriction_dairy_free = QCheckBox("Dairy-Free")
        self.restriction_nut_free = QCheckBox("Nut-Free")
        self.restriction_keto = QCheckBox("Keto-Friendly")
        self.restriction_paleo = QCheckBox("Paleo-Friendly")

        diet_layout.addWidget(self.restriction_vegetarian)
        diet_layout.addWidget(self.restriction_vegan)
        diet_layout.addWidget(self.restriction_gluten_free)
        diet_layout.addWidget(self.restriction_dairy_free)
        diet_layout.addWidget(self.restriction_nut_free)
        diet_layout.addWidget(self.restriction_keto)
        diet_layout.addWidget(self.restriction_paleo)

        diet_group.setLayout(diet_layout)
        layout.addWidget(diet_group)

        return tab

    def create_recommendations_tab(self):
        """Create the recommendations display tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Create scroll area for recommendations
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Add summary section
        summary_group = QGroupBox("Summary")
        summary_layout = QVBoxLayout()
        self.summary_text = QLabel("Please generate recommendations to view your summary.")
        self.summary_text.setWordWrap(True)
        summary_layout.addWidget(self.summary_text)
        summary_group.setLayout(summary_layout)
        scroll_layout.addWidget(summary_group)

        # Add meal plan section
        meal_group = QGroupBox("Meal Plan")
        meal_layout = QVBoxLayout()
        self.meal_text = QTextEdit()
        self.meal_text.setReadOnly(True)
        self.meal_text.setPlaceholderText("Your meal plan will appear here after generation.")
        meal_layout.addWidget(self.meal_text)
        meal_group.setLayout(meal_layout)
        scroll_layout.addWidget(meal_group)

        # Add workout plan section
        workout_group = QGroupBox("Workout Plan")
        workout_layout = QVBoxLayout()
        self.workout_text = QTextEdit()
        self.workout_text.setReadOnly(True)
        self.workout_text.setPlaceholderText("Your workout plan will appear here after generation.")
        workout_layout.addWidget(self.workout_text)
        workout_group.setLayout(workout_layout)
        scroll_layout.addWidget(workout_group)

        # Set scroll content
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        return tab

    def create_settings_tab(self):
        """Create a simplified settings tab with automatic split selection"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Workout settings group
        workout_settings = QGroupBox("Workout Settings")
        workout_layout = QFormLayout()

        # Number of workout days (which will determine the split)
        self.workout_days = QComboBox()
        self.workout_days.addItems(["2 days/week", "3 days/week", "4 days/week", "5 days/week", "6 days/week"])
        self.workout_days.setCurrentIndex(2)  # Default to 4 days

        # Add a label to show the suggested split
        self.split_description = QLabel("Recommended Split: Upper/Lower Split")
        self.split_description.setStyleSheet("color: #666; font-style: italic;")

        # Connect the workout days dropdown to update the split description
        self.workout_days.currentIndexChanged.connect(self.update_split_description)

        workout_layout.addRow("Training Frequency:", self.workout_days)
        workout_layout.addRow("", self.split_description)

        # Experience level
        self.experience_level = QComboBox()
        self.experience_level.addItems([
            "Beginner",
            "Intermediate",
            "Advanced"
        ])
        workout_layout.addRow("Experience Level:", self.experience_level)

        workout_settings.setLayout(workout_layout)
        layout.addWidget(workout_settings)

        # Meal plan settings group
        meal_settings = QGroupBox("Meal Plan Settings")
        meal_layout = QFormLayout()

        # Number of meals
        self.meals_per_day = QComboBox()
        self.meals_per_day.addItems([
            "3 meals/day",
            "4 meals/day",
            "5 meals/day",
            "6 meals/day"
        ])
        self.meals_per_day.setCurrentIndex(1)  # Default to 4 meals
        meal_layout.addRow("Meals per Day:", self.meals_per_day)

        # Macro preference
        self.macro_preference = QComboBox()
        self.macro_preference.addItems([
            "Balanced",
            "High Protein",
            "High Carb",
            "Low Carb",
            "High Fat",
            "Low Fat"
        ])
        meal_layout.addRow("Macro Preference:", self.macro_preference)

        meal_settings.setLayout(meal_layout)
        layout.addWidget(meal_settings)

        # Initialize the split description
        self.update_split_description()

        return tab

    def update_split_description(self):
        """Update the workout split description based on number of days selected"""
        days = int(self.workout_days.currentText().split()[0])

        if days == 2:
            split = "Full Body Split (2x per week)"
            description = "Each workout targets the entire body with compound exercises."
        elif days == 3:
            split = "Push/Pull/Legs Split"
            description = "One day each for push muscles, pull muscles, and legs."
        elif days == 4:
            split = "Upper/Lower Split (2x per week)"
            description = "Alternating upper and lower body workouts."
        elif days == 5:
            split = "Push/Pull/Legs/Upper/Lower Split"
            description = "PPL with additional upper and lower day."
        elif days == 6:
            split = "Push/Pull/Legs Split (2x per week)"
            description = "Full PPL rotation twice per week."
        else:
            split = "Custom Split"
            description = "Customized based on your goals."

        self.split_description.setText(f"Recommended Split: {split}\n{description}")

    def get_recommended_split_type(self, days):
        """Determine the recommended split type based on number of days"""
        if days == 2:
            return "full_body"
        elif days == 3:
            return "ppl"
        elif days == 4:
            return "upper_lower"
        elif days == 5:
            return "ppl_ul"
        elif days == 6:
            return "ppl_2x"
        else:
            return "full_body"

    def generate_recommendations(self):
        """Generate meal and workout recommendations based on user profile"""
        try:
            # Get user profile
            user = self._get_user_profile()

            # Create recommendation engines
            meal_planner = MealPlanCSP(self.kb.foods, user)
            workout_planner = WorkoutPlanGenerator(self.kb.exercises, user)

            # Get settings
            workout_days = int(self.workout_days.currentText().split()[0])
            meals_per_day = int(self.meals_per_day.currentText().split()[0])

            # Get the recommended split type
            split_type = self.get_recommended_split_type(workout_days)

            # Generate recommendations
            meal_plan = meal_planner.generate_meal_plan(meals_per_day=meals_per_day)

            # Pass the split_type as a parameter to the workout planner
            workout_plan = workout_planner.generate_workout_plan(days_per_week=workout_days)

            # Update summary
            tdee = user.calculate_tdee()
            bmr = user.calculate_bmr()

            if "weight loss" in user.goals:
                calorie_target = int(tdee * 0.8)
                goal_text = "Weight Loss"
            elif "muscle gain" in user.goals:
                calorie_target = int(tdee * 1.1)
                goal_text = "Muscle Gain"
            else:
                calorie_target = int(tdee)
                goal_text = "Maintenance"

            # Get the split name for display
            split_name = self.split_description.text().split(":", 1)[1].split("\n")[0].strip()

            summary = (f"<b>Name:</b> {self.name_input.text()}<br>"
                       f"<b>Height:</b> {user.height_ft}' {user.height_in}\"<br>"
                       f"<b>Weight:</b> {user.weight_lbs} lbs<br>"
                       f"<b>Goal:</b> {goal_text}<br>"
                       f"<b>Basal Metabolic Rate (BMR):</b> {bmr:.0f} calories<br>"
                       f"<b>Total Daily Energy Expenditure (TDEE):</b> {tdee:.0f} calories<br>"
                       f"<b>Daily Calorie Target:</b> {calorie_target} calories<br>"
                       f"<b>Workout Plan:</b> {workout_days} days per week ({split_name})<br>"
                       f"<b>Meal Plan:</b> {meals_per_day} meals per day")

            self.summary_text.setText(summary)

            # Update meal plan
            meal_text = ""
            for meal_name, foods in meal_plan:
                meal_text += f"<h3>{meal_name}</h3>"
                meal_text += "<ul>"
                for food in foods:
                    nutrition = self.kb.foods[food]
                    meal_text += (f"<li><b>{food}</b> - "
                                  f"{nutrition['calories']} cal, "
                                  f"{nutrition['protein']}g protein, "
                                  f"{nutrition['carbs']}g carbs, "
                                  f"{nutrition['fat']}g fat</li>")
                meal_text += "</ul>"

            self.meal_text.setHtml(meal_text)

            # Update workout plan
            workout_text = ""
            for i, (day_name, workout) in enumerate(workout_plan):
                workout_text += f"<h3>Day {i + 1}: {day_name}</h3>"
                workout_text += "<ul>"
                for exercise in workout:
                    if isinstance(exercise, tuple) and len(exercise) == 3:
                        exercise_name, sets, rep_range = exercise
                    else:
                        exercise_name = exercise
                        sets = 3  # Default sets
                        rep_range = "8-12"  # Default rep range

                    muscle = self.kb.exercises[exercise_name]['muscle_group']
                    difficulty = self.kb.exercises[exercise_name]['difficulty']
                    category = self.kb.exercises[exercise_name].get('category', 'compound')
                    workout_text += (f"<li><b>{exercise_name}</b> - "
                                     f"{sets} sets × {rep_range} reps "
                                     f"({muscle}, {difficulty} difficulty, {category})</li>")
                workout_text += "</ul>"

            self.workout_text.setHtml(workout_text)

            # Show success message
            QMessageBox.information(self, "Success",
                                    "Recommendations successfully generated!")

        except Exception as e:
            # Show error message
            QMessageBox.critical(self, "Error",
                                 f"An error occurred while generating recommendations:\n{str(e)}")

    def _get_user_profile(self):
        """Collect user profile data from the UI inputs"""
        # Get basic information
        age = self.age_input.value()
        height_ft = self.height_ft_input.value()
        height_in = self.height_in_input.value()
        weight_lbs = self.weight_input.value()
        gender = self.gender_input.currentText().lower()

        # Get activity level
        activity_map = {
            0: "sedentary",
            1: "light",
            2: "moderate",
            3: "active",
            4: "very active"
        }
        activity = activity_map[self.activity_input.currentIndex()]

        # Get fitness goal
        goals = []
        if self.goal_weight_loss.isChecked():
            goals.append("weight loss")
        elif self.goal_muscle_gain.isChecked():
            goals.append("muscle gain")
        elif self.goal_maintenance.isChecked():
            goals.append("maintenance")
        elif self.goal_athletic.isChecked():
            goals.append("athletic")
        elif self.goal_health.isChecked():
            goals.append("health")

        # Get dietary restrictions
        restrictions = []
        if self.restriction_vegetarian.isChecked():
            restrictions.append("vegetarian")
        if self.restriction_vegan.isChecked():
            restrictions.append("vegan")
        if self.restriction_gluten_free.isChecked():
            restrictions.append("gluten")
        if self.restriction_dairy_free.isChecked():
            restrictions.append("dairy")
        if self.restriction_nut_free.isChecked():
            restrictions.append("nuts")
        if self.restriction_keto.isChecked():
            restrictions.append("keto")
        if self.restriction_paleo.isChecked():
            restrictions.append("paleo")

        # Create and return user profile
        return UserProfile(
            age=age,
            height_ft=height_ft,
            height_in=height_in,
            weight_lbs=weight_lbs,
            gender=gender,
            activity_level=activity,
            goals=goals,
            restrictions=restrictions
        )


def main():
    app = QApplication(sys.argv)
    window = FitAIApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()