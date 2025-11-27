# AppWeb_Engine
## Welcome to AppWeb_Engine, here's what you will need to do
To get AppWeb_Engine working, its really simple. You need to change 2 lines of code that are so easy to understand.
Line 1 of code would be this:
url=f"file://{html_path}", (line 98)
and then.
title="AppWeb_Engine v1.2", (line 97)

Really fucking simple.

If you really want to, you can change the index.html in the assets folder to make the app using HTML

Skidded peice of shit.

# PLEASE READ IF YOU ARE GOING TO PACKAGE THIS
Python Web App Packaging Instructions (Windows .exe)
----------------------------------------------------

1. Make sure your project folder looks like this:

AppWeb_Engine/
│
├── app.py
├── requirements.txt
└── assets/
    ├── icon.ico
    └── index.html  (if using local files)

2. Install PyInstaller (if not already installed):

   Open a terminal or command prompt and run:
   pip install pyinstaller

3. (Optional) Activate your virtual environment if you have one:
   Windows:
       venv\Scripts\activate
   macOS/Linux:
       source venv/bin/activate

4. Open a terminal/command prompt in your project folder.

5. Run PyInstaller with the following command to build a standalone executable:

   If your app uses a local HTML file:
   pyinstaller --onefile --windowed --icon=assets/icon.ico app.py

   Notes:
   --onefile     -> Packages everything into a single executable.
   --windowed    -> Hides the console window for a GUI app.
   --icon        -> Sets the icon for the executable.

6. After PyInstaller finishes, the executable will be in the 'dist' folder:

   AppWeb_Engine/
   └── dist/
       └── app.exe

7. Test the executable by double-clicking 'app.exe'. It should open your web app window with your custom icon.

8. (Optional) To clean up the build files, you can delete the following folders:

   build/
   __pycache__/
   app.spec

9. Distribution:
   - You can now distribute the 'app.exe' file.
   - If using local assets (like index.html), make sure they are included in the same folder or modify the app to load them from relative paths.
