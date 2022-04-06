from flask import Blueprint, render_template, abort
from app.authorizer import authorize_with
import os
from app.blueprints.collaborate import collaborate

student = Blueprint("student", __name__, template_folder="templates")


@student.before_request
@authorize_with([], True, ["student", "admin"])
def middleware():
    pass


@student.route("/dashboard")
def dashboard():
    return render_template(
        "student/dashboard.html",
        components=[
            "/".join([student.name, "dashboardComponents", f])
            for f in os.listdir(
                os.path.join(
                    student.root_path,
                    student.template_folder,
                    student.name,
                    "dashboardComponents",
                )
            )
            if os.path.isfile(
                os.path.join(
                    student.root_path,
                    student.template_folder,
                    student.name,
                    "dashboardComponents",
                    f,
                )
            )
        ]
        + [
            "/".join([collaborate.name, "dashboardComponents", f])
            for f in os.listdir(
                os.path.join(
                    collaborate.root_path,
                    collaborate.template_folder,
                    collaborate.name,
                    "dashboardComponents",
                )
            )
            if os.path.isfile(
                os.path.join(
                    collaborate.root_path,
                    collaborate.template_folder,
                    collaborate.name,
                    "dashboardComponents",
                    f,
                )
            )
        ],
    )
