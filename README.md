<img width="1366" height="648" alt="Screenshot (48)" src="https://github.com/user-attachments/assets/f49bd679-09bc-4b36-b953-8bbfd02b1cb3" />


# MythBane
It is an AI-powered dashboard application that is made to debunk myths/conspiracy theories/rumors/stereotypes.The UI is cyber-themed and it gives short,concise and near accurate verdicts.

# Installation & Setup
**1 Clone the repository**
    ```bash

    git clone [https://github.com/rr-codes4/MythBane.git](https://github.com/rr-   codes4/MythBane.git)
    cd MythBane

**2 Install dependencies**
     ```bash
            
      pip install -r requirement.txt
**3 Run**
    ```bash
  
     py main.py
**4 Accesing the app**
    ```bash
   
     lt --port 5000

# Quickstart
**Example Query:** Type "Is the moon landing hoax?" in the dashboard and wait for it to reply.
**Try it out (Important info before starting,when you will click this link a localtunnel security page will pop up,Trust me,you just have to copy and paste the IP password on the screen)** [link to the website](./https://evil-bottles-drive.loca.lt/)



<img width="1366" height="648" alt="Screenshot (49)" src="https://github.com/user-attachments/assets/0c063592-ce6b-439e-b955-cf31134ef043" />

<img width="1366" height="661" alt="Screenshot (50)" src="https://github.com/user-attachments/assets/6d4dd540-5ab7-4b15-a59d-102067312630" />



# Troubleshooting (Please read its important)
**Rate limits** If the app receives a lot of requests, a rate-limit may occur and the app will stop working.Simply wait a moment and try again.

**Network/DNS errors** These error occurs from your sides,try checking you network.In cases of DNS error the tools (DDGS,WIKI) will stop working still the AI will use it existing knowledge and answer.


**Fatal Backend error** Please try to use correct grammar, if your grammar is wrong, the app will throw an error. Also this app strictly follows nohello.net, so it will refuse to talk with you and throw an error.

<img width="1366" height="661" alt="Screenshot (52)" src="https://github.com/user-attachments/assets/354ab74c-e54c-4a6c-949f-12edc88ecc22" />



# Detailed backend breakdown
My backend is structured around Flask,Python and AI agent orchestration (like LangChain)
* **flask initialization (`app = Flask(__name__)`):** Flask creates a lightweight website in Python.On running the programme (through main.py file) flask boots up and listens for HTTP requests (its like when you visit the website or type something) It connects to `0.0.0.0:5000` and Localtunnel forwards the traffic.

* **AI model (`ai.hackclub.com` proxy):** I have used OpenAI's API through Hackclub's proxy base URL.When user writes anything the model'gpt-4o-mini' using langchain breaks down the response and decides if they need any external source t answer accurately.
* **Tool (DDGS & WIKI)** Allows the model to look for information outside its training data.I have defined a tool wrapper for 'Wikipedia' and 'DuckDuckGo'.When the model gets queries it does not have an idea about it simply triggers a tool call and it scrapes through these sources.
* **Structure** The response AI gives is organized.My system prompts instructs the model to follow the format strictly.
* **Errors & Exception handling** Prevents AI from crashing if API fails and in DNS error it handle it gracefully.
* Also you will see a chat_history.txt files in the repository.Earlier I made it to save chats but later I decided not to save chats.The file is of no use now but still you can see my chat history just to see how it works.



# Cloud Hosting
Cloud hosting is done using nest

# AI usage
I have used AI for debugging. I am a backend developer so making frontend was not my cup of tea so I described the design and AI made it for me.

## Repository Structure
```bash
MythBane
   |_ templates
        |_ index.html
      .gitignore
      Readme.md
      chat_history.txt
      main.py
      requirements.txt
      resources.py
      
I have used AI in debugging and code generation.As I am not experienced in frontend I have used AI to make the frontend.

