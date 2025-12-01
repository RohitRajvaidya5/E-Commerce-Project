# E‑Commerce Project 🛒

**E‑Commerce Project** — a full‑stack Django e‑commerce web app with product listing, cart, checkout, and payment via Razorpay — built with Django, TailwindCSS & DaisyUI.

**Live at:** `https://e‑commerce‑project‑yb1q.onrender.com/`  
**Repository:** https://github.com/RohitRajvaidya5/E‑Commerce‑Project

---

## 📦 Features

- User authentication (signup/login/logout)  
- User profile (with optional photo upload)  
- Product listing and detail pages  
- Cart functionality (add items, update quantity, remove items)  
- Checkout flow with Razorpay integration  
- Order processing, tax calculation, and order records  
- Responsive UI using Tailwind + DaisyUI  
- Clean UI components: loaders, buttons, navigation, modals  

---

## 🛠 Tech Stack

| Layer        | Technology                      |
|--------------|----------------------------------|
| Backend      | Django (Python)                  |
| Frontend     | TailwindCSS + DaisyUI + HTML/CSS |
| Payments     | Razorpay Checkout                |
| Deployment   | Render.com                       |

---

## 📁 Project Structure (partial)

```
├── accounts/        # user & profile related code
├── products/        # product models, views, templates
├── orders/          # order models, views, payment logic
├── templates/       # base templates, UI shared layout
├── static/          # static files (css/js/images)
├── manage.py
├── requirements.txt
└── README.md        # ← you are here
```

---

## 🚀 Setup & Local Development

1. Clone the repo  
   ```bash
   git clone https://github.com/RohitRajvaidya5/E‑Commerce‑Project.git
   cd E‑Commerce‑Project
   ```  
2. Create & activate virtual environment  
   ```bash
   python -m venv env
   source env/bin/activate   # Windows: env\Scriptsctivate
   ```  
3. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```  
4. Set environment variables (e.g. in `.env`)  
   ```env
   SECRET_KEY=your_django_secret
   DEBUG=True
   RAZORPAY_KEY_ID=your_key_id
   RAZORPAY_KEY_SECRET=your_secret
   ```  
5. Run database migrations  
   ```bash
   python manage.py migrate
   ```  
6. Run server  
   ```bash
   python manage.py runserver
   ```  

---

## 💳 Razorpay Configuration (production)

Before deploying or switching to live mode:

- Add your live keys to environment variables  
- In Razorpay dashboard, set **Allowed Origins / Return URLs** to your domain, e.g.:  
  `https://e‑commerce‑project‑yb1q.onrender.com/checkout/`  
- Ensure your site is served over HTTPS  

---

## 🚀 Deployment (on Render)

1. Push code to GitHub  
2. On Render, create a new Web Service linked to this repo  
3. Add environment variables (`SECRET_KEY`, `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, etc.)  
4. Use default start command:  
   ```bash
   gunicorn <project_name>.wsgi:application
   ```  
5. Enable auto‑deploy for future pushes  

---

## 🧪 Testing & Usage

- Register a new user or log in  
- Browse products → add them to cart → checkout → complete payment via Razorpay  
- After payment success, order should be created; verify in admin or check order list  

---

## 🔐 Security & Good Practices

- Never commit `SECRET_KEY` or Razorpay secrets — use env variables  
- Set `DEBUG=False` in production  
- Properly configure `ALLOWED_HOSTS` to your domain  

---

## 🙋 Contributing

Contributions are welcome! Feel free to fork, open issues or submit pull requests.

---

## 📄 License

This project is open source. Use, modify, and distribute freely.
