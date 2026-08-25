import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_SENDER = os.getenv("SMTP_SENDER", "ebnalnasirs13@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "Sk_barniko12")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "barniko2017@gmail.com")

orders = []

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

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    menu_items = [
        {"name": "اسپرسو تک", "price": "۹۹٬۰۰۰ تومان"},
        {"name": "اسپرسو دبل", "price": "۱۶۶٬۰۰۰ تومان"},
        {"name": "آمریکانو", "price": "۱۷۷٬۰۰۰ تومان"},
        {"name": "ترک", "price": "۱۸۰٬۰۰۰ تومان"},
        {"name": "لاته", "price": "۲۲۲٬۰۰۰ تومان"},
        {"name": "موکا", "price": "۲۵۲٬۰۰۰ تومان"},
        {"name": "هات چاکلت", "price": "۲۲۲٬۰۰۰ تومان"},
        {"name": "هات چاکلت بارنیکو", "price": "۲۵۲٬۰۰۰ تومان"},
        {"name": "شیر عسل", "price": "۱۸۰٬۰۰۰ تومان"},
        {"name": "شیر نسکافه", "price": "۲۲۲٬۰۰۰ تومان"},
        {"name": "آیس آمریکانو", "price": "۱۷۷٬۰۰۰ تومان"},
        {"name": "آیس لاته", "price": "۲۲۲٬۰۰۰ تومان"},
        {"name": "آیس موکا", "price": "۲۵۲٬۰۰۰ تومان"},
        {"name": "آفوگاتو", "price": "۲۲۲٬۰۰۰ تومان"},
        {"name": "کافی جو", "price": "۲۲۲٬۰۰۰ تومان"},
        {"name": "کوک اسپرسو", "price": "۲۲۲٬۰۰۰ تومان"},
        {"name": "سیروپ", "price": "۴۴٬۰۰۰ تومان"},
        {"name": "دمنوش لبخند", "price": "۱۷۷٬۰۰۰ تومان"},
        {"name": "دمنوش انرژی", "price": "۱۷۷٬۰۰۰ تومان"},
        {"name": "دمنوش آرامش", "price": "۱۷۷٬۰۰۰ تومان"},
        {"name": "دمنوش ترش", "price": "۱۷۷٬۰۰۰ تومان"},
        {"name": "تک دمنوش", "price": "۱۶۶٬۰۰۰ تومان"},
        {"name": "دمنوش بسپارش به من", "price": "۱۷۷٬۰۰۰ تومان"},
        {"name": "چای ماسالا دمی", "price": "۲۲۲٬۰۰۰ تومان"},
        {"name": "چای مراکشی", "price": "۱۷۷٬۰۰۰ تومان"},
        {"name": "چای سیاه + یک طعم", "price": "۹۹٬۰۰۰ / ۱۱۹٬۰۰۰ تومان"},
        {"name": "قوری چای + یک طعم", "price": "۲۵۵٬۰۰۰ / ۲۶۶٬۰۰۰ تومان"},
        {"name": "قوری دمنوش ترکیبی", "price": "۳۳۳٬۰۰۰ تومان"},
        {"name": "نشاط", "price": "۱۶۶٬۰۰۰ تومان"},
        {"name": "آرامش", "price": "۱۶۶٬۰۰۰ تومان"},
        {"name": "انرژی", "price": "۱۶۶٬۰۰۰ تومان"},
        {"name": "بهشت", "price": "۱۶۶٬۰۰۰ تومان"},
        {"name": "نعنا لیمو", "price": "۱۶۶٬۰۰۰ تومان"},
        {"name": "خنک کننده", "price": "۱۶۶٬۰۰۰ تومان"},
        {"name": "سکنجبین خیار", "price": "۱۹۹٬۰۰۰ تومان"},
        {"name": "فالوده سیب", "price": "۱۹۹٬۰۰۰ تومان"},
        {"name": "قره یی", "price": "۱۹۹٬۰۰۰ تومان"},
        {"name": "بسپارش به من", "price": "۱۶۶٬۰۰۰ تومان"},
        {"name": "شیک بارنیکو", "price": "۳۳۳٬۰۰۰ تومان"},
        {"name": "شیک موز و بادام زمینی", "price": "۲۸۹٬۰۰۰ تومان"},
        {"name": "شیک موز و شکلات", "price": "۲۸۹٬۰۰۰ تومان"},
        {"name": "شیک موز و کارامل", "price": "۲۸۹٬۰۰۰ تومان"},
        {"name": "شیک موز و نسکافه", "price": "۲۸۹٬۰۰۰ تومان"},
        {"name": "بلوهاوایی", "price": "۲۴۲٬۰۰۰ تومان"},
        {"name": "موهیتو", "price": "۲۲۲٬۰۰۰ تومان"},
        {"name": "لیموناد", "price": "۲۲۲٬۰۰۰ تومان"},
        {"name": "فيله و ژامبون", "price": "۴۴۴٬۰۰۰ تومان"},
        {"name": "مرغ و قارچ", "price": "۳۹۵٬۰۰۰ تومان"},
        {"name": "پپرونی", "price": "۳۹۵٬۰۰۰ تومان"},
        {"name": "ژامبون تنورى", "price": "۳۶۹٬۰۰۰ تومان"},
        {"name": "هات داگ با پنیر چدار", "price": "۲۹۵٬۰۰۰ تومان"},
        {"name": "هات داگ مخصوص", "price": "۳۹۵٬۰۰۰ تومان"},
        {"name": "سوسيس كوكتل با پنیر چدار", "price": "۲۹۵٬۰۰۰ تومان"},
        {"name": "سوسيس كوكتل مخصوص", "price": "۳۹۵٬۰۰۰ تومان"},
        {"name": "سيب زمينى", "price": "۲۷۰٬۰۰۰ تومان"},
        {"name": "سيب زمينى پنیری", "price": "۳۶۰٬۰۰۰ تومان"},
        {"name": "سيب زمينى پنیری و ژامبون", "price": "۴۵۰٬۰۰۰ تومان"},
        {"name": "سينى فيله و سبزيجات", "price": "۵۹۹٬۰۰۰ تومان"},
        {"name": "سينى فيله و سيب زمينى", "price": "۵۹۹٬۰۰۰ تومان"},
        {"name": "هات چیپس", "price": "۸۹۹٬۰۰۰ تومان"},
        {"name": "پاستا پنه مرغ و قارچ", "price": "۵۹۹٬۰۰۰ تومان"},
        {"name": "كشک و بادمجان", "price": "۳۳۳٬۰۰۰ تومان"},
        {"name": "املت رب", "price": "۲۵۵٬۰۰۰ تومان"},
        {"name": "املت گوجه", "price": "۲۸۵٬۰۰۰ تومان"},
        {"name": "املت قارچ", "price": "۳۳۳٬۰۰۰ تومان"},
        {"name": "تخم مرغ تره", "price": "۱۹۹٬۰۰۰ تومان"},
        {"name": "تخم مرغ شنبلیله", "price": "۱۹۹٬۰۰۰ تومان"},
        {"name": "نيمرو", "price": "۱۹۹٬۰۰۰ تومان"},
        {"name": "سوسيس نيمرو", "price": "۲۹۹٬۰۰۰ تومان"},
        {"name": "سوسيس املت", "price": "۳۳۳٬۰۰۰ تومان"},
    ]
    return templates.TemplateResponse("index.html", {"request": request, "menu_items": menu_items})

@app.get("/api/orders")
async def get_orders():
    return {"orders": orders}

@app.post("/api/order")
async def create_order(
    customer_name: str = Form(...),
    phone: str = Form(...),
    items: str = Form(...),
    note: str = Form("")
):
    body = (
        f"سفارش جدید ثبت شد\n\n"
        f"نام مشتری: {customer_name}\n"
        f"شماره تماس: {phone}\n"
        f"اقلام: {items}\n"
        f"توضیحات: {note}\n"
    )

    order = {
        "customer_name": customer_name,
        "phone": phone,
        "items": items,
        "note": note,
        "confirmed": False
    }
    orders.append(order)

    send_email("سفارش جدید", body)

    return JSONResponse({"success": True, "message": "سفارش ثبت شد"})

@app.post("/api/confirm")
async def confirm_order(
    customer_name: str = Form(...),
    phone: str = Form(...)
):
    for order in orders:
        if order["customer_name"] == customer_name and order["phone"] == phone:
            order["confirmed"] = True
            return {"success": True, "message": "سفارش تایید شد"}
    return {"success": False, "message": "سفارشی پیدا نشد"}
