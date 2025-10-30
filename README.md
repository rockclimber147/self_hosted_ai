AI accessibility tool


## Backend Setup Instructions

Note: when installing packages or running using `python`, e.g. `python manage.py runserver`, and it doesn't work, try using `python3` instead. This is common on Mac and Linux systems.

### 1. Clone the repository

```bash
git clone https://github.com/rockclimber147/self_hosted_ai.git
cd backend
```

### 2. Set up and activate the virtual environment

```bash
Create a virtual environment named "venv":
run: python -m venv venv # or python3 -m venv venv
```

### 3. Make sure VSCode is using this interpreter
1. Open Command Palette

   - Press Ctrl + Shift + P (Windows/Linux)
   - Press Cmd + Shift + P (macOS)

2. Search and Select:

   Python: Select Interpreter

3. Choose the Correct Environment

   - Look for the interpreter path that corresponds to:
     - Your virtual environment (e.g., .venv/bin/python, venv\Scripts\python.exe)
     - A Poetry environment (usually includes .cache/pypoetry)
     - Conda or system Python if you're using those

   If unsure, choose the one matching your project folder.

### 4. Activate the virtual environment

- **Windows**:

```bash
venv\Scripts\activate
```

- **Linux/Mac**:

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the server
```bash
uvicorn main:app --reload
```
