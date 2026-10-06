from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>BMI & Health Planner</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 30px;
            background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        }

        .container {
            max-width: 850px;
            margin: auto;
            background: white;
            padding: 35px;
            border-radius: 18px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }

        h1, h2 {
            text-align: center;
        }

        h1 {
            color: #2e7d32;
        }

        h2 {
            color: #388e3c;
            margin-top: 30px;
        }

        label {
            font-weight: bold;
            display: block;
            margin-top: 15px;
        }

        input, select {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ccc;
            border-radius: 8px;
        }

        .radio-group {
            margin-top: 8px;
        }

        .radio-group input,
        .checkbox-group input {
            width: auto;
            margin-right: 5px;
        }

        .radio-group label,
        .checkbox-group label {
            display: inline-block;
            font-weight: normal;
            margin: 8px 15px 5px 0;
        }

        button {
            width: 100%;
            padding: 14px;
            margin-top: 25px;
            border: none;
            border-radius: 8px;
            background: #2e7d32;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #1b5e20;
        }

        .result {
            margin-top: 30px;
            padding: 20px;
            background: #f1f8e9;
            border-radius: 12px;
            border-left: 6px solid #2e7d32;
        }

        .plan {
            margin-top: 20px;
            padding: 20px;
            background: #fffde7;
            border-radius: 12px;
        }

        .question {
            margin-top: 25px;
            padding: 20px;
            background: #e3f2fd;
            border-radius: 12px;
            text-align: center;
        }

        .yes-no {
            display: flex;
            gap: 15px;
            margin-top: 15px;
        }

        .yes-no form {
            width: 50%;
        }

        .yes-no button {
            margin-top: 0;
        }

        .no-button {
            background: #757575;
        }

        .no-button:hover {
            background: #424242;
        }

        ul {
            line-height: 1.9;
        }

        .info {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
        }

        .back-button {
            background: #546e7a;
            margin-top: 20px;
        }

        .back-button:hover {
            background: #37474f;
        }

        .disclaimer {
            margin-top: 25px;
            padding: 15px;
            background: #fff3e0;
            border-radius: 10px;
            font-size: 14px;
            color: #555;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>🏥 BMI & Health Planner</h1>

    {% if bmi is not defined %}

        <!-- STEP 1: BMI FORM -->

        <form method="POST">

            <input type="hidden" name="step" value="bmi">

            <label>Age</label>

            <input
                type="number"
                name="age"
                min="1"
                max="120"
                required
            >

            <label>Gender</label>

            <select name="gender" required>

                <option value="">
                    Select Gender
                </option>

                <option value="Male">
                    Male
                </option>

                <option value="Female">
                    Female
                </option>

                <option value="Other">
                    Other
                </option>

            </select>

            <label>Height (cm)</label>

            <input
                type="number"
                name="height"
                step="0.1"
                min="1"
                required
            >

            <label>Weight (kg)</label>

            <input
                type="number"
                name="weight"
                step="0.1"
                min="1"
                required
            >

            <button type="submit">
                CALCULATE BMI
            </button>

        </form>

    {% else %}

        <!-- STEP 2: BMI RESULT -->

        <div class="result">

            <h2>Your BMI Result</h2>

            <p>
                <strong>Age:</strong>
                {{ age }}
            </p>

            <p>
                <strong>Gender:</strong>
                {{ gender }}
            </p>

            <p>
                <strong>Your BMI:</strong>
                {{ bmi }}
            </p>

            <p>
                <strong>Category:</strong>
                {{ category }}
            </p>

        </div>


        {% if plan %}

            <!-- STEP 5: PERSONALIZED PLAN -->

            <div class="info">

                <p>
                    <strong>Diet:</strong>
                    {{ diet }}
                </p>

                <p>
                    <strong>Exercise:</strong>
                    {{ exercise_time }} / {{ intensity }}
                </p>

                {% if allergies %}

                    <p>
                        <strong>Allergies:</strong>
                        {{ allergies | join(", ") }}
                    </p>

                {% else %}

                    <p>
                        <strong>Allergies:</strong>
                        None
                    </p>

                {% endif %}

            </div>


            <div class="plan">

                <h2>🌱 Your Personalized Plan</h2>

                <h3>🍎 Diet Suggestions</h3>

                <ul>

                    {% for item in diet_plan %}

                        <li>{{ item }}</li>

                    {% endfor %}

                </ul>


                <h3>🏃 Exercise Suggestions</h3>

                <ul>

                    {% for item in exercise_plan %}

                        <li>{{ item }}</li>

                    {% endfor %}

                </ul>

            </div>


            <div class="disclaimer">

                <strong>Note:</strong>
                This planner provides general health and
                fitness suggestions. It is not a substitute
                for professional medical advice.

            </div>


            <form method="GET">

                <button
                    type="submit"
                    class="back-button"
                >
                    START AGAIN
                </button>

            </form>


        {% elif show_suggestions %}

            <!-- STEP 4: SUGGESTION DETAILS -->

            <h2>🌱 Tell Us About Yourself</h2>

            <form method="POST">

                <input
                    type="hidden"
                    name="step"
                    value="plan"
                >

                <input
                    type="hidden"
                    name="bmi"
                    value="{{ bmi }}"
                >

                <input
                    type="hidden"
                    name="category"
                    value="{{ category }}"
                >

                <input
                    type="hidden"
                    name="age"
                    value="{{ age }}"
                >

                <input
                    type="hidden"
                    name="gender"
                    value="{{ gender }}"
                >


                <label>Diet</label>

                <div class="radio-group">

                    <label>
                        <input
                            type="radio"
                            name="diet"
                            value="Vegetarian"
                            required
                        >
                        Vegetarian
                    </label>


                    <label>
                        <input
                            type="radio"
                            name="diet"
                            value="Non-Vegetarian"
                        >
                        Non-Vegetarian
                    </label>


                    <label>
                        <input
                            type="radio"
                            name="diet"
                            value="Vegan"
                        >
                        Vegan
                    </label>

                </div>


                <label>Allergies</label>

                <div class="checkbox-group">

                    <label>
                        <input
                            type="checkbox"
                            name="allergies"
                            value="Dairy"
                        >
                        Dairy
                    </label>


                    <label>
                        <input
                            type="checkbox"
                            name="allergies"
                            value="Nuts"
                        >
                        Nuts
                    </label>


                    <label>
                        <input
                            type="checkbox"
                            name="allergies"
                            value="Gluten"
                        >
                        Gluten
                    </label>


                    <label>
                        <input
                            type="checkbox"
                            name="allergies"
                            value="Eggs"
                        >
                        Eggs
                    </label>


                    <label>
                        <input
                            type="checkbox"
                            name="allergies"
                            value="Soy"
                        >
                        Soy
                    </label>

                </div>


                <label>Exercise Time</label>

                <select
                    name="exercise_time"
                    required
                >

                    <option value="">
                        Select Exercise Time
                    </option>

                    <option>15–30 min</option>
                    <option>30–45 min</option>
                    <option>45–60 min</option>
                    <option>60+ min</option>

                </select>


                <label>Intensity</label>

                <select
                    name="intensity"
                    required
                >

                    <option value="">
                        Select Intensity
                    </option>

                    <option>Beginner</option>
                    <option>Moderate</option>
                    <option>Hardcore</option>

                </select>


                <button type="submit">
                    SHOW MY PLAN
                </button>

            </form>


        {% else %}

            <!-- STEP 3: YES / NO QUESTION -->

            <div class="question">

                <h2>
                    🌱 Would you like some suggestions?
                </h2>

                <p>
                    We can provide personalized diet and
                    exercise suggestions based on your
                    preferences.
                </p>


                <div class="yes-no">

                    <!-- YES -->

                    <form method="POST">

                        <input
                            type="hidden"
                            name="step"
                            value="suggestions"
                        >

                        <input
                            type="hidden"
                            name="bmi"
                            value="{{ bmi }}"
                        >

                        <input
                            type="hidden"
                            name="category"
                            value="{{ category }}"
                        >

                        <input
                            type="hidden"
                            name="age"
                            value="{{ age }}"
                        >

                        <input
                            type="hidden"
                            name="gender"
                            value="{{ gender }}"
                        >

                        <button type="submit">
                            YES, SHOW ME
                        </button>

                    </form>


                    <!-- NO -->

                    <form method="POST">

                        <input
                            type="hidden"
                            name="step"
                            value="no_suggestions"
                        >

                        <button
                            type="submit"
                            class="no-button"
                        >
                            NO, THANKS
                        </button>

                    </form>

                </div>

            </div>

        {% endif %}

    {% endif %}

</div>

</body>
</html>
"""





def get_bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"




def create_diet_plan(diet, allergies, category):

    plan = []

    if category == "Overweight":

        plan.append(
            "Focus on reasonable portions and limit sugary drinks and highly processed foods."
        )

    elif category == "Underweight":

        plan.append(
            "Include nutritious calorie-dense foods and regular balanced meals."
        )

    elif category == "Obese":

        plan.append(
            "Focus on balanced portions, nutrient-dense foods and gradual lifestyle changes."
        )

    else:

        plan.append(
            "Maintain a balanced diet with vegetables, fruits, whole grains and protein."
        )


    if diet == "Vegetarian":

        breakfast = "Breakfast: Oats with fruits and seeds."

        lunch = (
            "Lunch: Brown rice or roti with dal, "
            "vegetables and salad."
        )

        snack = (
            "Snack: Fresh fruit, roasted chana or sprouts."
        )

        dinner = (
            "Dinner: Vegetable soup with roti "
            "and a protein-rich meal."
        )


    elif diet == "Non-Vegetarian":

        breakfast = (
            "Breakfast: Eggs with whole-grain toast and fruit."
        )

        lunch = (
            "Lunch: Grilled chicken or fish with rice, "
            "vegetables and salad."
        )

        snack = "Snack: Fresh fruit or yogurt."

        dinner = (
            "Dinner: Grilled fish or chicken with vegetables."
        )


    else:

        breakfast = (
            "Breakfast: Oats with fruits and plant-based milk."
        )

        lunch = (
            "Lunch: Brown rice with lentils, "
            "vegetables and salad."
        )

        snack = (
            "Snack: Fresh fruit or roasted chickpeas."
        )

        dinner = (
            "Dinner: Vegetable soup with beans and whole grains."
        )


   

    if "Dairy" in allergies:

        plan.append(
            "Dairy allergy selected: avoid dairy products and use suitable alternatives."
        )

    if "Nuts" in allergies:

        plan.append(
            "Nut allergy selected: avoid nuts and nut-based products."
        )

    if "Gluten" in allergies:

        plan.append(
            "Gluten allergy selected: choose gluten-free grains such as rice or millet."
        )

    if "Eggs" in allergies:

        plan.append(
            "Egg allergy selected: avoid eggs and choose other protein sources."
        )

    if "Soy" in allergies:

        plan.append(
            "Soy allergy selected: avoid soy-based products."
        )


    plan.extend([
        breakfast,
        lunch,
        snack,
        dinner
    ])

    return plan




def create_exercise_plan(exercise_time, intensity):

    if intensity == "Beginner":

        return [

            "Warm-up: 5 minutes of light stretching.",

            "Cardio: Brisk walking or easy cycling.",

            "Strength: Bodyweight squats, wall push-ups and lunges.",

            f"Exercise duration: {exercise_time}.",

            "Cool-down: 5 minutes of gentle stretching."

        ]


    elif intensity == "Moderate":

        return [

            "Warm-up: 5–10 minutes of dynamic stretching.",

            "Cardio: Jogging, cycling or fast walking.",

            "Strength: Squats, push-ups, planks and lunges.",

            f"Exercise duration: {exercise_time}.",

            "Cool-down: Stretching and slow breathing."

        ]


    else:

        return [

            "Warm-up: 10 minutes of dynamic movement.",

            "Cardio: Running, HIIT or intense cycling.",

            "Strength: Advanced bodyweight or resistance training.",

            f"Exercise duration: {exercise_time}.",

            "Cool-down: Stretching and recovery exercises."

        ]




@app.route("/", methods=["GET", "POST"])
def home():

    

    if request.method == "GET":

        return render_template_string(HTML)


    step = request.form.get("step")


    

    if step == "bmi":

        age = int(request.form["age"])

        gender = request.form["gender"]

        height = float(request.form["height"])

        weight = float(request.form["weight"])


        height_m = height / 100


        bmi = round(
            weight / (height_m * height_m),
            1
        )


        category = get_bmi_category(bmi)


        return render_template_string(

            HTML,

            bmi=bmi,

            category=category,

            age=age,

            gender=gender,

            show_suggestions=False

        )


   

    elif step == "suggestions":

        return render_template_string(

            HTML,

            bmi=request.form["bmi"],

            category=request.form["category"],

            age=request.form["age"],

            gender=request.form["gender"],

            show_suggestions=True

        )


    

    elif step == "no_suggestions":

        # Redirect back to the first page
        return redirect(url_for("home"))


    

    elif step == "plan":

        bmi = request.form["bmi"]

        category = request.form["category"]

        age = request.form["age"]

        gender = request.form["gender"]

        diet = request.form["diet"]

        allergies = request.form.getlist("allergies")

        exercise_time = request.form["exercise_time"]

        intensity = request.form["intensity"]


        diet_plan = create_diet_plan(
            diet,
            allergies,
            category
        )


        exercise_plan = create_exercise_plan(
            exercise_time,
            intensity
        )


        return render_template_string(

            HTML,

            bmi=bmi,

            category=category,

            age=age,

            gender=gender,

            diet=diet,

            allergies=allergies,

            exercise_time=exercise_time,

            intensity=intensity,

            diet_plan=diet_plan,

            exercise_plan=exercise_plan,

            plan=True

        )


    return "Something went wrong. Please start again."



if __name__ == "__main__":

    app.run(debug=True)