# Overview


The **SpendWise** app helps users take control of their finances by centralizing subscription management into one intuitive platform. By securely connecting multiple bank accounts, users can track upcoming payments, view active subscriptions, and monitor transactions in real time. Powered by Agentic AI, the app delivers actionable recommendations and answers user questions directly, empowering smarter financial decisions, reducing unnecessary spending, and building confidence in money management.

## AI Features
#### Recommend Subscriptions
- Scenario: A user wonders if there are better subscription options than the ones they currently have.
- Solution: AI recommends subscriptions based on the user’s subscription information.
#### Ask About Subscriptions
- Scenario: A user wants to know whether their T-Mobile plan includes free subscriptions.
- Solution: The AI answers and responds to subscription-related questions.
#### Compare Subscriptions
- Scenario: A user is looking for better alternatives to their current subscriptions.
- Solution: The AI compares available options based on user needs and subscription information.
#### Save Money
- Scenario: A user is unsure how to save money and optimize their active subscriptions.
- Solution: The AI suggests cost-saving actions, provides reasoning, and offers actionable buttons for guidance.

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
5. Build and run the application on your iOS device or simulator.

## Acknowledgments
- Watsonx AI: For providing the models that power the AI agent.
- SwiftUI: For enabling modern UI development on iOS.
