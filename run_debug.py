from app.main import app


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
