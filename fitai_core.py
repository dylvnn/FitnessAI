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


class KnowledgeBase:
    def __init__(self):
        # Initialize with food database and exercise database
        self.foods = {}  # Will populate with nutritional data
        self.exercises = {}  # Will populate with exercise data


class MealPlanCSP:
    """Advanced meal planning with more diverse options and better structure"""

    def __init__(self, foods, user_profile):
        self.foods = foods
        self.user = user_profile
        self.constraints = self._generate_constraints()

    def _generate_constraints(self):
        """Generate constraints based on user profile"""
        weight_kg = self.user.get_weight_kg()

        constraints = {
            'calories': {
                'min': 0.9 * self.user.calculate_tdee(),
                'max': 1.1 * self.user.calculate_tdee()
            },
            'protein': {
                'min': 0.8 * weight_kg,  # 0.8g per kg body weight
                'max': 2.5 * weight_kg  # 2.5g per kg body weight
            },
            'carbs': {
                'min': 2.0 * weight_kg,  # 2g per kg body weight
                'max': 6.0 * weight_kg  # 6g per kg body weight
            },
            'fat': {
                'min': 0.5 * weight_kg,  # 0.5g per kg body weight
                'max': 1.5 * weight_kg  # 1.5g per kg body weight
            },
            'restrictions': self.user.restrictions
        }

        # Adjust macro constraints based on goals
        if 'weight loss' in self.user.goals:
            constraints['calories']['max'] = 0.8 * self.user.calculate_tdee()
            # Lower carbs for weight loss
            constraints['carbs']['max'] = 3.0 * weight_kg
            constraints['protein']['min'] = 1.6 * weight_kg  # Higher protein for satiety
        elif 'muscle gain' in self.user.goals:
            constraints['calories']['min'] = 1.1 * self.user.calculate_tdee()
            constraints['protein']['min'] = 1.8 * weight_kg
            constraints['carbs']['min'] = 4.0 * weight_kg  # Higher carbs for energy

        return constraints

    def generate_meal_plan(self, meals_per_day=4):
        """Generate a meal plan that satisfies all constraints"""
        meal_plan = []

        # Get total daily targets
        daily_calories = self.constraints['calories']['max'] * 0.95  # Aim for 95% of max
        daily_protein = self.constraints['protein']['min'] * 1.1  # Aim for 110% of min
        daily_carbs = self.constraints['carbs']['min'] * 1.1  # Aim for 110% of min
        daily_fat = self.constraints['fat']['min'] * 1.1  # Aim for 110% of min

        # Define meal names for better organization
        if meals_per_day == 3:
            meal_names = ["Breakfast", "Lunch", "Dinner"]
            meal_distribution = {
                "calories": [0.25, 0.35, 0.4],
                "protein": [0.25, 0.35, 0.4],
                "carbs": [0.3, 0.4, 0.3],
                "fat": [0.25, 0.35, 0.4]
            }
        elif meals_per_day == 4:
            meal_names = ["Breakfast", "Lunch", "Snack", "Dinner"]
            meal_distribution = {
                "calories": [0.25, 0.3, 0.15, 0.3],
                "protein": [0.2, 0.3, 0.15, 0.35],
                "carbs": [0.3, 0.3, 0.15, 0.25],
                "fat": [0.25, 0.3, 0.15, 0.3]
            }
        elif meals_per_day == 5:
            meal_names = ["Breakfast", "Morning Snack", "Lunch", "Afternoon Snack", "Dinner"]
            meal_distribution = {
                "calories": [0.2, 0.1, 0.3, 0.1, 0.3],
                "protein": [0.2, 0.1, 0.3, 0.1, 0.3],
                "carbs": [0.25, 0.1, 0.3, 0.1, 0.25],
                "fat": [0.2, 0.1, 0.3, 0.1, 0.3]
            }
        elif meals_per_day == 6:
            meal_names = ["Breakfast", "Morning Snack", "Lunch", "Afternoon Snack", "Dinner", "Evening Snack"]
            meal_distribution = {
                "calories": [0.2, 0.1, 0.25, 0.1, 0.25, 0.1],
                "protein": [0.2, 0.1, 0.25, 0.1, 0.25, 0.1],
                "carbs": [0.25, 0.1, 0.25, 0.1, 0.25, 0.05],
                "fat": [0.2, 0.1, 0.25, 0.1, 0.25, 0.1]
            }
        else:
            # Default to 3 meals
            meal_names = ["Breakfast", "Lunch", "Dinner"]
            meal_distribution = {
                "calories": [0.25, 0.35, 0.4],
                "protein": [0.25, 0.35, 0.4],
                "carbs": [0.3, 0.4, 0.3],
                "fat": [0.25, 0.35, 0.4]
            }

        # Create meal templates based on meal type
        meal_templates = {
            "Breakfast": {
                "proteins": ["Egg", "Egg Whites", "Greek Yogurt", "Protein Shake", "Cottage Cheese"],
                "carbs": ["Oatmeal", "Ezekiel Bread", "Whole Wheat Bread", "Banana", "Sweet Potato", "Blueberries"],
                "fats": ["Avocado", "Peanut Butter", "Almond Butter", "Chia Seeds", "Flax Seeds"],
                "veggies": ["Spinach", "Tomato", "Bell Pepper", "Mushrooms"],
                "exclude": ["Salmon", "Chicken Breast", "Tuna", "Tilapia", "Beef"]
            },
            "Lunch": {
                "proteins": ["Chicken Breast", "Tuna", "Turkey Breast", "Tofu", "Salmon", "Lean Beef", "Greek Yogurt"],
                "carbs": ["Brown Rice", "Sweet Potato", "Quinoa", "Whole Wheat Bread", "Ezekiel Bread"],
                "fats": ["Avocado", "Olive Oil", "Almonds", "Feta Cheese"],
                "veggies": ["Mixed Greens", "Broccoli", "Spinach", "Cucumber", "Tomato", "Bell Pepper"],
                "exclude": []
            },
            "Dinner": {
                "proteins": ["Salmon", "Chicken Breast", "Lean Beef", "Shrimp", "Tilapia", "Turkey Breast", "Cod"],
                "carbs": ["Sweet Potato", "Brown Rice", "Quinoa", "Jasmine Rice"],
                "fats": ["Avocado", "Olive Oil", "Almonds"],
                "veggies": ["Broccoli", "Asparagus", "Brussels Sprouts", "Zucchini", "Cauliflower", "Green Beans"],
                "exclude": ["Oatmeal"]
            },
            "Snack": {
                "proteins": ["Greek Yogurt", "Protein Shake", "Cottage Cheese", "Protein Bar"],
                "carbs": ["Banana", "Apple", "Orange", "Blueberries", "Strawberries", "Rice Cakes"],
                "fats": ["Almonds", "Peanut Butter", "Almond Butter", "Trail Mix"],
                "veggies": ["Carrot", "Cucumber", "Bell Pepper"],
                "exclude": ["Salmon", "Chicken Breast", "Beef"]
            },
            "Morning Snack": {
                "proteins": ["Greek Yogurt", "Protein Shake", "Cottage Cheese", "Protein Bar"],
                "carbs": ["Banana", "Apple", "Orange", "Blueberries", "Rice Cakes"],
                "fats": ["Almonds", "Peanut Butter", "Almond Butter", "Trail Mix"],
                "veggies": ["Carrot", "Cucumber"],
                "exclude": ["Salmon", "Chicken Breast", "Beef"]
            },
            "Afternoon Snack": {
                "proteins": ["Greek Yogurt", "Protein Shake", "Cottage Cheese", "Protein Bar"],
                "carbs": ["Banana", "Apple", "Orange", "Blueberries", "Rice Cakes"],
                "fats": ["Almonds", "Peanut Butter", "Almond Butter", "Trail Mix"],
                "veggies": ["Carrot", "Cucumber", "Bell Pepper"],
                "exclude": ["Salmon", "Chicken Breast", "Beef"]
            },
            "Evening Snack": {
                "proteins": ["Greek Yogurt", "Cottage Cheese", "Protein Shake"],
                "carbs": ["Banana", "Blueberries", "Strawberries", "Rice Cakes"],
                "fats": ["Almonds", "Peanut Butter", "Almond Butter"],
                "veggies": ["Carrot", "Cucumber"],
                "exclude": ["Salmon", "Chicken Breast", "Beef"]
            }
        }

        # For each meal, find foods that approximately match the targets
        for i in range(meals_per_day):
            meal_name = meal_names[i if i < len(meal_names) else -1]

            # Calculate target macros for this meal
            meal_calories = daily_calories * meal_distribution["calories"][
                i if i < len(meal_distribution["calories"]) else -1]
            meal_protein = daily_protein * meal_distribution["protein"][
                i if i < len(meal_distribution["protein"]) else -1]
            meal_carbs = daily_carbs * meal_distribution["carbs"][i if i < len(meal_distribution["carbs"]) else -1]
            meal_fat = daily_fat * meal_distribution["fat"][i if i < len(meal_distribution["fat"]) else -1]

            # Use the corresponding template
            template = meal_templates.get(meal_name, {})
            meal = self._select_foods_for_meal(
                meal_calories, meal_protein, meal_carbs, meal_fat,
                meal_name, template
            )
            meal_plan.append((meal_name, meal))

        return meal_plan

    def _select_foods_for_meal(self, target_calories, target_protein, target_carbs, target_fat, meal_type,
                               template=None):
        """Select a combination of foods that meet the targets with better variety"""
        import random
        selected_foods = []

        # Track current macros
        current_calories = 0
        current_protein = 0
        current_carbs = 0
        current_fat = 0

        # Create available foods dictionary with filtering by restrictions
        available_foods = self._filter_available_foods(template)

        # Categorize foods
        protein_sources = []
        carb_sources = []
        fat_sources = []
        veggie_sources = []
        fruit_sources = []

        # Categorize foods based on their dominant macro
        for food_name, nutrition in available_foods.items():
            # Skip foods that are excluded for this meal type
            if template and "exclude" in template and food_name in template.get("exclude", []):
                continue

            # Protein-dominant foods
            protein_per_calorie = nutrition['protein'] / max(nutrition['calories'], 1)
            if protein_per_calorie >= 0.1 and "Protein" in food_name or "Egg" in food_name or "Chicken" in food_name or "Fish" in food_name or "Turkey" in food_name or "Tofu" in food_name or "Beef" in food_name or "Cottage" in food_name or "Greek" in food_name:
                protein_sources.append((food_name, nutrition))

            # Carb-dominant foods
            carb_per_calorie = nutrition['carbs'] / max(nutrition['calories'], 1)
            if carb_per_calorie >= 0.15 and "Rice" in food_name or "Potato" in food_name or "Bread" in food_name or "Oatmeal" in food_name or "Quinoa" in food_name:
                carb_sources.append((food_name, nutrition))

            # Fat-dominant foods
            fat_per_calorie = nutrition['fat'] / max(nutrition['calories'], 1)
            if fat_per_calorie >= 0.1 and "Oil" in food_name or "Butter" in food_name or "Avocado" in food_name or "Seeds" in food_name or "Almonds" in food_name or "Nuts" in food_name:
                fat_sources.append((food_name, nutrition))

            # Vegetables
            if "Broccoli" in food_name or "Spinach" in food_name or "Greens" in food_name or "Asparagus" in food_name or "Cucumber" in food_name or "Carrot" in food_name or "Pepper" in food_name or "Zucchini" in food_name or "Cauliflower" in food_name or "Brussels" in food_name or "Tomato" in food_name or "Mushrooms" in food_name or "Green Beans" in food_name or "Kale" in food_name:
                veggie_sources.append((food_name, nutrition))

            # Fruits
            if "Banana" in food_name or "Apple" in food_name or "Orange" in food_name or "Strawberries" in food_name or "Blueberries" in food_name or "Grapes" in food_name or "Pineapple" in food_name or "Mango" in food_name or "Watermelon" in food_name or "Kiwi" in food_name:
                fruit_sources.append((food_name, nutrition))

        # Prioritize template-preferred foods
        preferred_proteins = []
        preferred_carbs = []
        preferred_fats = []
        preferred_veggies = []

        if template:
            # Filter preferred protein sources
            if "proteins" in template:
                preferred_proteins = [(f, n) for f, n in protein_sources if f in template["proteins"]]

            # Filter preferred carb sources
            if "carbs" in template:
                preferred_carbs = [(f, n) for f, n in carb_sources if f in template["carbs"]]

            # Filter preferred fat sources
            if "fats" in template:
                preferred_fats = [(f, n) for f, n in fat_sources if f in template["fats"]]

            # Filter preferred veggie sources
            if "veggies" in template:
                preferred_veggies = [(f, n) for f, n in veggie_sources if f in template["veggies"]]

        # If no preferred foods found, use the original lists
        if not preferred_proteins and protein_sources:
            preferred_proteins = protein_sources

        if not preferred_carbs and carb_sources:
            preferred_carbs = carb_sources

        if not preferred_fats and fat_sources:
            preferred_fats = fat_sources

        if not preferred_veggies and veggie_sources:
            preferred_veggies = veggie_sources

        # Build the meal based on type
        max_foods_per_meal = 5
        if meal_type == "Breakfast":
            # Add 1 protein source
            if preferred_proteins:
                protein_food, nutrition = random.choice(preferred_proteins)
                selected_foods.append(protein_food)
                current_calories += nutrition['calories']
                current_protein += nutrition['protein']
                current_carbs += nutrition['carbs']
                current_fat += nutrition['fat']

            # Add 1 carb source
            if preferred_carbs and len(selected_foods) < max_foods_per_meal:
                carb_food, nutrition = random.choice(preferred_carbs)
                selected_foods.append(carb_food)
                current_calories += nutrition['calories']
                current_protein += nutrition['protein']
                current_carbs += nutrition['carbs']
                current_fat += nutrition['fat']

            # Add 1 fat source
            if preferred_fats and len(selected_foods) < max_foods_per_meal:
                fat_food, nutrition = random.choice(preferred_fats)
                selected_foods.append(fat_food)
                current_calories += nutrition['calories']
                current_protein += nutrition['protein']
                current_carbs += nutrition['carbs']
                current_fat += nutrition['fat']

            # Add fruits or veggies
            if fruit_sources and len(selected_foods) < max_foods_per_meal:
                fruit_food, nutrition = random.choice(fruit_sources)
                selected_foods.append(fruit_food)
                current_calories += nutrition['calories']
                current_protein += nutrition['protein']
                current_carbs += nutrition['carbs']
                current_fat += nutrition['fat']

        elif meal_type == "Lunch" or meal_type == "Dinner":
            # Add 1-2 protein sources
            if preferred_proteins and len(selected_foods) < max_foods_per_meal:
                protein_food, nutrition = random.choice(preferred_proteins)
                selected_foods.append(protein_food)
                current_calories += nutrition['calories']
                current_protein += nutrition['protein']
                current_carbs += nutrition['carbs']
                current_fat += nutrition['fat']

            # Add 1 carb source
            if preferred_carbs and len(selected_foods) < max_foods_per_meal:
                carb_food, nutrition = random.choice(preferred_carbs)
                selected_foods.append(carb_food)
                current_calories += nutrition['calories']
                current_protein += nutrition['protein']
                current_carbs += nutrition['carbs']
                current_fat += nutrition['fat']

            # Add 1-2 vegetable sources
            veggie_count = min(2, len(preferred_veggies), max_foods_per_meal - len(selected_foods))
            random.shuffle(preferred_veggies)
            for i in range(veggie_count):
                if i < len(preferred_veggies):
                    veggie_food, nutrition = preferred_veggies[i]
                    selected_foods.append(veggie_food)
                    current_calories += nutrition['calories']
                    current_protein += nutrition['protein']
                    current_carbs += nutrition['carbs']
                    current_fat += nutrition['fat']

            # Add 1 fat source
            if preferred_fats and len(selected_foods) < max_foods_per_meal:
                fat_food, nutrition = random.choice(preferred_fats)
                selected_foods.append(fat_food)
                current_calories += nutrition['calories']
                current_protein += nutrition['protein']
                current_carbs += nutrition['carbs']
                current_fat += nutrition['fat']

        elif "Snack" in meal_type:
            # Snacks should be simpler - just 2-3 items

            # Add 1 protein
            if preferred_proteins and len(selected_foods) < 3:
                protein_food, nutrition = random.choice(preferred_proteins)
                selected_foods.append(protein_food)
                current_calories += nutrition['calories']
                current_protein += nutrition['protein']
                current_carbs += nutrition['carbs']
                current_fat += nutrition['fat']

            # Add either fruit or carb
            if random.choice([True, False]) and fruit_sources and len(selected_foods) < 3:
                fruit_food, nutrition = random.choice(fruit_sources)
                selected_foods.append(fruit_food)
                current_calories += nutrition['calories']
                current_protein += nutrition['protein']
                current_carbs += nutrition['carbs']
                current_fat += nutrition['fat']
            elif preferred_carbs and len(selected_foods) < 3:
                carb_food, nutrition = random.choice(preferred_carbs)
                selected_foods.append(carb_food)
                current_calories += nutrition['calories']
                current_protein += nutrition['protein']
                current_carbs += nutrition['carbs']
                current_fat += nutrition['fat']

            # Maybe add a fat source
            if preferred_fats and len(selected_foods) < 3:
                fat_food, nutrition = random.choice(preferred_fats)
                selected_foods.append(fat_food)
                current_calories += nutrition['calories']
                current_protein += nutrition['protein']
                current_carbs += nutrition['carbs']
                current_fat += nutrition['fat']

        # If we're still significantly below our targets and have space for more foods
        # Try to add one more item that gets us closer to target macros
        if len(selected_foods) < max_foods_per_meal:
            # Determine which macro we need most
            protein_deficit = target_protein - current_protein
            carb_deficit = target_carbs - current_carbs
            fat_deficit = target_fat - current_fat

            max_deficit = max(protein_deficit, carb_deficit, fat_deficit)

            if max_deficit == protein_deficit and protein_deficit > 0 and preferred_proteins:
                protein_food, nutrition = random.choice(preferred_proteins)
                if protein_food not in selected_foods:
                    selected_foods.append(protein_food)
                    current_calories += nutrition['calories']
                    current_protein += nutrition['protein']
                    current_carbs += nutrition['carbs']
                    current_fat += nutrition['fat']
            elif max_deficit == carb_deficit and carb_deficit > 0 and preferred_carbs:
                carb_food, nutrition = random.choice(preferred_carbs)
                if carb_food not in selected_foods:
                    selected_foods.append(carb_food)
                    current_calories += nutrition['calories']
                    current_protein += nutrition['protein']
                    current_carbs += nutrition['carbs']
                    current_fat += nutrition['fat']
            elif max_deficit == fat_deficit and fat_deficit > 0 and preferred_fats:
                fat_food, nutrition = random.choice(preferred_fats)
                if fat_food not in selected_foods:
                    selected_foods.append(fat_food)
                    current_calories += nutrition['calories']
                    current_protein += nutrition['protein']
                    current_carbs += nutrition['carbs']
                    current_fat += nutrition['fat']

        return selected_foods

    def _filter_available_foods(self, template=None):
        """Filter available foods based on dietary restrictions"""
        available_foods = {}

        for food_name, nutrition in self.foods.items():
            # Skip foods that are excluded for this meal type
            if template and "exclude" in template and food_name in template.get("exclude", []):
                continue

            # Check dietary restrictions
            should_exclude = False

            # Define food categories for restrictions
            dairy_foods = ["Milk", "Cheese", "Greek Yogurt", "Cottage Cheese", "Feta Cheese",
                           "Mozzarella", "Cheddar", "Butter", "Yogurt"]
            meat_foods = ["Chicken", "Salmon", "Beef", "Turkey", "Tuna", "Tilapia", "Shrimp",
                          "Pork", "Cod", "Ground Turkey"]
            nut_foods = ["Almonds", "Peanut Butter", "Almond Butter", "Walnuts", "Trail Mix"]
            gluten_foods = ["Wheat", "Bread", "Pasta", "Flour Tortilla", "Ezekiel Bread",
                            "Whole Wheat"]

            # Apply appropriate restrictions
            for restriction in self.constraints['restrictions']:
                if restriction.lower() == "vegetarian":
                    if any(meat in food_name for meat in meat_foods):
                        should_exclude = True
                elif restriction.lower() == "vegan":
                    if any(meat in food_name for meat in meat_foods) or any(
                            dairy in food_name for dairy in dairy_foods):
                        should_exclude = True
                elif restriction.lower() == "dairy":
                    if any(dairy in food_name for dairy in dairy_foods):
                        should_exclude = True
                elif restriction.lower() == "nuts":
                    if any(nut in food_name for nut in nut_foods):
                        should_exclude = True
                elif restriction.lower() == "gluten":
                    if any(gluten in food_name for gluten in gluten_foods):
                        should_exclude = True

            # Only add foods that don't violate any restrictions
            if not should_exclude:
                available_foods[food_name] = nutrition

        return available_foods


class WorkoutPlanGenerator:
    """Generate workout plans using optimal split approaches"""

    def __init__(self, exercises, user_profile):
        self.exercises = exercises
        self.user = user_profile

    def generate_workout_plan(self, days_per_week=6):
        """Generate a weekly workout plan using a structured approach"""
        workout_plan = []

        # Use an appropriate split based on days per week
        if days_per_week == 6:
            # PPL (Push/Pull/Legs) split twice per week
            split = [
                ("Push Day 1", self._create_push_workout(intensity="heavy")),
                ("Pull Day 1", self._create_pull_workout(intensity="heavy")),
                ("Legs Day 1", self._create_legs_workout(intensity="heavy")),
                ("Push Day 2", self._create_push_workout(intensity="moderate")),
                ("Pull Day 2", self._create_pull_workout(intensity="moderate")),
                ("Legs Day 2", self._create_legs_workout(intensity="moderate"))
            ]
        elif days_per_week == 5:
            # Upper/Lower + PPL hybrid
            split = [
                ("Upper Power", self._create_upper_workout(focus="power")),
                ("Lower Power", self._create_legs_workout(intensity="heavy")),
                ("Push Hypertrophy", self._create_push_workout(intensity="moderate")),
                ("Pull Hypertrophy", self._create_pull_workout(intensity="moderate")),
                ("Lower Hypertrophy", self._create_legs_workout(intensity="moderate"))
            ]
        elif days_per_week == 4:
            # Upper/Lower split twice per week
            split = [
                ("Upper Day 1", self._create_upper_workout(focus="strength")),
                ("Lower Day 1", self._create_legs_workout(intensity="heavy")),
                ("Upper Day 2", self._create_upper_workout(focus="hypertrophy")),
                ("Lower Day 2", self._create_legs_workout(intensity="moderate"))
            ]
        elif days_per_week == 3:
            # Full body 3 days per week
            split = [
                ("Full Body A", self._create_full_body_workout(focus="push")),
                ("Full Body B", self._create_full_body_workout(focus="pull")),
                ("Full Body C", self._create_full_body_workout(focus="legs"))
            ]
        else:
            # For any other number of days, create custom split
            muscle_groups = ['chest', 'back', 'legs', 'shoulders', 'arms', 'core']
            split = []

            for i in range(days_per_week):
                if i % 6 == 0:
                    split.append((f"Chest Focus Day", self._create_chest_focused_workout()))
                elif i % 6 == 1:
                    split.append((f"Back Focus Day", self._create_back_focused_workout()))
                elif i % 6 == 2:
                    split.append((f"Legs Focus Day", self._create_legs_workout(intensity="heavy")))
                elif i % 6 == 3:
                    split.append((f"Shoulders Focus Day", self._create_shoulder_focused_workout()))
                elif i % 6 == 4:
                    split.append((f"Arms Focus Day", self._create_arms_focused_workout()))
                else:
                    split.append((f"Core & Cardio Day", self._create_core_focused_workout()))

        # Take only as many days as requested
        workout_plan = split[:days_per_week]
        return workout_plan

    def _create_push_workout(self, intensity="moderate"):
        """Create a push workout (chest, shoulders, triceps)"""
        workout = []

        # Select compound chest exercises
        chest_compounds = self._filter_exercises("chest", "compound")
        chest_isolations = self._filter_exercises("chest", "isolation")

        # Select shoulder exercises
        shoulder_compounds = self._filter_exercises("shoulders", "compound")
        shoulder_isolations = self._filter_exercises("shoulders", "isolation")

        # Select tricep exercises
        tricep_compounds = self._filter_exercises("arms", "compound", lambda x: "Tricep" in x or "Close-Grip" in x)
        tricep_isolations = self._filter_exercises("arms", "isolation", lambda
            x: "Tricep" in x or "Skull" in x or "Pushdown" in x or "Extension" in x)

        # Adjust rep ranges based on intensity
        heavy_rep_range = "5-8"
        moderate_rep_range = "8-12"
        light_rep_range = "12-15"

        # Build the workout
        if intensity == "heavy":
            # Add 2 compound chest exercises
            workout.extend(self._pick_exercises(chest_compounds, 2, heavy_rep_range))
            # Add 1 compound shoulder exercise
            workout.extend(self._pick_exercises(shoulder_compounds, 1, heavy_rep_range))
            # Add 1 isolation shoulder exercise
            workout.extend(self._pick_exercises(shoulder_isolations, 1, moderate_rep_range))
            # Add 2 tricep exercises (mix of compound and isolation)
            workout.extend(self._pick_exercises(tricep_compounds, 1, moderate_rep_range))
            workout.extend(self._pick_exercises(tricep_isolations, 1, moderate_rep_range))
        else:
            # Add 1 compound chest exercise
            workout.extend(self._pick_exercises(chest_compounds, 1, moderate_rep_range))
            # Add 1-2 isolation chest exercises
            workout.extend(self._pick_exercises(chest_isolations, 2, moderate_rep_range))
            # Add 1-2 shoulder exercises (prioritize isolation)
            workout.extend(self._pick_exercises(shoulder_compounds, 1, moderate_rep_range))
            workout.extend(self._pick_exercises(shoulder_isolations, 1, light_rep_range))
            # Add 2 tricep isolation exercises
            workout.extend(self._pick_exercises(tricep_isolations, 2, light_rep_range))

        return workout

    def _create_pull_workout(self, intensity="moderate"):
        """Create a pull workout (back, biceps, rear delts)"""
        workout = []

        # Select back exercises
        back_compounds = self._filter_exercises("back", "compound")
        back_isolations = self._filter_exercises("back", "isolation")

        # Select bicep exercises
        bicep_isolations = self._filter_exercises("arms", "isolation", lambda x: "Curl" in x)

        # Select rear delt exercises
        rear_delt_exercises = self._filter_exercises("shoulders", "isolation",
                                                     lambda x: "Face Pull" in x or "Reverse" in x)

        # Adjust rep ranges based on intensity
        heavy_rep_range = "5-8"
        moderate_rep_range = "8-12"
        light_rep_range = "12-15"

        # Build the workout
        if intensity == "heavy":
            # Add 2-3 compound back exercises
            workout.extend(self._pick_exercises(back_compounds, 3, heavy_rep_range))
            # Add 1 back isolation
            workout.extend(self._pick_exercises(back_isolations, 1, moderate_rep_range))
            # Add 2 bicep exercises
            workout.extend(self._pick_exercises(bicep_isolations, 2, moderate_rep_range))
            # Add 1 rear delt exercise
            workout.extend(self._pick_exercises(rear_delt_exercises, 1, moderate_rep_range))
        else:
            # Add 2 compound back exercises
            workout.extend(self._pick_exercises(back_compounds, 2, moderate_rep_range))
            # Add 1-2 back isolation
            workout.extend(self._pick_exercises(back_isolations, 1, moderate_rep_range))
            # Add 2-3 bicep exercises
            workout.extend(self._pick_exercises(bicep_isolations, 3, light_rep_range))
            # Add 1 rear delt exercise
            workout.extend(self._pick_exercises(rear_delt_exercises, 1, light_rep_range))

        return workout

    def _create_legs_workout(self, intensity="moderate"):
        """Create a legs workout (quads, hamstrings, calves)"""
        workout = []

        # Filter exercises
        quad_compounds = self._filter_exercises("legs", "compound",
                                                lambda x: "Squat" in x or "Leg Press" in x or "Hack" in x)
        ham_compounds = self._filter_exercises("legs", "compound",
                                               lambda x: "Deadlift" in x or "Lunge" in x or "Split" in x)
        leg_isolations = self._filter_exercises("legs", "isolation")
        calf_exercises = self._filter_exercises("legs", "isolation", lambda x: "Calf" in x)
        core_exercises = self._filter_exercises("core", None)

        # Adjust rep ranges based on intensity
        heavy_rep_range = "5-8"
        moderate_rep_range = "8-12"
        light_rep_range = "12-15"

        # Build the workout
        if intensity == "heavy":
            # Add 2 quad compound exercises
            workout.extend(self._pick_exercises(quad_compounds, 2, heavy_rep_range))
            # Add 1 ham compound exercise
            workout.extend(self._pick_exercises(ham_compounds, 1, heavy_rep_range))
            # Add 1 leg isolation
            workout.extend(self._pick_exercises(leg_isolations, 1, moderate_rep_range))
            # Add 1 calf exercise
            workout.extend(self._pick_exercises(calf_exercises, 1, moderate_rep_range))
            # Add 1 core exercise
            workout.extend(self._pick_exercises(core_exercises, 1, moderate_rep_range))
        else:
            # Add 1 quad compound exercise
            workout.extend(self._pick_exercises(quad_compounds, 1, moderate_rep_range))
            # Add 1 ham compound exercise
            workout.extend(self._pick_exercises(ham_compounds, 1, moderate_rep_range))
            # Add 2 leg isolations
            workout.extend(self._pick_exercises(leg_isolations, 2, light_rep_range))
            # Add 2 calf exercises
            workout.extend(self._pick_exercises(calf_exercises, 2, light_rep_range))
            # Add 1 core exercise
            workout.extend(self._pick_exercises(core_exercises, 1, light_rep_range))

        return workout

    def _create_upper_workout(self, focus="strength"):
        """Create an upper body workout (chest, back, shoulders, arms)"""
        workout = []

        # Filter exercises
        chest_compounds = self._filter_exercises("chest", "compound")
        chest_isolations = self._filter_exercises("chest", "isolation")
        back_compounds = self._filter_exercises("back", "compound")
        back_isolations = self._filter_exercises("back", "isolation")
        shoulder_compounds = self._filter_exercises("shoulders", "compound")
        shoulder_isolations = self._filter_exercises("shoulders", "isolation")
        bicep_exercises = self._filter_exercises("arms", "isolation", lambda x: "Curl" in x)
        tricep_exercises = self._filter_exercises("arms", "isolation", lambda x: "Tricep" in x or "Skull" in x)

        # Adjust rep ranges based on focus
        if focus == "power" or focus == "strength":
            chest_rep_range = "4-8"
            back_rep_range = "4-8"
            shoulder_rep_range = "6-10"
            arm_rep_range = "8-12"
        else:
            chest_rep_range = "8-12"
            back_rep_range = "8-12"
            shoulder_rep_range = "10-15"
            arm_rep_range = "12-15"

        # Add 1-2 chest exercises
        workout.extend(self._pick_exercises(chest_compounds, 1, chest_rep_range))
        if focus != "power":
            workout.extend(self._pick_exercises(chest_isolations, 1, chest_rep_range))

        # Add 1-2 back exercises
        workout.extend(self._pick_exercises(back_compounds, 1, back_rep_range))
        if focus != "power":
            workout.extend(self._pick_exercises(back_isolations, 1, back_rep_range))

        # Add 1-2 shoulder exercises
        workout.extend(self._pick_exercises(shoulder_compounds, 1, shoulder_rep_range))
        if focus != "power":
            workout.extend(self._pick_exercises(shoulder_isolations, 1, shoulder_rep_range))

        # Add 1 exercise each for biceps and triceps
        workout.extend(self._pick_exercises(bicep_exercises, 1, arm_rep_range))
        workout.extend(self._pick_exercises(tricep_exercises, 1, arm_rep_range))

        return workout

    def _create_full_body_workout(self, focus="balanced"):
        """Create a full body workout with emphasis on a specific area"""
        workout = []

        # Determine emphasis based on focus
        if focus == "push":
            # Emphasize chest and shoulders
            workout.extend(self._pick_exercises(self._filter_exercises("chest", "compound"), 2, "6-10"))
            workout.extend(self._pick_exercises(self._filter_exercises("shoulders", "compound"), 1, "8-12"))
            # Include less emphasis on pull and legs
            workout.extend(self._pick_exercises(self._filter_exercises("back", "compound"), 1, "8-12"))
            workout.extend(self._pick_exercises(self._filter_exercises("legs", "compound"), 1, "8-12"))
            # Add arm and core work
            workout.extend(
                self._pick_exercises(self._filter_exercises("arms", "isolation", lambda x: "Tricep" in x), 1, "10-15"))
            workout.extend(self._pick_exercises(self._filter_exercises("core", None), 1, "12-15"))
        elif focus == "pull":
            # Emphasize back and biceps
            workout.extend(self._pick_exercises(self._filter_exercises("back", "compound"), 2, "6-10"))
            workout.extend(
                self._pick_exercises(self._filter_exercises("arms", "isolation", lambda x: "Curl" in x), 1, "8-12"))
            # Include less emphasis on push and legs
            workout.extend(self._pick_exercises(self._filter_exercises("chest", "compound"), 1, "8-12"))
            workout.extend(self._pick_exercises(self._filter_exercises("legs", "compound"), 1, "8-12"))
            # Add shoulder and core work
            workout.extend(self._pick_exercises(self._filter_exercises("shoulders", "isolation"), 1, "10-15"))
            workout.extend(self._pick_exercises(self._filter_exercises("core", None), 1, "12-15"))
        elif focus == "legs":
            # Emphasize legs
            workout.extend(self._pick_exercises(self._filter_exercises("legs", "compound"), 3, "6-10"))
            # Include minimal upper body
            workout.extend(self._pick_exercises(self._filter_exercises("chest", "compound"), 1, "8-12"))
            workout.extend(self._pick_exercises(self._filter_exercises("back", "compound"), 1, "8-12"))
            # Add core work
            workout.extend(self._pick_exercises(self._filter_exercises("core", None), 2, "12-15"))
        else:
            # Balanced approach
            workout.extend(self._pick_exercises(self._filter_exercises("chest", "compound"), 1, "8-12"))
            workout.extend(self._pick_exercises(self._filter_exercises("back", "compound"), 1, "8-12"))
            workout.extend(self._pick_exercises(self._filter_exercises("legs", "compound"), 2, "8-12"))
            workout.extend(self._pick_exercises(self._filter_exercises("shoulders", "compound"), 1, "8-12"))
            workout.extend(self._pick_exercises(self._filter_exercises("arms", "isolation"), 1, "10-15"))
            workout.extend(self._pick_exercises(self._filter_exercises("core", None), 1, "12-15"))

        return workout

    def _create_chest_focused_workout(self):
        """Create a chest-focused workout"""
        workout = []

        # Add 2-3 compound chest exercises
        workout.extend(self._pick_exercises(self._filter_exercises("chest", "compound"), 3, "6-12"))

        # Add 2 isolation chest exercises
        workout.extend(self._pick_exercises(self._filter_exercises("chest", "isolation"), 2, "10-15"))

        # Add 1 front delt exercise
        workout.extend(
            self._pick_exercises(self._filter_exercises("shoulders", "isolation", lambda x: "Front" in x), 1, "10-15"))

        # Add 1 tricep exercise
        workout.extend(
            self._pick_exercises(self._filter_exercises("arms", "isolation", lambda x: "Tricep" in x), 1, "10-15"))

        return workout

    def _create_back_focused_workout(self):
        """Create a back-focused workout"""
        workout = []

        # Add 2-3 compound back exercises
        workout.extend(self._pick_exercises(self._filter_exercises("back", "compound"), 3, "6-12"))

        # Add 1-2 isolation back exercises
        workout.extend(self._pick_exercises(self._filter_exercises("back", "isolation"), 1, "10-15"))

        # Add 1 rear delt exercise
        workout.extend(self._pick_exercises(
            self._filter_exercises("shoulders", "isolation", lambda x: "Reverse" in x or "Face" in x), 1, "10-15"))

        # Add 1-2 bicep exercises
        workout.extend(
            self._pick_exercises(self._filter_exercises("arms", "isolation", lambda x: "Curl" in x), 2, "10-15"))

        return workout

    def _create_shoulder_focused_workout(self):
        """Create a shoulder-focused workout"""
        workout = []

        # Add 2 compound shoulder exercises
        workout.extend(self._pick_exercises(self._filter_exercises("shoulders", "compound"), 2, "6-12"))

        # Add 3 isolation shoulder exercises (lateral, front, rear)
        workout.extend(
            self._pick_exercises(self._filter_exercises("shoulders", "isolation", lambda x: "Lateral" in x), 1,
                                 "12-15"))
        workout.extend(
            self._pick_exercises(self._filter_exercises("shoulders", "isolation", lambda x: "Front" in x), 1, "12-15"))
        workout.extend(self._pick_exercises(
            self._filter_exercises("shoulders", "isolation", lambda x: "Reverse" in x or "Face" in x), 1, "12-15"))

        # Add 1 trap exercise
        workout.extend(
            self._pick_exercises(self._filter_exercises("shoulders", "isolation", lambda x: "Shrug" in x), 1, "10-15"))

        # Add 1 tricep exercise
        workout.extend(
            self._pick_exercises(self._filter_exercises("arms", "isolation", lambda x: "Tricep" in x), 1, "10-15"))

        return workout

    def _create_arms_focused_workout(self):
        """Create an arms-focused workout"""
        workout = []

        # Add 3 bicep exercises
        workout.extend(
            self._pick_exercises(self._filter_exercises("arms", "isolation", lambda x: "Curl" in x), 3, "8-15"))

        # Add 3 tricep exercises
        workout.extend(self._pick_exercises(
            self._filter_exercises("arms", "isolation", lambda x: "Tricep" in x or "Skull" in x or "Extension" in x), 3,
            "8-15"))

        # Add 1 compound exercise for each
        workout.extend(
            self._pick_exercises(self._filter_exercises("back", "compound", lambda x: "Chin-up" in x), 1, "8-12"))
        workout.extend(
            self._pick_exercises(self._filter_exercises("arms", "compound", lambda x: "Close-Grip" in x or "Dips" in x),
                                 1, "8-12"))

        return workout

    def _create_core_focused_workout(self):
        """Create a core-focused workout with some cardio"""
        workout = []

        # Add variety of core exercises
        core_exercises = self._filter_exercises("core", None)

        # Add 6-8 core exercises covering different areas
        core_subset = {}

        for name, data in core_exercises.items():
            category = data.get("category", "isolation")
            if category not in core_subset:
                core_subset[name] = data

            if len(core_subset) >= 7:
                break

        # Add all selected core exercises with appropriate rep ranges
        for name, data in core_subset.items():
            rep_range = data.get("rep_range", "15-20")
            workout.append((name, 3, rep_range))

        return workout

    def _filter_exercises(self, muscle_group, category, condition=None):
        """Filter exercises by muscle group, category, and optional condition"""
        filtered = {}

        for name, data in self.exercises.items():
            if data["muscle_group"] == muscle_group:
                if category is None or data.get("category", "isolation") == category:
                    if condition is None or condition(name):
                        filtered[name] = data

        return filtered

    def _pick_exercises(self, exercise_dict, count, rep_range=None):
        """Pick a specified number of exercises from the filtered list"""
        import random
        result = []

        # Make a copy of the exercise dictionary items
        exercises = list(exercise_dict.items())

        # Shuffle to randomize selection
        random.shuffle(exercises)

        # Take only the number requested or all available if less
        selected = exercises[:min(count, len(exercises))]

        # Format the selected exercises with sets and rep ranges
        for name, data in selected:
            # Use provided rep range or one from the exercise data
            reps = rep_range if rep_range else data.get("rep_range", "8-12")
            result.append((name, 3, reps))  # Default to 3 sets

        return result


def _initialize_expanded_food_database(self):
    self.kb.foods = {
        # Proteins - Meat & Fish
        "Chicken Breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
        "Salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 13},
        "Lean Beef": {"calories": 250, "protein": 26, "carbs": 0, "fat": 15},
        "Turkey Breast": {"calories": 135, "protein": 30, "carbs": 0, "fat": 1},
        "Tuna": {"calories": 120, "protein": 25, "carbs": 0, "fat": 1},
        "Tilapia": {"calories": 128, "protein": 26, "carbs": 0, "fat": 2.7},
        "Shrimp": {"calories": 85, "protein": 18, "carbs": 0, "fat": 1.5},
        "Pork Tenderloin": {"calories": 143, "protein": 26, "carbs": 0, "fat": 3.5},
        "Ground Turkey": {"calories": 170, "protein": 21, "carbs": 0, "fat": 9},
        "Cod": {"calories": 90, "protein": 20, "carbs": 0, "fat": 1},

        # Proteins - Vegetarian/Vegan
        "Tofu": {"calories": 76, "protein": 8, "carbs": 2, "fat": 4.5},
        "Tempeh": {"calories": 160, "protein": 16, "carbs": 8, "fat": 9},
        "Seitan": {"calories": 100, "protein": 21, "carbs": 4, "fat": 0.5},
        "Edamame": {"calories": 120, "protein": 12, "carbs": 10, "fat": 5},
        "Lentils": {"calories": 116, "protein": 9, "carbs": 20, "fat": 0.4},
        "Black Beans": {"calories": 114, "protein": 7.6, "carbs": 20, "fat": 0.5},
        "Chickpeas": {"calories": 120, "protein": 6, "carbs": 22, "fat": 2},
        "Quinoa": {"calories": 120, "protein": 4.4, "carbs": 21, "fat": 1.9},
        "Nutritional Yeast": {"calories": 60, "protein": 8, "carbs": 5, "fat": 0.5},
        "Plant-Based Burger": {"calories": 240, "protein": 20, "carbs": 9, "fat": 14},

        # Dairy & Eggs
        "Egg": {"calories": 68, "protein": 5.7, "carbs": 0.6, "fat": 4.8},
        "Egg Whites": {"calories": 17, "protein": 3.6, "carbs": 0.2, "fat": 0},
        "Greek Yogurt": {"calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4},
        "Cottage Cheese": {"calories": 98, "protein": 11, "carbs": 3.4, "fat": 4.3},
        "Feta Cheese": {"calories": 75, "protein": 4, "carbs": 1.2, "fat": 6},
        "Mozzarella": {"calories": 85, "protein": 6.3, "carbs": 0.6, "fat": 6.3},
        "Cheddar Cheese": {"calories": 113, "protein": 7, "carbs": 0.4, "fat": 9.3},
        "Skim Milk": {"calories": 42, "protein": 3.4, "carbs": 5, "fat": 0.1},
        "Whole Milk": {"calories": 61, "protein": 3.2, "carbs": 4.8, "fat": 3.3},
        "Protein Shake": {"calories": 120, "protein": 24, "carbs": 3, "fat": 1},

        # Grains & Starches
        "Brown Rice": {"calories": 112, "protein": 2.6, "carbs": 23, "fat": 0.9},
        "White Rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
        "Jasmine Rice": {"calories": 140, "protein": 3, "carbs": 31, "fat": 0.3},
        "Basmati Rice": {"calories": 121, "protein": 3.5, "carbs": 25, "fat": 0.3},
        "Sweet Potato": {"calories": 86, "protein": 1.6, "carbs": 20, "fat": 0.1},
        "Russet Potato": {"calories": 64, "protein": 1.7, "carbs": 14.5, "fat": 0.1},
        "Oatmeal": {"calories": 68, "protein": 2.5, "carbs": 12, "fat": 1.4},
        "Ezekiel Bread": {"calories": 80, "protein": 4, "carbs": 15, "fat": 0.5},
        "Whole Wheat Bread": {"calories": 69, "protein": 3.6, "carbs": 12, "fat": 1},
        "Whole Wheat Pasta": {"calories": 124, "protein": 5, "carbs": 26, "fat": 0.8},
        "White Pasta": {"calories": 158, "protein": 6, "carbs": 31, "fat": 0.9},
        "Couscous": {"calories": 120, "protein": 4, "carbs": 23, "fat": 0.2},
        "Corn Tortilla": {"calories": 52, "protein": 1.4, "carbs": 10.7, "fat": 0.7},
        "Flour Tortilla": {"calories": 104, "protein": 2.8, "carbs": 17.8, "fat": 3},

        # Vegetables
        "Broccoli": {"calories": 55, "protein": 3.7, "carbs": 11.2, "fat": 0.6},
        "Spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4},
        "Kale": {"calories": 33, "protein": 2.2, "carbs": 6.7, "fat": 0.5},
        "Bell Pepper": {"calories": 31, "protein": 1, "carbs": 6, "fat": 0.3},
        "Carrot": {"calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2},
        "Cucumber": {"calories": 16, "protein": 0.7, "carbs": 3.6, "fat": 0.1},
        "Zucchini": {"calories": 17, "protein": 1.2, "carbs": 3.1, "fat": 0.3},
        "Cauliflower": {"calories": 25, "protein": 2, "carbs": 5, "fat": 0.1},
        "Brussels Sprouts": {"calories": 43, "protein": 3, "carbs": 9, "fat": 0.3},
        "Asparagus": {"calories": 27, "protein": 2.9, "carbs": 5.2, "fat": 0.2},
        "Mixed Greens": {"calories": 15, "protein": 1.5, "carbs": 2.9, "fat": 0.2},
        "Tomato": {"calories": 22, "protein": 1.1, "carbs": 4.8, "fat": 0.2},
        "Mushrooms": {"calories": 22, "protein": 3.1, "carbs": 3.3, "fat": 0.3},
        "Green Beans": {"calories": 34, "protein": 1.8, "carbs": 7.8, "fat": 0.2},

        # Fruits
        "Banana": {"calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3},
        "Apple": {"calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2},
        "Orange": {"calories": 47, "protein": 0.9, "carbs": 12, "fat": 0.1},
        "Strawberries": {"calories": 32, "protein": 0.7, "carbs": 7.7, "fat": 0.3},
        "Blueberries": {"calories": 57, "protein": 0.7, "carbs": 14.5, "fat": 0.3},
        "Grapes": {"calories": 62, "protein": 0.6, "carbs": 16, "fat": 0.3},
        "Pineapple": {"calories": 50, "protein": 0.5, "carbs": 13, "fat": 0.1},
        "Mango": {"calories": 60, "protein": 0.8, "carbs": 15, "fat": 0.4},
        "Watermelon": {"calories": 30, "protein": 0.6, "carbs": 7.6, "fat": 0.2},
        "Kiwi": {"calories": 42, "protein": 0.8, "carbs": 10.1, "fat": 0.4},

        # Fats & Oils
        "Avocado": {"calories": 160, "protein": 2, "carbs": 8, "fat": 15},
        "Olive Oil": {"calories": 119, "protein": 0, "carbs": 0, "fat": 13.5},
        "Coconut Oil": {"calories": 121, "protein": 0, "carbs": 0, "fat": 13.5},
        "Butter": {"calories": 102, "protein": 0.1, "carbs": 0, "fat": 11.5},
        "Peanut Butter": {"calories": 188, "protein": 8, "carbs": 6, "fat": 16},
        "Almond Butter": {"calories": 180, "protein": 7, "carbs": 7, "fat": 16},
        "Almonds": {"calories": 164, "protein": 6, "carbs": 6, "fat": 14},
        "Walnuts": {"calories": 185, "protein": 4.3, "carbs": 3.9, "fat": 18.5},
        "Chia Seeds": {"calories": 58, "protein": 2, "carbs": 4.2, "fat": 3.7},
        "Flax Seeds": {"calories": 55, "protein": 1.9, "carbs": 3, "fat": 4.3},

        # Snacks & Others
        "Protein Bar": {"calories": 200, "protein": 20, "carbs": 20, "fat": 5},
        "Trail Mix": {"calories": 173, "protein": 5, "carbs": 12, "fat": 12},
        "Dark Chocolate": {"calories": 155, "protein": 2, "carbs": 13, "fat": 11},
        "Hummus": {"calories": 70, "protein": 2, "carbs": 4, "fat": 5},
        "Guacamole": {"calories": 100, "protein": 1.5, "carbs": 6, "fat": 9},
        "Rice Cakes": {"calories": 35, "protein": 0.7, "carbs": 7.3, "fat": 0.3},
        "Honey": {"calories": 64, "protein": 0.1, "carbs": 17.3, "fat": 0}
    }


def _initialize_expanded_exercise_database(self):
    self.kb.exercises = {
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