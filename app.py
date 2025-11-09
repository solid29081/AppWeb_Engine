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

def main():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    html_path = os.path.join(current_dir, "assets", "index.html")
    icon_path = os.path.join(current_dir, "assets", "icon.ico")

    api = Api()
    window = webview.create_window(
        title="Nove",
        url=f"https://novenovetus.xyz",
        js_api=api,
        width=900,
        height=700,
        resizable=True,
        confirm_close=True,
        text_select=True
    )

    # Start app without devtools or console
    webview.start(debug=False, icon=icon_path)

if __name__ == "__main__":
    main()
