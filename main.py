import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_SENDER = os.getenv("SMTP_SENDER", "ebnalnasirs13@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "Sk_barniko12")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "barniko2017@gmail.com")

def send_email(subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = SMTP_SENDER
    msg["To"] = ADMIN_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_SENDER, SMTP_PASSWORD)
        server.sendmail(SMTP_SENDER, ADMIN_EMAIL, msg.as_string())

@app.post("/api/order")
async def create_order(
    customer_name: str = Form(...),
    phone: str = Form(...),
    item_name: str = Form(...),
    quantity: int = Form(...),
    note: str = Form("")
):
    body = (
        f"سفارش جدید ثبت شد\n\n"
        f"نام مشتری: {customer_name}\n"
        f"شماره تماس: {phone}\n"
        f"محصول: {item_name}\n"
        f"تعداد: {quantity}\n"
        f"توضیحات: {note}\n"
    )

    send_email("سفارش جدید بارنیکو", body)

    return JSONResponse({
        "success": True,
        "message": "سفارش ثبت شد و برای مدیر ایمیل شد"
    })
