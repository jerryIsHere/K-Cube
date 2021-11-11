from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

branch = Blueprint("branch", __name__, url_prefix="branch")


@branch.post("/")
def post_with_workspace():
    if request.args.get("tag") is not None and request.args.get("workspaceId") is not None:
        if request.args.get("fork") is not None:
            return jsonify(
                {
                    "success": True,
                    "message": get_api_driver().workspace.commit_workspace_as_fork(
                        deltaGraphId=request.args.get("workspaceId"),
                        tag=request.args.get("tag"),
                        userId=session["user"]["userId"],
                    ),
                }
            )
        else:
            pass
    return jsonify({"success": False, "message": "incomplete request"})
