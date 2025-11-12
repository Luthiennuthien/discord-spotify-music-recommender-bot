# discord-spotify-music-recommender-bot

 🎵 Discord Spotify Music Recommender Bot

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Discord.py](https://img.shields.io/badge/discord.py-2.3+-purple.svg)
![Spotify API](https://img.shields.io/badge/Spotify-API-success.svg)

A personalized **Spotify Music Recommender System** built as a **Discord bot**.  
It connects to Spotify’s Web API to analyze a user’s listening patterns and recommend new songs that match their preferences.  
This project integrates **data analysis (Pandas)**, **API usage (Spotipy)**, and **Discord bot development (discord.py)** to create an intelligent and interactive recommendation experience.

---

## 🚀 Features

- 🎧 **/search** — Search for artists or tracks on Spotify and preview them in Discord  
- 📋 **/findtrack** — View playlist stats and metadata  
- 👤 **/user** — Fetch and analyze a Spotify user’s playlists  
- 📊 **/displaystat** — Display the user’s average music stats (energy, tempo, etc.)  
- 💡 **/recommend** — Generate music recommendations based on the user’s listening habits  
- 💽 **/create** — Automatically create a Spotify playlist with recommended songs  
- 🧠 **/personality** — Generate a short description of the user’s “music personality”  

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| **Language** | Python 3.10+ |
| **Discord Bot Framework** | discord.py |
| **Spotify API Wrapper** | Spotipy |
| **Data Analysis** | Pandas |
| **Secrets Management** | python-dotenv |
| **Async Programming** | asyncio |

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<yourusername>/discord-spotify-music-recommender-bot.git
cd discord-spotify-music-recommender-bot
