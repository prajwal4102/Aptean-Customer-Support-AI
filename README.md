# Customer Support - AI case resolution agent.

A comprehensive web application featuring a real-time customer support dashboard with integrated AI-powered SQL chatbot. The system provides live monitoring of support tickets, customer information, and agent performance through an intuitive interface. The AI assistant allows users to query the database using natural language, making data access effortless for non-technical users.

## Features

- **Real-time Dashboard**: Monitor support tickets, customers, and agents with live updates
- **SQL Assistant Chatbot**: AI-powered natural language interface for database queries
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Visual Analytics**: Interactive charts showing ticket status distribution
- **Role-based Access**: Supervisor login functionality
- **Voice Support**: Floating support icon with call functionality

## Technology Stack

### Frontend
- HTML5, CSS3, JavaScript (ES6+)
- Chart.js for data visualization
- Font Awesome icons
- Responsive grid layout

### Backend
- Python with FastAPI framework
- MySQL database
- DeepSeek AI language model
- LangChain for prompt management

## Project Structure

```
customer-support-dashboard/
├── dashboard.html          # Main dashboard frontend
├── backend.py             # FastAPI backend server
├── index.html             # Aptean website clone with support features
└── README.md              # Project documentation
```

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd customer-support-dashboard
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install fastapi uvicorn langchain-openai langchain-community mysql-connector-python
   ```

4. **Set up MySQL database**
   - Create a database named `customer_support_database`
   - Update the connection string in `backend.py` if needed

5. **Configure API key**
   - Add your DeepSeek API key to the `DEEPSEEK_API_KEY` environment variable

6. **Run the backend server**
   ```bash
   python backend.py
   ```

7. **Open the applications**
   - Dashboard: Open `dashboard.html` in a web browser
   - Aptean website: Open `index.html` in a web browser
   - Or use a local server: `python -m http.server 5500` then navigate to the desired file

## API Endpoints

- `GET /tickets` - Retrieve all support tickets
- `GET /customers` - Retrieve all customers
- `GET /users` - Retrieve all users/agents
- `GET /agents` - Retrieve agents with active ticket counts
- `POST /ask` - Process natural language SQL queries

## Database Schema

The application uses four main tables:
- **users**: Support agents and administrators
- **customers**: Company clients and contact information
- **tickets**: Support requests with status and priority tracking
- **ticket_updates**: History of ticket modifications

## Usage

1. **Dashboard**: View real-time statistics and tables of tickets, customers, and agents
2. **SQL Assistant**: Click the chat icon in the bottom right to ask questions in natural language
   - Example: "Show me all high priority tickets from last week"
   - Example: "Which customers have the most open tickets?"
3. **Voice Support**: Click the floating headset icon for voice support options

## Customization

- Modify the MySQL connection string in `backend.py` for your database
- Adjust the dashboard styling in `dashboard.html` to match your brand
- Customize the SQL prompts in the backend for specialized queries

## License

This project is created for demonstration purposes.

## Screenshots

The application includes:
- Modern dashboard with statistics cards
- Interactive data tables
- AI chat interface
- Professional website design with support features

## Support

For technical support, use the voice support feature in the application or contact the development team.

