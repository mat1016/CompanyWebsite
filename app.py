
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "company.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS company (
            id INTEGER PRIMARY KEY,
            name TEXT,
            title TEXT,
            description TEXT,
            services TEXT,
            about TEXT,
            phone TEXT,
            email TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS team (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            position TEXT,
            education TEXT,
            experience TEXT,
            specialty TEXT,
            bio TEXT
        )
    """)

    company = conn.execute(
        "SELECT id FROM company WHERE id = 1"
    ).fetchone()

    if company is None:
        conn.execute(
            """
            INSERT INTO company
            (id, name, title, description, services, about, phone, email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                "پرلیت کاوان سبز",
                "مهندسین مشاور",
                "شرکت پرلیت کاوان سبز از سال 1387 در عرصه های ملی و بین المللی با ارائه راهکارهای نوین و خدمات حرفه‌ای برای رشد کسب‌وکار و همچنین استفاده از علم مهندسین با تجربه پروژه های بزرگی را به سر انجام رسانده اند",
                "مشاوره در عرصه های ژئوفیزیک، زمین شناسی، ژئوتکنیک، ژئولوژی و ...",
                "ما با ارائه خدمات حرفه‌ای و استفاده از فناوری‌های جدید، به کسب‌وکارها کمک می‌کنیم حضور قدرتمندتری در فضای کار داشته باشند.",
                "02177074548",
                "Perlit.k.s@gmail.com"
            )
        )

    count = conn.execute(
        "SELECT COUNT(*) FROM team"
    ).fetchone()[0]

    if count == 0:

        members = [
            (
                "نام مدیرعامل اول",
                "مدیرعامل",
                "مهندس ...",
                "مثلاً ۱۵ سال",
                "مدیریت و مهندسی",
                "رزومه مدیرعامل اول در این قسمت قرار می‌گیرد."
            ),
            (
                "نام مدیرعامل دوم",
                "مدیرعامل",
                "مهندس ...",
                "مثلاً ۱۲ سال",
                "مدیریت پروژه",
                "رزومه مدیرعامل دوم در این قسمت قرار می‌گیرد."
            ),
            (
                "نام کارمند",
                "کارشناس",
                "مهندس ...",
                "مثلاً ۵ سال",
                "زمین شناسی و ژئوتکنیک",
                "رزومه این کارمند در این قسمت قرار می‌گیرد."
            )
        ]

        conn.executemany(
            """
            INSERT INTO team
            (name, position, education, experience, specialty, bio)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            members
        )

    conn.commit()
    conn.close()


def get_company():
    conn = get_db()
    company = conn.execute(
        "SELECT * FROM company WHERE id = 1"
    ).fetchone()
    conn.close()
    return company


def get_team():
    conn = get_db()
    team = conn.execute(
        "SELECT * FROM team ORDER BY id"
    ).fetchall()
    conn.close()
    return team


init_database()


@app.route("/")
def home():
    company = get_company()
    team = get_team()

    return render_template(
        "index.html",
        company=company,
        team=team
    )


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        form_type = request.form.get("form_type")

        if form_type == "company":

            conn = get_db()

            conn.execute(
                """
                UPDATE company
                SET name = ?,
                    title = ?,
                    description = ?,
                    services = ?,
                    about = ?,
                    phone = ?,
                    email = ?
                WHERE id = 1
                """,
                (
                    request.form["name"],
                    request.form["title"],
                    request.form["description"],
                    request.form["services"],
                    request.form["about"],
                    request.form["phone"],
                    request.form["email"]
                )
            )

            conn.commit()
            conn.close()

            return redirect("/admin")

        if form_type == "team":

            member_id = request.form["member_id"]

            conn = get_db()

            conn.execute(
                """
                UPDATE team
                SET name = ?,
                    position = ?,
                    education = ?,
                    experience = ?,
                    specialty = ?,
                    bio = ?
                WHERE id = ?
                """,
                (
                    request.form["name"],
                    request.form["position"],
                    request.form["education"],
                    request.form["experience"],
                    request.form["specialty"],
                    request.form["bio"],
                    member_id
                )
            )

            conn.commit()
            conn.close()

            return redirect("/admin")

    company = get_company()
    team = get_team()

    return render_template(
        "admin.html",
        company=company,
        team=team
    )


@app.route("/admin/team/add", methods=["POST"])
def add_team_member():

    conn = get_db()

    conn.execute(
        """
        INSERT INTO team
        (name, position, education, experience, specialty, bio)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "عضو جدید",
            "سمت جدید",
            "",
            "",
            "",
            "رزومه و توضیحات این عضو را وارد کنید."
        )
    )

    conn.commit()
    conn.close()

    return redirect("/admin")


@app.route("/admin/team/delete/<int:member_id>", methods=["POST"])
def delete_team_member(member_id):

    conn = get_db()

    conn.execute(
        "DELETE FROM team WHERE id = ?",
        (member_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)
    
