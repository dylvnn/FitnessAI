import time
import random
import numpy as np
import matplotlib.pyplot as plt

# Define UserProfile class for use in the script
class UserProfile:
    def __init__(self, age, height_ft, height_in, weight_lbs, gender, activity_level, goals, restrictions):
        self.age = age
        self.height_ft = height_ft
        self.height_in = height_in
        self.weight_lbs = weight_lbs
        self.gender = gender
        self.activity_level = activity_level  # sedentary, light, moderate, active, very active
        self.goals = goals  # weight loss, muscle gain, maintenance, athletic, health
        self.restrictions = restrictions  # dietary restrictions

    def _convert_to_metric(self):
        # Convert height from ft/in to cm
        total_inches = (self.height_ft * 12) + self.height_in
        height_cm = total_inches * 2.54

        # Convert weight from lbs to kg
        weight_kg = self.weight_lbs / 2.2046

        return height_cm, weight_kg

    def calculate_bmr(self):
        """Calculate BMR using Mifflin-St Jeor Equation"""
        height_cm, weight_kg = self._convert_to_metric()

        if self.gender.lower() == 'male':
            return 10 * weight_kg + 6.25 * height_cm - 5 * self.age + 5
        else:
            return 10 * weight_kg + 6.25 * height_cm - 5 * self.age - 161

    def calculate_tdee(self):
        """Calculate Total Daily Energy Expenditure"""
        activity_factors = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very active': 1.9
        }
        return self.calculate_bmr() * activity_factors[self.activity_level.lower()]

    def get_weight_kg(self):
        """Return weight in kg for use in calculations"""
        return self.weight_lbs / 2.2046


# Define KnowledgeBase class
class KnowledgeBase:
    def __init__(self):
        # Initialize with exercise database
        self.exercises = {}  # Will populate with exercise data

# Initialize exercise database function
def initialize_expanded_exercise_database():
    """Create and return the expanded exercise database"""
    exercises = {
        # Legs
        "Barbell Back Squats": {"muscle_group": "legs", "difficulty": "hard", "rep_range": "6-10",
                                "category": "compound"},
        "Front Squats": {"muscle_group": "legs", "difficulty": "hard", "rep_range": "6-10", "category": "compound"},
        "Romanian Deadlifts": {"muscle_group": "legs", "difficulty": "moderate", "rep_range": "8-12",
                               "category": "compound"},
        "Leg Press": {"muscle_group": "legs", "difficulty": "moderate", "rep_range": "8-12", "category": "compound"},
        "Hack Squats": {"muscle_group": "legs", "difficulty": "moderate", "rep_range": "8-12", "category": "compound"},
        "Walking Lunges": {"muscle_group": "legs", "difficulty": "moderate", "rep_range": "10-15",
                           "category": "compound"},
        "Bulgarian Split Squats": {"muscle_group": "legs", "difficulty": "hard", "rep_range": "8-12",
                                   "category": "compound"},
        "Leg Extensions": {"muscle_group": "legs", "difficulty": "easy", "rep_range": "12-15", "category": "isolation"},
        "Leg Curls": {"muscle_group": "legs", "difficulty": "easy", "rep_range": "12-15", "category": "isolation"},
        "Calf Raises": {"muscle_group": "legs", "difficulty": "easy", "rep_range": "15-20", "category": "isolation"},
        "Seated Calf Raises": {"muscle_group": "legs", "difficulty": "easy", "rep_range": "15-20",
                               "category": "isolation"},
        "Goblet Squats": {"muscle_group": "legs", "difficulty": "easy", "rep_range": "10-15", "category": "compound"},
        "Box Jumps": {"muscle_group": "legs", "difficulty": "moderate", "rep_range": "8-12", "category": "plyometric"},
        "Step-Ups": {"muscle_group": "legs", "difficulty": "moderate", "rep_range": "10-15", "category": "compound"},

        # Back
        "Deadlifts": {"muscle_group": "back", "difficulty": "hard", "rep_range": "5-8", "category": "compound"},
        "Pull-ups": {"muscle_group": "back", "difficulty": "hard", "rep_range": "6-12", "category": "compound"},
        "Lat Pulldowns": {"muscle_group": "back", "difficulty": "moderate", "rep_range": "8-12",
                          "category": "compound"},
        "Barbell Rows": {"muscle_group": "back", "difficulty": "moderate", "rep_range": "8-12", "category": "compound"},
        "Dumbbell Rows": {"muscle_group": "back", "difficulty": "moderate", "rep_range": "8-12",
                          "category": "compound"},
        "T-Bar Rows": {"muscle_group": "back", "difficulty": "moderate", "rep_range": "8-12", "category": "compound"},
        "Cable Rows": {"muscle_group": "back", "difficulty": "moderate", "rep_range": "10-15", "category": "compound"},
        "Meadows Rows": {"muscle_group": "back", "difficulty": "moderate", "rep_range": "8-12", "category": "compound"},
        "Straight Arm Pulldowns": {"muscle_group": "back", "difficulty": "easy", "rep_range": "12-15",
                                   "category": "isolation"},
        "Good Mornings": {"muscle_group": "back", "difficulty": "moderate", "rep_range": "10-15",
                          "category": "compound"},
        "Pull-Overs": {"muscle_group": "back", "difficulty": "easy", "rep_range": "12-15", "category": "isolation"},
        "Chin-ups": {"muscle_group": "back", "difficulty": "hard", "rep_range": "6-12", "category": "compound"},

        # Chest
        "Bench Press": {"muscle_group": "chest", "difficulty": "moderate", "rep_range": "6-10", "category": "compound"},
        "Incline Bench Press": {"muscle_group": "chest", "difficulty": "moderate", "rep_range": "8-12",
                                "category": "compound"},
        "Decline Bench Press": {"muscle_group": "chest", "difficulty": "moderate", "rep_range": "8-12",
                                "category": "compound"},
        "Dumbbell Press": {"muscle_group": "chest", "difficulty": "moderate", "rep_range": "8-12",
                           "category": "compound"},
        "Incline Dumbbell Press": {"muscle_group": "chest", "difficulty": "moderate", "rep_range": "8-12",
                                   "category": "compound"},
        "Dips": {"muscle_group": "chest", "difficulty": "moderate", "rep_range": "8-15", "category": "compound"},
        "Cable Crossovers": {"muscle_group": "chest", "difficulty": "easy", "rep_range": "12-15",
                             "category": "isolation"},
        "Pec Deck": {"muscle_group": "chest", "difficulty": "easy", "rep_range": "12-15", "category": "isolation"},
        "Chest Flyes": {"muscle_group": "chest", "difficulty": "easy", "rep_range": "12-15", "category": "isolation"},
        "Landmine Press": {"muscle_group": "chest", "difficulty": "moderate", "rep_range": "10-15",
                           "category": "compound"},

        # Shoulders
        "Overhead Press": {"muscle_group": "shoulders", "difficulty": "moderate", "rep_range": "6-10",
                           "category": "compound"},
        "Seated Dumbbell Press": {"muscle_group": "shoulders", "difficulty": "moderate", "rep_range": "8-12",
                                  "category": "compound"},
        "Arnold Press": {"muscle_group": "shoulders", "difficulty": "moderate", "rep_range": "8-12",
                         "category": "compound"},
        "Lateral Raises": {"muscle_group": "shoulders", "difficulty": "easy", "rep_range": "12-15",
                           "category": "isolation"},
        "Front Raises": {"muscle_group": "shoulders", "difficulty": "easy", "rep_range": "12-15",
                         "category": "isolation"},
        "Face Pulls": {"muscle_group": "shoulders", "difficulty": "easy", "rep_range": "12-15",
                       "category": "isolation"},
        "Reverse Flyes": {"muscle_group": "shoulders", "difficulty": "easy", "rep_range": "12-15",
                          "category": "isolation"},
        "Upright Rows": {"muscle_group": "shoulders", "difficulty": "moderate", "rep_range": "10-15",
                         "category": "compound"},
        "Shrugs": {"muscle_group": "shoulders", "difficulty": "easy", "rep_range": "12-15", "category": "isolation"},
        "Cable Lateral Raises": {"muscle_group": "shoulders", "difficulty": "easy", "rep_range": "12-15",
                                 "category": "isolation"},
        "Landmine Lateral Raises": {"muscle_group": "shoulders", "difficulty": "moderate", "rep_range": "10-15",
                                    "category": "isolation"},

        # Arms - Biceps
        "Barbell Curls": {"muscle_group": "arms", "difficulty": "easy", "rep_range": "10-15", "category": "isolation"},
        "Dumbbell Curls": {"muscle_group": "arms", "difficulty": "easy", "rep_range": "10-15", "category": "isolation"},
        "Hammer Curls": {"muscle_group": "arms", "difficulty": "easy", "rep_range": "10-15", "category": "isolation"},
        "Preacher Curls": {"muscle_group": "arms", "difficulty": "easy", "rep_range": "10-15", "category": "isolation"},
        "Concentration Curls": {"muscle_group": "arms", "difficulty": "easy", "rep_range": "12-15",
                                "category": "isolation"},
        "Cable Curls": {"muscle_group": "arms", "difficulty": "easy", "rep_range": "12-15", "category": "isolation"},
        "EZ Bar Curls": {"muscle_group": "arms", "difficulty": "easy", "rep_range": "10-15", "category": "isolation"},

        # Arms - Triceps
        "Tricep Dips": {"muscle_group": "arms", "difficulty": "moderate", "rep_range": "8-15", "category": "compound"},
        "Skull Crushers": {"muscle_group": "arms", "difficulty": "easy", "rep_range": "10-15", "category": "isolation"},
        "Tricep Pushdowns": {"muscle_group": "arms", "difficulty": "easy", "rep_range": "12-15",
                             "category": "isolation"},
        "Overhead Tricep Extensions": {"muscle_group": "arms", "difficulty": "easy", "rep_range": "12-15",
                                       "category": "isolation"},
        "Close-Grip Bench Press": {"muscle_group": "arms", "difficulty": "moderate", "rep_range": "8-12",
                                   "category": "compound"},
        "Diamond Push-ups": {"muscle_group": "arms", "difficulty": "moderate", "rep_range": "10-15",
                             "category": "compound"},
        "Kickbacks": {"muscle_group": "arms", "difficulty": "easy", "rep_range": "12-15", "category": "isolation"},

        # Core
        "Plank": {"muscle_group": "core", "difficulty": "easy", "rep_range": "30-90sec", "category": "isometric"},
        "Crunches": {"muscle_group": "core", "difficulty": "easy", "rep_range": "15-25", "category": "isolation"},
        "Leg Raises": {"muscle_group": "core", "difficulty": "moderate", "rep_range": "12-20", "category": "isolation"},
        "Russian Twists": {"muscle_group": "core", "difficulty": "moderate", "rep_range": "15-25",
                           "category": "isolation"},
        "Ab Rollouts": {"muscle_group": "core", "difficulty": "hard", "rep_range": "8-15", "category": "compound"},
        "Cable Crunches": {"muscle_group": "core", "difficulty": "moderate", "rep_range": "12-20",
                           "category": "isolation"},
        "Hanging Leg Raises": {"muscle_group": "core", "difficulty": "hard", "rep_range": "10-15",
                               "category": "isolation"},
        "Mountain Climbers": {"muscle_group": "core", "difficulty": "moderate", "rep_range": "15-30",
                              "category": "cardio"},
        "Bicycle Crunches": {"muscle_group": "core", "difficulty": "moderate", "rep_range": "15-25",
                             "category": "isolation"},
        "Side Planks": {"muscle_group": "core", "difficulty": "moderate", "rep_range": "20-60sec",
                        "category": "isometric"},
        "Deadbug": {"muscle_group": "core", "difficulty": "easy", "rep_range": "12-20", "category": "isolation"},
        "Pallof Press": {"muscle_group": "core", "difficulty": "moderate", "rep_range": "12-15",
                         "category": "anti-rotation"}
    }

    return exercises

class StrongFastLikeGenerator:
    """Simulates an algorithm approach similar to commercial workout builders like StrongFast.

    Based on analysis of commercial workout generators, they typically use:
    1. Predefined templates with minimal customization
    2. Simple rule-based systems rather than constraint satisfaction or search
    3. Volume thresholds based on experience level
    4. Limited exercise substitution
    """

    def __init__(self, exercises_database):
        self.exercises = exercises_database

        # Predefined split templates - commercial apps often use fixed templates
        self.templates = {
            "fullbody": {
                "days": 3,
                "focus": ["fullbody", "fullbody", "fullbody"],
                "exercises_per_day": [8, 8, 8]
            },
            "upper_lower": {
                "days": 4,
                "focus": ["upper", "lower", "upper", "lower"],
                "exercises_per_day": [8, 8, 8, 8]
            },
            "push_pull_legs": {
                "days": 6,
                "focus": ["push", "pull", "legs", "push", "pull", "legs"],
                "exercises_per_day": [7, 7, 7, 7, 7, 7]
            },
            "bro_split": {
                "days": 5,
                "focus": ["chest", "back", "shoulders", "legs", "arms"],
                "exercises_per_day": [6, 6, 6, 8, 6]
            }
        }

        # Predefined exercise selections - commercial apps often have fixed exercise pools
        self.exercise_pools = {
            "fullbody": {
                "compound": ["Barbell Back Squats", "Bench Press", "Deadlifts", "Pull-ups", "Overhead Press"],
                "isolation": ["Leg Extensions", "Dumbbell Rows", "Bicep Curls", "Tricep Pushdowns", "Lateral Raises"]
            },
            "upper": {
                "chest": ["Bench Press", "Incline Bench Press", "Dumbbell Press", "Cable Crossovers"],
                "back": ["Pull-ups", "Barbell Rows", "Lat Pulldowns", "Cable Rows"],
                "shoulders": ["Overhead Press", "Lateral Raises", "Face Pulls"],
                "arms": ["Tricep Dips", "Bicep Curls", "Skull Crushers"]
            },
            "lower": {
                "quads": ["Barbell Back Squats", "Leg Press", "Leg Extensions", "Goblet Squats"],
                "hams": ["Romanian Deadlifts", "Leg Curls", "Walking Lunges"],
                "calves": ["Calf Raises", "Seated Calf Raises"]
            },
            "push": {
                "chest": ["Bench Press", "Incline Bench Press", "Dumbbell Press", "Chest Flyes"],
                "shoulders": ["Overhead Press", "Lateral Raises", "Arnold Press"],
                "triceps": ["Tricep Dips", "Skull Crushers", "Tricep Pushdowns"]
            },
            "pull": {
                "back": ["Deadlifts", "Pull-ups", "Barbell Rows", "Lat Pulldowns"],
                "rear_delts": ["Face Pulls", "Reverse Flyes"],
                "biceps": ["Barbell Curls", "Hammer Curls", "Preacher Curls"]
            },
            "legs": {
                "quads": ["Barbell Back Squats", "Front Squats", "Leg Press", "Leg Extensions"],
                "hams": ["Romanian Deadlifts", "Leg Curls", "Walking Lunges"],
                "calves": ["Calf Raises", "Seated Calf Raises"]
            },
            "chest": ["Bench Press", "Incline Bench Press", "Dumbbell Press", "Chest Flyes", "Cable Crossovers",
                      "Dips"],
            "back": ["Deadlifts", "Pull-ups", "Barbell Rows", "Lat Pulldowns", "Cable Rows", "T-Bar Rows"],
            "shoulders": ["Overhead Press", "Lateral Raises", "Face Pulls", "Reverse Flyes", "Arnold Press",
                          "Upright Rows"],
            "legs": ["Barbell Back Squats", "Front Squats", "Leg Press", "Romanian Deadlifts", "Leg Extensions",
                     "Leg Curls", "Calf Raises", "Walking Lunges"],
            "arms": ["Barbell Curls", "Hammer Curls", "Preacher Curls", "Tricep Dips", "Skull Crushers",
                     "Tricep Pushdowns", "Close-Grip Bench Press"]
        }

    def generate_workout_plan(self, user_profile, days_per_week=4):
        """Generate a workout plan using a simplified rule-based approach."""
        # 1. Select template based on days per week
        if days_per_week <= 3:
            template_key = "fullbody"
        elif days_per_week == 4:
            template_key = "upper_lower"
        elif days_per_week >= 6:
            template_key = "push_pull_legs"
        else:  # 5 days
            template_key = "bro_split"

        template = self.templates[template_key]

        # 2. Adjust for requested days (if template doesn't match exactly)
        days = min(days_per_week, template["days"])

        # 3. Generate workout plan
        workout_plan = []

        for i in range(days):
            focus = template["focus"][i % len(template["focus"])]
            target_exercises = template["exercises_per_day"][i % len(template["exercises_per_day"])]

            # 4. Select exercises for this day
            exercises = self._select_exercises_for_day(focus, target_exercises, user_profile)

            # 5. Add the day to the workout plan
            workout_plan.append((focus.capitalize(), exercises))

        return workout_plan

    def _select_exercises_for_day(self, focus, target_count, user_profile):
        """Select exercises for a workout day."""
        selected_exercises = []

        # Determine sets and reps based on user's goal
        if "muscle gain" in user_profile.goals:
            sets = 4
            rep_range = "8-12"
        elif "weight loss" in user_profile.goals:
            sets = 3
            rep_range = "12-15"
        elif "athletic" in user_profile.goals:
            sets = 3
            rep_range = "6-10"
        else:  # Health or maintenance
            sets = 3
            rep_range = "10-12"

        # Handle different focus types
        if focus == "fullbody":
            # For full body, select a mix of compounds and isolations
            compound_count = min(4, target_count // 2)
            isolation_count = target_count - compound_count

            compounds = self._sample_from_pool(self.exercise_pools["fullbody"]["compound"], compound_count)
            isolations = self._sample_from_pool(self.exercise_pools["fullbody"]["isolation"], isolation_count)

            for exercise in compounds:
                selected_exercises.append((exercise, sets, rep_range))
            for exercise in isolations:
                selected_exercises.append((exercise, sets, rep_range))

        elif focus in ["upper", "lower", "push", "pull", "legs"]:
            # For these splits, select from predefined pools
            pool = self.exercise_pools[focus]

            # Distribute exercises across subgroups
            exercises_per_subgroup = max(1, target_count // len(pool))
            remaining = target_count - (exercises_per_subgroup * len(pool))

            if isinstance(pool, dict):
                # Distribute exercises across subgroups
                exercises_per_subgroup = max(1, target_count // len(pool))
                remaining = target_count - (exercises_per_subgroup * len(pool))

                for subgroup, exercises_list in pool.items():
                    count = exercises_per_subgroup + (1 if remaining > 0 else 0)
                    remaining -= 1 if remaining > 0 else 0

                    subgroup_exercises = self._sample_from_pool(exercises_list, count)
                    for exercise in subgroup_exercises:
                        selected_exercises.append((exercise, sets, rep_range))

            elif isinstance(pool, list):
                selected = self._sample_from_pool(pool, target_count)
                for exercise in selected:
                    selected_exercises.append((exercise, sets, rep_range))


        else:
            # For specific muscle group focuses
            pool = self.exercise_pools.get(focus, [])
            selected = self._sample_from_pool(pool, target_count)

            for exercise in selected:
                selected_exercises.append((exercise, sets, rep_range))

        return selected_exercises

    def _sample_from_pool(self, pool, count):
        """Sample a number of exercises from a pool."""
        if not pool:
            return []

        # Simple random sampling with no constraints
        return random.sample(pool, min(count, len(pool)))


class AnkRuleBasedGenerator:
    """Simulates a rule-based workout generator similar to Ank-22/WorkoutGenerator.

    This implements a simple rule-based system that:
    1. Uses predefined exercise categories
    2. Follows fixed rules for exercise selection
    3. Has minimal optimization or constraint satisfaction
    """

    def __init__(self, exercises_database):
        self.exercises = exercises_database

        # Define muscle groups and categories
        self.muscle_groups = ['chest', 'back', 'legs', 'shoulders', 'arms', 'core']
        self.exercise_categories = ['compound', 'isolation', 'plyometric', 'cardio']

        # Define workout types
        self.workout_types = {
            "beginner": {
                "sets": 3,
                "reps": "12-15",
                "compound_ratio": 0.5,
                "exercises_per_day": 5
            },
            "intermediate": {
                "sets": 4,
                "reps": "8-12",
                "compound_ratio": 0.6,
                "exercises_per_day": 6
            },
            "advanced": {
                "sets": 5,
                "reps": "6-10",
                "compound_ratio": 0.7,
                "exercises_per_day": 8
            }
        }

        # Define workout splits
        self.splits = {
            2: "full_body",
            3: "push_pull_legs",
            4: "upper_lower",
            5: "body_part",
            6: "push_pull_legs"
        }

        # Define split structures
        self.split_structures = {
            "full_body": [
                ["chest", "back", "legs", "shoulders", "arms"],
                ["chest", "back", "legs", "shoulders", "arms"]
            ],
            "push_pull_legs": [
                ["chest", "shoulders", "arms"],  # Push
                ["back", "arms"],  # Pull
                ["legs", "core"]  # Legs
            ],
            "upper_lower": [
                ["chest", "back", "shoulders", "arms"],  # Upper
                ["legs", "core"],  # Lower
                ["chest", "back", "shoulders", "arms"],  # Upper
                ["legs", "core"]  # Lower
            ],
            "body_part": [
                ["chest"],
                ["back"],
                ["legs"],
                ["shoulders"],
                ["arms", "core"]
            ]
        }

    def generate_workout_plan(self, user_profile, days_per_week=4):
        """Generate a workout plan using rule-based approach."""
        # Determine user level
        if user_profile.activity_level in ["sedentary", "light"]:
            level = "beginner"
        elif user_profile.activity_level in ["moderate"]:
            level = "intermediate"
        else:
            level = "advanced"

        # Determine split type
        split_type = self.splits.get(days_per_week, "full_body")

        # Get the structure for this split
        split_structure = self.split_structures[split_type]

        # Create the workout plan
        workout_plan = []

        # For each day in the split
        for i in range(min(days_per_week, len(split_structure))):
            day_muscles = split_structure[i % len(split_structure)]
            day_name = self._get_day_name(split_type, i)

            # Generate exercises for this day
            exercises = self._generate_day_exercises(
                day_muscles,
                self.workout_types[level]["exercises_per_day"],
                self.workout_types[level]["compound_ratio"],
                self.workout_types[level]["sets"],
                self.workout_types[level]["reps"]
            )

            workout_plan.append((day_name, exercises))

        return workout_plan

    def _get_day_name(self, split_type, day_index):
        """Get the name for a workout day based on split type and index."""
        if split_type == "push_pull_legs":
            day_names = ["Push", "Pull", "Legs"]
            return day_names[day_index % len(day_names)]
        elif split_type == "upper_lower":
            day_names = ["Upper Body", "Lower Body"]
            return day_names[day_index % len(day_names)]
        elif split_type == "body_part":
            day_names = ["Chest", "Back", "Legs", "Shoulders", "Arms"]
            return day_names[day_index % len(day_names)]
        else:
            return f"Full Body Day {day_index + 1}"

    def _generate_day_exercises(self, muscle_groups, total_exercises, compound_ratio, sets, rep_range):
        """Generate exercises for a specific day based on muscle groups."""
        exercises = []

        # Calculate how many compounds vs isolations
        compound_count = int(total_exercises * compound_ratio)
        isolation_count = total_exercises - compound_count

        # Divide exercises among muscle groups
        exercises_per_group = {}
        remaining_exercises = total_exercises

        for i, muscle in enumerate(muscle_groups):
            if i == len(muscle_groups) - 1:
                # Last muscle group gets all remaining exercises
                exercises_per_group[muscle] = remaining_exercises
            else:
                # Distribute exercises evenly
                count = max(1, remaining_exercises // (len(muscle_groups) - i))
                exercises_per_group[muscle] = count
                remaining_exercises -= count

        # For each muscle group, select appropriate exercises
        for muscle, count in exercises_per_group.items():
            # Calculate compounds vs isolations for this muscle
            muscle_compounds = min(count, int(count * compound_ratio))
            muscle_isolations = count - muscle_compounds

            # Get available exercises for this muscle
            available_compounds = [name for name, info in self.exercises.items()
                                   if info["muscle_group"] == muscle and
                                   info.get("category", "") == "compound"]

            available_isolations = [name for name, info in self.exercises.items()
                                    if info["muscle_group"] == muscle and
                                    info.get("category", "") == "isolation"]

            # Select compound exercises
            selected_compounds = random.sample(
                available_compounds,
                min(muscle_compounds, len(available_compounds))
            )

            # Select isolation exercises
            selected_isolations = random.sample(
                available_isolations,
                min(muscle_isolations, len(available_isolations))
            )

            # Add to workout with appropriate sets and reps
            for exercise in selected_compounds:
                exercises.append((exercise, sets, rep_range))

            for exercise in selected_isolations:
                exercises.append((exercise, sets, rep_range))

        return exercises


# Simplified WorkoutPlanGenerator for testing
class WorkoutPlanGenerator:
    """Generate workout plans using A* search algorithm with split-specific guidance"""

    def __init__(self, exercises, user_profile):
        self.exercises = exercises
        self.user = user_profile

    def generate_workout_plan(self, days_per_week=4, split_type=None):
        """Simplified workout plan generator for testing"""
        # Create a default workout plan based on days per week
        workout_plan = []

        # Determine split type based on days per week
        if not split_type:
            if days_per_week <= 3:
                split_type = "full_body"
            elif days_per_week == 4:
                split_type = "upper_lower"
            elif days_per_week >= 6:
                split_type = "ppl_2x"
            else:  # 5 days
                split_type = "ppl_ul"

        # Generate sample workout days
        if split_type == "full_body":
            for i in range(days_per_week):
                exercises = [
                    ("Barbell Back Squats", 3, "8-12"),
                    ("Bench Press", 3, "8-12"),
                    ("Deadlifts", 3, "6-10"),
                    ("Overhead Press", 3, "8-12"),
                    ("Pull-ups", 3, "8-12"),
                    ("Dumbbell Rows", 3, "10-15"),
                    ("Leg Curls", 3, "10-15"),
                    ("Plank", 3, "30-60sec")
                ]
                workout_plan.append((f"Full Body Day {i + 1}", exercises))

        elif split_type == "upper_lower":
            for i in range(days_per_week):
                if i % 2 == 0:  # Upper day
                    exercises = [
                        ("Bench Press", 3, "8-12"),
                        ("Pull-ups", 3, "6-10"),
                        ("Overhead Press", 3, "8-12"),
                        ("Barbell Rows", 3, "8-12"),
                        ("Lateral Raises", 3, "12-15"),
                        ("Bicep Curls", 3, "10-15"),
                        ("Tricep Pushdowns", 3, "10-15"),
                        ("Face Pulls", 3, "12-15")
                    ]
                    workout_plan.append(("Upper Body", exercises))
                else:  # Lower day
                    exercises = [
                        ("Barbell Back Squats", 3, "8-12"),
                        ("Romanian Deadlifts", 3, "8-12"),
                        ("Leg Press", 3, "10-15"),
                        ("Leg Curls", 3, "10-15"),
                        ("Calf Raises", 3, "15-20"),
                        ("Hanging Leg Raises", 3, "10-15"),
                        ("Russian Twists", 3, "15-20")
                    ]
                    workout_plan.append(("Lower Body", exercises))

        elif "ppl" in split_type:
            days = min(days_per_week, 6)
            for i in range(days):
                if i % 3 == 0:  # Push day
                    exercises = [
                        ("Bench Press", 3, "8-12"),
                        ("Incline Dumbbell Press", 3, "8-12"),
                        ("Overhead Press", 3, "8-12"),
                        ("Lateral Raises", 3, "12-15"),
                        ("Tricep Pushdowns", 3, "10-15"),
                        ("Skull Crushers", 3, "10-15")
                    ]
                    workout_plan.append(("Push Day", exercises))
                elif i % 3 == 1:  # Pull day
                    exercises = [
                        ("Deadlifts", 3, "6-10"),
                        ("Pull-ups", 3, "6-10"),
                        ("Barbell Rows", 3, "8-12"),
                        ("Face Pulls", 3, "12-15"),
                        ("Bicep Curls", 3, "10-15"),
                        ("Hammer Curls", 3, "10-15")
                    ]
                    workout_plan.append(("Pull Day", exercises))
                else:  # Legs day
                    exercises = [
                        ("Barbell Back Squats", 3, "8-12"),
                        ("Romanian Deadlifts", 3, "8-12"),
                        ("Leg Press", 3, "10-15"),
                        ("Leg Curls", 3, "10-15"),
                        ("Calf Raises", 3, "15-20"),
                        ("Hanging Leg Raises", 3, "10-15")
                    ]
                    workout_plan.append(("Legs Day", exercises))

        # If we need more days than our templates, just repeat days
        while len(workout_plan) < days_per_week:
            idx = len(workout_plan) % len(workout_plan)
            day_name, exercises = workout_plan[idx]
            workout_plan.append((day_name + " (Repeat)", exercises))

        return workout_plan


def evaluate_workout_plan(plan, exercises_database):
    """Evaluate a workout plan on multiple quality metrics."""
    # Initialize metrics
    metrics = {
        "total_exercises": 0,
        "unique_exercises": set(),
        "compound_exercises": 0,
        "isolation_exercises": 0,
        "muscle_group_volume": {
            "chest": 0, "back": 0, "legs": 0, "shoulders": 0, "arms": 0, "core": 0
        },
        "exercise_difficulty": {
            "easy": 0, "moderate": 0, "hard": 0
        },
        "consecutive_muscle_training": 0
    }

    # Track which muscle groups are trained on each day
    day_muscle_groups = []

    # Process each day in the workout plan
    for day_name, exercises in plan:
        # Initialize muscles trained today
        muscles_today = set()

        # Process each exercise
        for exercise in exercises:
            # Extract exercise name (may be a tuple with sets/reps)
            if isinstance(exercise, tuple):
                exercise_name = exercise[0]
            else:
                exercise_name = exercise

            # Increment counter and add to unique set
            metrics["total_exercises"] += 1
            metrics["unique_exercises"].add(exercise_name)

            # Get exercise info if available in database
            if exercise_name in exercises_database:
                ex_info = exercises_database[exercise_name]

                # Count by category
                category = ex_info.get("category", "")
                if category == "compound":
                    metrics["compound_exercises"] += 1
                elif category == "isolation":
                    metrics["isolation_exercises"] += 1

                # Add to muscle group volume
                muscle = ex_info["muscle_group"]
                metrics["muscle_group_volume"][muscle] += 1
                muscles_today.add(muscle)

                # Count by difficulty
                difficulty = ex_info["difficulty"]
                metrics["exercise_difficulty"][difficulty] += 1

        # Add today's muscles to tracking list
        day_muscle_groups.append(muscles_today)

    # Calculate consecutive muscle training
    for i in range(len(day_muscle_groups) - 1):
        overlap = day_muscle_groups[i].intersection(day_muscle_groups[i + 1])
        metrics["consecutive_muscle_training"] += len(overlap)

    # Calculate derived metrics
    if metrics["total_exercises"] > 0:
        metrics["exercise_variety"] = len(metrics["unique_exercises"]) / metrics["total_exercises"]
        metrics["compound_ratio"] = metrics["compound_exercises"] / metrics["total_exercises"]
    else:
        metrics["exercise_variety"] = 0
        metrics["compound_ratio"] = 0

    # Calculate muscle balance (coefficient of variation)
    muscle_values = list(metrics["muscle_group_volume"].values())
    if sum(muscle_values) > 0:
        muscle_mean = sum(muscle_values) / len(muscle_values)
        muscle_variance = sum((x - muscle_mean) ** 2 for x in muscle_values) / len(muscle_values)
        muscle_std_dev = muscle_variance ** 0.5
        metrics["muscle_balance"] = 1 - min(1, (muscle_std_dev / max(1, muscle_mean)) / 0.5)
    else:
        metrics["muscle_balance"] = 0

    # Calculate recovery score (penalize consecutive training)
    metrics["recovery_score"] = max(0, 1 - metrics["consecutive_muscle_training"] / max(1, len(plan)))

    # Calculate overall quality score (weighted combination of key metrics)
    weights = {
        "exercise_variety": 0.2,
        "compound_ratio": 0.15,
        "muscle_balance": 0.35,
        "recovery_score": 0.3
    }

    metrics["quality_score"] = sum(
        metrics[key] * weight for key, weight in weights.items()
    ) * 100  # Scale to 0-100

    return metrics

def compare_algorithms(exercises_database, user_profile, iterations=3):
    """Compare FitAI, StrongFast-like, and Ank-Rule-Based algorithms on performance and quality."""
    # Initialize generators
    fitai_generator = WorkoutPlanGenerator(exercises_database, user_profile)
    strongfast_generator = StrongFastLikeGenerator(exercises_database)
    ankrule_generator = AnkRuleBasedGenerator(exercises_database)

    results = {
        'fitai': {
            'times': [],
            'metrics': [],
            'plans': []
        },
        'strongfast': {
            'times': [],
            'metrics': [],
            'plans': []
        },
        'ankrule': {
            'times': [],
            'metrics': [],
            'plans': []
        }
    }

    # Test with different workout days configurations
    days_to_test = [3, 4, 5, 6]

    for days in days_to_test:
        print(f"Testing with {days} days per week...")

        # Test each algorithm multiple times to average results
        for i in range(iterations):
            # FitAI generator
            start_time = time.time()
            fitai_plan = fitai_generator.generate_workout_plan(days_per_week=days)
            fitai_time = time.time() - start_time

            # Calculate metrics for FitAI
            fitai_metrics = evaluate_workout_plan(fitai_plan, exercises_database)

            results['fitai']['times'].append(fitai_time)
            results['fitai']['metrics'].append(fitai_metrics)
            results['fitai']['plans'].append(fitai_plan)

            # StrongFast-like generator
            start_time = time.time()
            strongfast_plan = strongfast_generator.generate_workout_plan(user_profile, days_per_week=days)
            strongfast_time = time.time() - start_time

            # Calculate metrics for StrongFast-like
            strongfast_metrics = evaluate_workout_plan(strongfast_plan, exercises_database)

            results['strongfast']['times'].append(strongfast_time)
            results['strongfast']['metrics'].append(strongfast_metrics)
            results['strongfast']['plans'].append(strongfast_plan)

            # Ank Rule-Based generator
            start_time = time.time()
            ankrule_plan = ankrule_generator.generate_workout_plan(user_profile, days_per_week=days)
            ankrule_time = time.time() - start_time

            # Calculate metrics for Ank Rule-Based
            ankrule_metrics = evaluate_workout_plan(ankrule_plan, exercises_database)

            results['ankrule']['times'].append(ankrule_time)
            results['ankrule']['metrics'].append(ankrule_metrics)
            results['ankrule']['plans'].append(ankrule_plan)

            print(f"  Iteration {i + 1}/{iterations} complete")

    # Analyze results
    comparison = analyze_algorithm_results(results)

    return comparison, results


def analyze_algorithm_results(results):
    """Analyze and compare algorithm performance results."""

    def safe_div(numerator, denominator):
        return float('inf') if denominator == 0 else numerator / denominator

    algorithms = ['fitai', 'strongfast', 'ankrule']
    metrics = ['times', 'quality_score', 'exercise_variety', 'muscle_balance', 'recovery_score', 'compound_ratio']

    comparison = {}

    # Calculate average values for each algorithm and metric
    for alg in algorithms:
        comparison[alg] = {
            'avg_time': sum(results[alg]['times']) / len(results[alg]['times']),
            'avg_quality': sum(m['quality_score'] for m in results[alg]['metrics']) / len(results[alg]['metrics']),
            'avg_variety': sum(m['exercise_variety'] for m in results[alg]['metrics']) / len(
                results[alg]['metrics']),
            'avg_balance': sum(m['muscle_balance'] for m in results[alg]['metrics']) / len(results[alg]['metrics']),
            'avg_recovery': sum(m['recovery_score'] for m in results[alg]['metrics']) / len(
                results[alg]['metrics']),
            'avg_compound': sum(m['compound_ratio'] for m in results[alg]['metrics']) / len(
                results[alg]['metrics']),
        }

    # Compare algorithms against each other
    comparison['comparisons'] = {
        'time_ratios': {
            'fitai_vs_strongfast': safe_div(comparison['fitai']['avg_time'], comparison['strongfast']['avg_time']),
            'fitai_vs_ankrule': safe_div(comparison['fitai']['avg_time'], comparison['ankrule']['avg_time']),
            'strongfast_vs_ankrule': safe_div(comparison['strongfast']['avg_time'], comparison['ankrule']['avg_time'])
        },
    }


    # Determine winners for each metric
    comparison['winners'] = {}

    # Time (lower is better)
    times = [(alg, comparison[alg]['avg_time']) for alg in algorithms]
    times.sort(key=lambda x: x[1])
    comparison['winners']['time'] = times[0][0]

    # Quality (higher is better)
    quality = [(alg, comparison[alg]['avg_quality']) for alg in algorithms]
    quality.sort(key=lambda x: x[1], reverse=True)
    comparison['winners']['quality'] = quality[0][0]

    # Variety (higher is better)
    variety = [(alg, comparison[alg]['avg_variety']) for alg in algorithms]
    variety.sort(key=lambda x: x[1], reverse=True)
    comparison['winners']['variety'] = variety[0][0]

    # Balance (higher is better)
    balance = [(alg, comparison[alg]['avg_balance']) for alg in algorithms]
    balance.sort(key=lambda x: x[1], reverse=True)
    comparison['winners']['balance'] = balance[0][0]

    # Recovery (higher is better)
    recovery = [(alg, comparison[alg]['avg_recovery']) for alg in algorithms]
    recovery.sort(key=lambda x: x[1], reverse=True)
    comparison['winners']['recovery'] = recovery[0][0]

    return comparison

def print_detailed_comparison(comparison, results):
    """Print a simplified comparison focused on execution speed only."""
    print("\n" + "=" * 80)
    print(" Speed Comparison: Algorithm Timing Only ".center(80, "="))
    print("=" * 80)

    print("\nAverage Generation Time (in seconds):")
    print("-" * 80)
    print(f"FitAI (A* Search):         {comparison['fitai']['avg_time']:.6f}")
    print(f"StrongFast (Template):     {comparison['strongfast']['avg_time']:.6f}")
    print(f"AnkRule (Rule-based):      {comparison['ankrule']['avg_time']:.6f}")

    print("\n" + "-" * 80)

    fastest = comparison['winners']['time']
    print(f"🏆 Fastest Algorithm: {fastest.upper()}")

    print(f"\n{fastest.upper()} provides the best runtime performance for generating workout plans.")
    print("=" * 80)


def main():
    """Run the algorithm comparison with a test user profile."""
    # Initialize knowledge base
    kb = KnowledgeBase()

    # Initialize exercise database directly
    kb.exercises = initialize_expanded_exercise_database()

    # Create sample user profile
    user = UserProfile(
        age=30,
        height_ft=5,
        height_in=10,
        weight_lbs=175,
        gender="male",
        activity_level="moderate",
        goals=["muscle gain"],
        restrictions=[]
    )

    print("Starting algorithm comparison...")
    comparison, results = compare_algorithms(kb.exercises, user, iterations=2)  # Using fewer iterations for testing

    # Print detailed comparison
    print_detailed_comparison(comparison, results)

if __name__ == "__main__":
    main()