from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from database import get_connection

from ai_model import recommend_career

from skill_gap import (
    analyze_skill_gap,
    CAREER_SKILLS
)

from roadmap import create_roadmap
from resources import get_resources


app = Flask(__name__)

# =========================================================
# SECRET KEY
# =========================================================

app.secret_key = "careerpilot_secret_key_2026"


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        # -------------------------
        # Validation
        # -------------------------

        if not name or not email or not password:

            flash(
                "Please fill all fields.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        # -------------------------
        # Check existing email
        # -------------------------

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            cursor.close()
            connection.close()

            flash(
                "Email already registered.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        # -------------------------
        # Create user
        # -------------------------

        cursor.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                name,
                email,
                password
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = %s
            AND password = %s
            """,
            (
                email,
                password
            )
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:

            session["user_id"] = user["id"]

            session["user_name"] = user["name"]

            session["user_email"] = user["email"]

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password.",
            "error"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "login.html"
    )


# =========================================================
# DASHBOARD
# STEP 13 + STEP 14 + STEP 15
# =========================================================

@app.route("/dashboard")
def dashboard():

    # -------------------------
    # Check login
    # -------------------------

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    # -------------------------
    # Get logged-in user
    # -------------------------

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = %s
        """,
        (
            session["user_id"],
        )
    )

    user = cursor.fetchone()

    if not user:

        cursor.close()
        connection.close()

        session.clear()

        return redirect(
            url_for("login")
        )

    # =====================================================
    # DEFAULT VALUES
    # =====================================================

    readiness = 0

    matched_skills = []

    missing_skills = []

    roadmap = []

    total_learning_skills = 0

    completed_learning_skills = 0

    learning_progress = 0

    career_message = ""

    career_action = ""

    overall_progress = 0

    career = user.get(
        "career_goal"
    )

    # =====================================================
    # SKILL GAP ANALYSIS
    # =====================================================

    if career:

        result = analyze_skill_gap(

            user.get("skills") or "",

            career

        )

        readiness = result["readiness"]

        matched_skills = result["matched"]

        missing_skills = result["missing"]

        # -------------------------
        # Create roadmap
        # -------------------------

        roadmap = create_roadmap(
            missing_skills
        )

        # -------------------------
        # Total skills to learn
        # -------------------------

        total_learning_skills = len(
            missing_skills
        )

        # =================================================
        # GET COMPLETED SKILLS
        # =================================================

        cursor.execute(
            """
            SELECT skill
            FROM skill_progress
            WHERE user_id = %s
            AND completed = 1
            """,
            (
                session["user_id"],
            )
        )

        completed_rows = cursor.fetchall()

        # Only count skills that are
        # currently part of the skill gap

        completed_learning_skills = len([

            row

            for row in completed_rows

            if row["skill"] in missing_skills

        ])

        # =================================================
        # LEARNING PROGRESS
        # =================================================

        if total_learning_skills > 0:

            learning_progress = int(

                (
                    completed_learning_skills
                    /
                    total_learning_skills
                )
                * 100

            )

        else:

            learning_progress = 100

    # =====================================================
    # CAREER INSIGHT
    # STEP 14
    # =====================================================

    if learning_progress == 0:

        career_message = (
            "You are at the beginning of your career "
            "journey. Start learning the skills in "
            "your roadmap."
        )

        career_action = "Start Learning"


    elif learning_progress < 50:

        career_message = (
            "Good start! Continue completing the "
            "skills in your personalized roadmap."
        )

        career_action = "Continue Learning"


    elif learning_progress < 100:

        career_message = (
            "Great progress! You are getting closer "
            "to your target career."
        )

        career_action = "Keep Going"


    else:

        career_message = (
            "Excellent! You completed all the skills "
            "in your current learning roadmap."
        )

        career_action = (
            "Explore Career Opportunities"
        )

    # =====================================================
    # OVERALL CAREER PROGRESS
    # STEP 15
    # =====================================================

    overall_progress = int(

        (
            readiness +
            learning_progress
        ) / 2

    )

    # Make sure it never exceeds 100

    if overall_progress > 100:

        overall_progress = 100

    # =====================================================
    # CLOSE DATABASE
    # =====================================================

    cursor.close()

    connection.close()

    # =====================================================
    # SEND DATA TO DASHBOARD
    # =====================================================

    return render_template(

        "dashboard.html",

        user=user,

        readiness=readiness,

        matched_skills=matched_skills,

        missing_skills=missing_skills,

        roadmap=roadmap,

        total_learning_skills=
            total_learning_skills,

        completed_learning_skills=
            completed_learning_skills,

        learning_progress=
            learning_progress,

        career_message=
            career_message,

        career_action=
            career_action,

        overall_progress=
            overall_progress

    )


# =========================================================
# PROFILE
# =========================================================

@app.route(
    "/profile",
    methods=["GET", "POST"]
)
def profile():

    # -------------------------
    # Check login
    # -------------------------

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    # -------------------------
    # Get user
    # -------------------------

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = %s
        """,
        (
            session["user_id"],
        )
    )

    user = cursor.fetchone()

    if not user:

        cursor.close()
        connection.close()

        session.clear()

        return redirect(
            url_for("login")
        )

    # =====================================================
    # UPDATE PROFILE
    # =====================================================

    if request.method == "POST":

        skills = request.form.get(
            "skills",
            ""
        ).strip()

        interests = request.form.get(
            "interests",
            ""
        ).strip()

        education = request.form.get(
            "education",
            ""
        ).strip()

        career_goal = request.form.get(
            "career_goal",
            ""
        ).strip()

        cursor.execute(
            """
            UPDATE users

            SET
                skills = %s,
                interests = %s,
                education = %s,
                career_goal = %s

            WHERE id = %s
            """,
            (
                skills,
                interests,
                education,
                career_goal,
                session["user_id"]
            )
        )

        connection.commit()

        # -------------------------
        # Get updated user
        # -------------------------

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE id = %s
            """,
            (
                session["user_id"],
            )
        )

        user = cursor.fetchone()

        flash(
            "Profile updated successfully!",
            "success"
        )

    cursor.close()

    connection.close()

    return render_template(

        "profile.html",

        user=user

    )
# =========================================================
# AI CAREER RECOMMENDATION
# =========================================================

@app.route("/recommendation")
def recommendation():

    # Check login

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    # Get logged-in user

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = %s
        """,
        (
            session["user_id"],
        )
    )


    user = cursor.fetchone()


    cursor.close()

    connection.close()


    if not user:

        session.clear()

        return redirect(
            url_for("login")
        )


    # Default values

    recommendations = []

    profile_complete = False

    message = ""


    # Get profile information

    skills = user.get("skills") or ""

    interests = user.get("interests") or ""

    education = user.get("education") or ""

    career_goal = user.get("career_goal") or ""


    # Check profile completion

    if skills and interests and education:

        profile_complete = True


    # =====================================================
    # AI RECOMMENDATION
    # =====================================================

    if profile_complete:

        recommendations = recommend_career(

            skills,

            interests,

            education

        )

        message = (
            "CareerPilot AI analyzed your profile "
            "and generated these career recommendations."
        )


    else:

        message = (
            "Complete your profile with skills, "
            "interests and education to get better "
            "AI career recommendations."
        )


    return render_template(

        "recommendation.html",

        user=user,

        recommendations=recommendations,

        profile_complete=profile_complete,

        message=message

    )    

# =========================================================
# SKILL GAP ANALYSIS
# =========================================================

@app.route(
    "/skill-gap",
    methods=["GET", "POST"]
)
def skill_gap():

    # -------------------------
    # Check login
    # -------------------------

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    # -------------------------
    # Get user
    # -------------------------

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = %s
        """,
        (
            session["user_id"],
        )
    )

    user = cursor.fetchone()

    cursor.close()

    connection.close()

    if not user:

        return redirect(
            url_for("login")
        )

    # -------------------------
    # Career list
    # -------------------------

    careers = list(
        CAREER_SKILLS.keys()
    )

    result = None

    selected_career = ""

    # =====================================================
    # ANALYZE SKILL GAP
    # =====================================================

    if request.method == "POST":

        selected_career = request.form.get(
            "career",
            ""
        )

        if selected_career:

            result = analyze_skill_gap(

                user.get("skills") or "",

                selected_career

            )

    return render_template(

        "skill_gap.html",

        careers=careers,

        result=result,

        selected_career=
            selected_career

    )


# =========================================================
# PERSONALIZED ROADMAP
# STEP 12
# =========================================================

@app.route("/roadmap")
def roadmap():

    # -------------------------
    # Check login
    # -------------------------

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    # -------------------------
    # Get user
    # -------------------------

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = %s
        """,
        (
            session["user_id"],
        )
    )

    user = cursor.fetchone()

    if not user:

        cursor.close()
        connection.close()

        return redirect(
            url_for("login")
        )

    roadmap_data = []

    completed_skills = []

    career = user.get(
        "career_goal"
    )

    readiness = 0

    # =====================================================
    # CREATE ROADMAP
    # =====================================================

    if career:

        result = analyze_skill_gap(

            user.get("skills") or "",

            career

        )

        readiness = result["readiness"]

        roadmap_data = create_roadmap(

            result["missing"]

        )

        # =================================================
        # GET COMPLETED SKILLS
        # =================================================

        cursor.execute(
            """
            SELECT skill
            FROM skill_progress
            WHERE user_id = %s
            AND completed = 1
            """,
            (
                session["user_id"],
            )
        )

        rows = cursor.fetchall()

        completed_skills = [

            row["skill"]

            for row in rows

        ]

    cursor.close()

    connection.close()

    return render_template(

        "roadmap.html",

        roadmap=roadmap_data,

        career=career,

        readiness=readiness,

        completed_skills=
            completed_skills

    )


# =========================================================
# UPDATE SKILL PROGRESS
# STEP 12
# =========================================================

@app.route(
    "/complete-skill",
    methods=["POST"]
)
def complete_skill():

    # -------------------------
    # Check login
    # -------------------------

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    skill = request.form.get(
        "skill"
    )

    if not skill:

        return redirect(
            url_for("roadmap")
        )

    connection = get_connection()

    cursor = connection.cursor()

    # -------------------------
    # Save progress
    # -------------------------

    cursor.execute(
        """
        INSERT INTO skill_progress
        (
            user_id,
            skill,
            completed
        )
        VALUES
        (
            %s,
            %s,
            1
        )

        ON DUPLICATE KEY UPDATE

            completed = 1
        """,
        (
            session["user_id"],
            skill
        )
    )

    connection.commit()

    cursor.close()

    connection.close()

    return redirect(
        url_for("roadmap")
    )
# =========================================================
# LEARNING RESOURCES
# =========================================================

@app.route("/resources")
def resources():

    # Check login

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )
        return render_template(
                "resources.html"
                                    )


    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = %s
        """,
        (
            session["user_id"],
        )
    )


    user = cursor.fetchone()


    cursor.close()

    connection.close()


    if not user:

        session.clear()

        return redirect(
            url_for("login")
        )


    resources = []

    missing_skills = []


    # Analyze career skills

    career = user.get("career_goal")


    if career:

        result = analyze_skill_gap(

            user.get("skills") or "",

            career

        )


        missing_skills = result["missing"]


        resources = get_resources(
            missing_skills
        )


    return render_template(

        "resources.html",

        user=user,

        resources=resources,

        missing_skills=missing_skills

    )
# =========================================================
# RESUME & JOB READINESS
# =========================================================

@app.route("/job-readiness")
def job_readiness():

    # Check login

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    # Get logged-in user

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = %s
        """,
        (
            session["user_id"],
        )
    )


    user = cursor.fetchone()


    cursor.close()

    connection.close()


    if not user:

        session.clear()

        return redirect(
            url_for("login")
        )


    # Default values

    readiness = 0

    matched_skills = []

    missing_skills = []

    career = user.get("career_goal")


    # Analyze career readiness

    if career:

        result = analyze_skill_gap(

            user.get("skills") or "",

            career

        )


        readiness = result["readiness"]

        matched_skills = result["matched"]

        missing_skills = result["missing"]


    # Resume readiness

    resume_score = 0


    if user.get("name"):

        resume_score += 20


    if user.get("email"):

        resume_score += 20


    if user.get("education"):

        resume_score += 20


    if user.get("skills"):

        resume_score += 20


    if user.get("career_goal"):

        resume_score += 20


    # Job readiness

    job_score = int(
        (readiness + resume_score) / 2
    )


    # Job readiness message

    if job_score < 40:

        readiness_message = (
            "You are getting started. "
            "Complete your profile and build "
            "the required skills."
        )


    elif job_score < 70:

        readiness_message = (
            "You are making good progress. "
            "Improve your missing skills and "
            "strengthen your resume."
        )


    elif job_score < 100:

        readiness_message = (
            "You are almost job ready. "
            "Focus on your remaining skill gaps "
            "and practical projects."
        )


    else:

        readiness_message = (
            "Excellent! Your profile shows strong "
            "career and job readiness."
        )


    return render_template(

        "job_readiness.html",

        user=user,

        career=career,

        readiness=readiness,

        resume_score=resume_score,

        job_score=job_score,

        matched_skills=matched_skills,

        missing_skills=missing_skills,

        readiness_message=readiness_message

    )
# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return """
    <h1>404 - Page Not Found</h1>

    <p>
        The requested page does not exist.
    </p>

    <a href="/">
        Go Home
    </a>
    """, 404


@app.errorhandler(500)
def internal_server_error(error):

    return """
    <h1>500 - Internal Server Error</h1>

    <p>
        Something went wrong in the application.
    </p>

    <a href="/">
        Go Home
    </a>
    """, 500


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )