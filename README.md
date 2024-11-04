# API de Lembretes por E-mail com Autenticação JWT e Agendamento

Este projeto é uma API avançada construída com Flask, Celery e SendGrid para gerenciar e agendar lembretes por e-mail. Ele inclui:
- **JWT Authentication** for secure access to endpoints.
- **CRUD operations** to manage reminders.
- **Email scheduling** using Celery and Redis.
- **Robust validations** for request data.

## How to Run the Project

1. **Clone the repository**:
   ```bash
   git clone <REPO_URL>
   cd email_reminder_app

2. Instalar dependências:
   pip install -r requirements.txt

3. Iniciar o Redis: certifique-se de que o Redis esteja em execução no seu sistema ou configure-o adequadamente.

4. Execute o Celery :
celery -A tasks worker --loglevel=info

5. Inicie o aplicativo Flask:
python app.py
