import webview
import os
import json
import threading
from urllib.parse import urlparse

# -------------------------------------------------------
# Paths
# -------------------------------------------------------
current_dir = os.path.abspath(os.path.dirname(__file__))
html_path = os.path.join(current_dir, "assets", "index.html")
COOKIE_DIR = os.path.join(current_dir, "cookies")
os.makedirs(COOKIE_DIR, exist_ok=True)

# -------------------------------------------------------
# Save cookies to JSON file for the domain
# -------------------------------------------------------
def save_cookies(domain, cookie_string):
    if not domain:
        return

    path = os.path.join(COOKIE_DIR, f"{domain}.json")
    data = {"cookies": cookie_string}

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


# -------------------------------------------------------
# Load cookies from JSON file for the domain
# -------------------------------------------------------
def load_cookies(domain):
    path = os.path.join(COOKIE_DIR, f"{domain}.json")
    if not os.path.exists(path):
        return ""

    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f).get("cookies", "")
        except:
            return ""


# -------------------------------------------------------
# Inject cookies into the page using JavaScript
# -------------------------------------------------------
def inject_cookies(window, url):
    domain = urlparse(url).hostname or "localfile"
    cookie_string = load_cookies(domain)

    if cookie_string:
        js = ";".join([f"document.cookie='{c.strip()}';" for c in cookie_string.split(";")])
        window.evaluate_js(js)


# -------------------------------------------------------
# Called each time the page finishes loading
# -------------------------------------------------------
def on_page_loaded(window):
    url = window.get_current_url()
    domain = urlparse(url).hostname or "localfile"

    # Get cookies from browser
    cookie_js = "document.cookie;"
    cookie_string = window.evaluate_js(cookie_js)

    save_cookies(domain, cookie_string)


# -------------------------------------------------------
# Bridge API for JS <-> Python
# -------------------------------------------------------
class Api:
    def alert(self, message):
        print(f"[Alert] {message}")

    def open_uri(self, uri):
        print(f"[Open URI] {uri}")
        window = webview.windows[0]
        if uri.startswith(("http://", "https://")):
            window.load_url(uri)
        elif uri.startswith("file://"):
            window.load_url(uri)
        else:
            print("Custom scheme:", uri)
        return True


# -------------------------------------------------------
# Start WebView
# -------------------------------------------------------
def start_webview():
    api = Api()

    # Create window with local HTML
    window = webview.create_window(
        title="AppWeb_Engine v.1.2",
        url=f"file://{html_path}",
        js_api=api,
        width=900,
        height=700,
        resizable=True,
        confirm_close=True,
        text_select=True
    )

    # Monitor URL changes to inject cookies
    def hook_loop():
        last_url = None
        while True:
            current_url = window.get_current_url()
            if current_url != last_url:
                inject_cookies(window, current_url)
                last_url = current_url
            threading.Event().wait(0.5)

    window.events.loaded += lambda: on_page_loaded(window)
    threading.Thread(target=hook_loop, daemon=True).start()

    webview.start()


if __name__ == "__main__":
    start_webview()
