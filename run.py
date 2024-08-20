from app import create_app
from werkzeug.middleware.proxy_fix import ProxyFix

app = create_app()

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config["PREFERRED_URL_SCHEME"] = "https"

if __name__ == "__main__":
    app.run(ssl_context="adhoc")
