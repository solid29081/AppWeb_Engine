import os
import webview

class Api:
    def alert(self, message):
        print(f"[Alert] {message}")
        return f"Alert shown: {message}"

    def prompt(self, question):
        print(f"[Prompt] {question}")
        answer = input(f"Prompt from JS: {question}\n> ")
        return answer

    def open_uri(self, uri):
        print(f"[Open URI] {uri}")
        window = webview.windows[0]
        if uri.startswith(("http://", "https://")):
            window.load_url(uri)
        else:
            print("Custom URI scheme:", uri)
        return None

    # ---------------------------------------------------
    # COOKIE MANAGEMENT (PYTHON <-> JAVASCRIPT)
    # ---------------------------------------------------

    def set_cookie(self, name, value, days=30):
        print(f"[Set Cookie] {name}={value}")
        return {
            "name": name,
            "value": value,
            "days": days
        }

    def delete_cookie(self, name):
        print(f"[Delete Cookie] {name}")
        return {
            "delete": name
        }

    def read_cookie(self, name):
        print(f"[Read Cookie] {name}")
        return name


def main():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    html_path = os.path.join(current_dir, "assets", "index.html")

    api = Api()

    # ---------------------------------------------------
    # JS COOKIE HELPERS (AUTO-INJECTED INTO EVERY PAGE)
    # ---------------------------------------------------
    js_cookie_api = """
        window.setCookie = function(name, value, days = 30) {
            document.cookie = `${name}=${value}; Max-Age=${days * 86400}; path=/`;
            console.log('[JS] Set cookie:', name, value);
        };

        window.getCookie = function(name) {
            const cookies = document.cookie.split('; ').reduce((a, c) => {
                const [k, v] = c.split('=');
                a[k] = v;
                return a;
            }, {});
            console.log('[JS] Read cookie:', name, cookies[name] || null);
            return cookies[name] || null;
        };

        window.deleteCookie = function(name) {
            document.cookie = `${name}=; Max-Age=0; path=/`;
            console.log('[JS] Deleted cookie:', name);
        };

        console.log('Cookie API Initialized');
    """

    # ---------------------------------------------------
    # CREATE WINDOW
    # ---------------------------------------------------
    window = webview.create_window(
        title="AppWeb_Engine",
        url="file://{html_path}",
        js_api=api,
        width=900,
        height=700,
        resizable=True,
        confirm_close=True,
        text_select=True,
        on_top_loaded=js_cookie_api  # inject cookie JS
    )

    # ---------------------------------------------------
    # START WEBVIEW
    # ---------------------------------------------------
    webview.start(debug=False)


if __name__ == "__main__":
    main()
