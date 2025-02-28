# [Ongoing...]AI Agents for Hospital Appointment Booking

## Overview

This project is an AI-powered chatbot designed to handle hospital appointment bookings efficiently. It leverages **DeepSeek-Self-Manage** for AI agent functionalities, providing features such as:

- **Conversational AI** for doctor appointment scheduling.
- **Session Management** to track and maintain conversation flow.
- **Conversation Logging & Monitoring** for tracking and auditing interactions.
- **Bypassing Mechanism** to escalate conversations to human customer service when necessary.

## Features

### 1. Conversational AI

- Handles basic Q&A related to doctor appointments.
- Guides users through the booking process.
- Provides relevant hospital and doctor availability information.

### 2. Session Management

- Tracks session states (open, ongoing, closed).
- Enables session continuation to prevent redundant conversations.
- Helps optimize business logic and reduce operational costs.

### 3. Conversation Logging & Monitoring

- Logs user interactions for analysis and auditing.
- Stores key details of user queries and responses.
- Provides insights into chatbot performance and potential improvements.

### 4. Human Escalation (Bypassing)

- Identifies cases where chatbot should not handle a query.
- Transfers the conversation with logs to human agents.
- Ensures a smooth transition by providing past conversation context.

## Tech Stack

- **Backend:** FastAPI + Uvicorn
- **AI Framework:** DeepSeek-Self-Manage
- **Database:** PostgreSQL / MongoDB (for session & log storage)
- **Logging:** ELK Stack (Elasticsearch, Logstash, Kibana) or alternative
- **Deployment:** Docker + Kubernetes (optional)

## Project Structure

```
📂 AI-Agents-Hospital-Booking
├── 📁 src
│   ├── 📁 agents  # AI agent configurations
│   ├── 📁 api     # FastAPI routes
│   ├── 📁 db      # Database connection & models
│   ├── 📁 logs    # Logging setup
│   ├── main.py   # Entry point for the app
├── 📁 configs     # Configuration files
├── 📁 tests       # Unit & integration tests
├── 📄 README.md   # Project documentation
├── 📄 requirements.txt  # Python dependencies
├── 📄 Dockerfile  # Containerization setup
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Agents-Hospital-Booking.git
cd AI-Agents-Hospital-Booking
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate    # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn src.main:app --reload
```

## API Endpoints

| Method | Endpoint                   | Description              |
| ------ | -------------------------- | ------------------------ |
| POST   | `/appointment/book`        | Book a new appointment   |
| GET    | `/appointment/status/{id}` | Check appointment status |
| POST   | `/conversation/logs`       | Store conversation logs  |
| POST   | `/conversation/transfer`   | Escalate to human agent  |

## Future Enhancements

- Integrate NLP models for better intent recognition.
- Add authentication and user profile management.
- Deploy using cloud services (AWS/GCP/Azure).

## Contribution

Feel free to open issues and pull requests to enhance this project! 🚀

## License

This project is licensed under the MIT License.
