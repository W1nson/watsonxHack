# SpendWise App
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009485.svg?style=for-the-badge&logo=fastapi&logoColor=white)
![Swift](https://img.shields.io/badge/swift-F54A2A?style=for-the-badge&logo=swift&logoColor=white)
![Xcode](https://img.shields.io/badge/Xcode-007ACC?style=for-the-badge&logo=Xcode&logoColor=white)
## Overview
The **SpendWise** app helps users take control of their finances by centralizing subscription management into one intuitive platform. By securely connecting multiple bank accounts, users can track upcoming payments, view active subscriptions, and monitor transactions in real time. Powered by Agentic AI, the app delivers actionable recommendations and answers user questions directly, empowering smarter financial decisions, reducing unnecessary spending, and building confidence in money management.

[<img src="https://github.com/user-attachments/assets/e4bf52d2-1da3-467b-9dc9-73aa456597f3" width="250"/>](https://github.com/user-attachments/assets/e4bf52d2-1da3-467b-9dc9-73aa456597f3)
[<img src="https://github.com/user-attachments/assets/03c66f84-ce33-47ce-9c82-7988e8d60f64" width="250"/>](https://github.com/user-attachments/assets/03c66f84-ce33-47ce-9c82-7988e8d60f64)

## AI Features
- **Recommend Subscriptions**: AI recommends subscriptions based on the user’s subscription information.
- **Ask About Subscriptions**: The AI answers and responds to subscription-related questions.
- **Compare Subscriptions**: The AI compares available options based on user needs and subscription information.
- **Save Money**: The AI suggests cost-saving actions, provides reasoning, and offers actionable buttons for guidance.

## Getting Started
### Prerequisites
Before you begin, ensure you have the following:
* Xcode 13.0 or later
* macOS 11.0 or later
* Python 3.11

## Installation
1. Clone the repository: 
```bash
git clone https://github.com/W1nson/watsonxHack.git
```
2. Navigate to the project directory and install Python packages:
```bash
cd watsonxHack/backend
pip install -r requirements.txt
```
3. Run backend:
```bash
cd backend/agent
uvicorn main:app --reload --log-level debug
```
4. Open the project in Xcode:
```bash
open iOS.xcodeproj
```
5. Build and run the application on your iOS simulator.

## Usage
Spendwise's AI agent, powered by Watsonx AI, utilizes a RAG system where it loads user information to enhance the AI's ability to provide more personalized and relevant responses. You can interact with the agent by navigating to the "Jarvis AI" button in the right-hand corner. From there, you can choose from the recommended questions or type in your own. The AI will process your input and respond based on the data it has access to. Feel free to explore different scenarios to see how the AI adapts its responses.

## Acknowledgments
- Watsonx AI: For providing the models that power the AI agent.
- SwiftUI: For a modern user interface for iOS.
