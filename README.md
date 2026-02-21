# UnReel
Streamlit app to replace doom-scrolling with learning.

[![Gatekeeper](https://github.com/matze298/unreel/actions/workflows/gatekeeper.yml/badge.svg)](https://github.com/matze298/unreel/actions/workflows/gatekeeper.yml)

[![codecov](https://codecov.io/gh/matze298/unreel/graph/badge.svg?token=S15KJJOKVU)](https://codecov.io/gh/matze298/unreel)

## Local usage
Run with
`streamlit run main.py`

## Mobile Usage
To use on your iPhone:
1. Ensure your phone and computer are on the same Wi-Fi.
2. Run with:
   ```bash
   streamlit run main.py --server.address 0.0.0.0
   ```
3. Open `http://<YOUR_COMPUTER_IP>:8501` in Safari.
  1. To find your computer IP, run `ipconfig`.
4. Tap "Share" -> "Add to Home Screen".

## Cloud Hosting (Free)
To host the app online without running it on your computer, use **Streamlit Community Cloud**:

1. **Push to GitHub**: Ensure your code is in a public GitHub repository.
2. **Deploy**:
   - Go to share.streamlit.io and sign up.
   - Click **New app**, select your repository, and set the main file to `main.py`.
   - Click **Deploy**.
3. **Secrets**: In the app dashboard, go to **Settings** -> **Secrets** and add:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```