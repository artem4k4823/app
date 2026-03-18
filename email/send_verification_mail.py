from app.core.models.users import User
from app.email.send_mail import send_mail

async def send_verification_mail(user: User, verification_code: str, verification_link: str):
    recipient = user.email
    subject = 'Подтвердите ваш email'
    plain_content = f"Ваш код подтверждения: {verification_code}"
    html_content = f"<h1>Ваш код подтверждения: {verification_code}</h1>"
    await send_mail(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content= html_content
    )
   