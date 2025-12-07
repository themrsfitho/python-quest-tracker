# Python Quest Tracker

**A modular Python CLI application to track personal goals using a gamified quest system with simulated AI-generated tasks.**

---

## 📝 Project Overview

The Python Quest Tracker is a command-line interface (CLI) app that lets users create and manage quests to achieve personal goals. It demonstrates:

- Object-oriented programming (OOP) in Python  
- File-based data persistence with JSON  
- Modular project architecture  
- Simulated AI-style quest generation  
- CLI user interaction and input handling  

This project was designed to showcase Python programming skills suitable for junior Python developer, automation, and scripting roles.

---

## ⚙️ Features

- **User management**: Create and switch between multiple users.  
- **Quest tracking**: Add, list, and complete quests with points and difficulty levels.  
- **AI-generated quests (simulated)**: Generate personalized quests for your goals using a mock AI engine.  
- **Persistence**: All users and quests are saved in `data/users.json`.  
- **Clean CLI interface**: Simple, text-based menu navigation for easy interaction.  

---

## 🗂️ Project Structure

```text
python-quest-tracker/
├── main.py           # Main CLI application
├── tracker.py        # QuestTracker class (user management & data persistence)
├── quest.py          # Quest class
├── utils.py          # Utility functions (AI quest generation)
├── ai_engine.py      # Simulated AI engine for quest generation
├── prompts/          # Folder containing AI prompt templates
│   ├── base_prompt.txt
│   ├── quest_gen_prompt.txt
│   └── schema.json
└── data/
    └── users.json    # JSON file to store users and quests
