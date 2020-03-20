# yt-favs

*Python script using the Youtube-API and youtube-dl to download and keep track of your Youtube favorites*

If you want to keep a backup copy of your favorite videos, it is quite inconvinient to download them manually and to keep track of which videos are new and which you already have saved. This simple script can automate this task for you.

## Prerequisites
- Python 3.5+
- [youtube-dl](https://github.com/ytdl-org/youtube-dl)
- Youtube/Google-Account

## Setup
1. Clone this repo
    ```bash
    git clone git@github.com:n0ctua/yt-favs.git
    ```
2. Create and activate an isolated Python environment
    ```bash
    python3 -m venv ./venv
    source venv/bin/activate
    ```
3. Install requirements
    ```bash
     pip install --upgrade -r requirements.txt
    ```
4. Setup Credentials
  a. Visit your [Google API Console](https://console.developers.google.com/)
  b. Create a new project, e.g. *yt-favs*
  c. In the [library panel](https://console.developers.google.com/apis/library), find and enable the `YouTube Data API v3` for this project
  d. In the [credentials panel](https://console.developers.google.com/apis/credentials), create an `OAuth 2.0 client ID` and set the application type to `TVs and Limited Input devices`
  e. Download the JSON file that contains your OAuth 2.0 credentials, rename it to `client_secret.json` and move it to the project directory
  f. When you run the script for the first time, your browser will open and you have to grant this app the permission to access your Youtube account.
  You can always check which third-party apps can access your Google account [here](https://myaccount.google.com/permissions).

## Usage
```bash
source venv/bin/activate
python3 yt-favs.py
```
