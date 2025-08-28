import smtplib
from email.mime.text import MIMEText

# --- Настройки аккаунта Microsoft ---
smtp_server = 'smtp.office365.com'  # или 'smtp-mail.outlook.com'
port = 587  # порт для TLS-шифрования
sender_email = 'your_email@outlook.com'
app_password = 'your_app_password'  # Используйте пароль для приложения, а не обычный пароль!

# --- Детали письма ---
receiver_email = 'recipient_email@example.com'
subject = 'Тестовое письмо из Python'
body = 'Привет! Это тестовое письмо, отправленное с помощью Python через аккаунт Microsoft.'

# --- Создание объекта письма ---
msg = MIMEText(body, 'plain', 'utf-8')
msg['Subject'] = subject
msg['From'] = sender_email
msg['To'] = receiver_email

try:
    # 1. Создание SMTP-объекта
    # smtp.office365.com требует TLS, поэтому мы используем `starttls()`
    with smtplib.SMTP(smtp_server, port) as server:

        # 2. Переводим соединение в защищённый режим TLS
        server.starttls()

        # 3. Аутентификация на сервере
        server.login(sender_email, app_password)

        # 4. Отправка письма
        server.send_message(msg)

    print("Письмо успешно отправлено!")

except smtplib.SMTPAuthenticationError as e:
    print("Ошибка аутентификации. Проверьте ваш email и пароль для приложения.")
    print(f"Детали ошибки: {e}")
except Exception as e:
    print(f"Произошла ошибка при отправке письма: {e}")