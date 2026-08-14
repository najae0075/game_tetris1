# Tetris Streamlit App

This project runs a browser-style Tetris game inside a Streamlit app.

## Project structure

- `streamlit_app.py` — main app entry point
- `requirements.txt` — Python dependency list for deployment
- `.streamlit/config.toml` — Streamlit theme and server config
- `.gitignore` — repository hygiene for local and virtualenv files

## Run locally

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Open Streamlit Community Cloud.
3. Click "New app" and choose the repository.
4. Select the app file as `streamlit_app.py`.
5. Keep `requirements.txt` as the dependency source.
6. Click deploy.

## Notes

- The app is a static front-end game embedded in Streamlit and does not require a database.
- Browser localStorage is used for the best-score value in the client, so it works in the browser session.
- No secret keys or external credentials are required.
