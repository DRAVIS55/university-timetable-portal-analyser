

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail  # Optional if you want to send email
from .models import ContactMessage



def personal_profile(request):
    html = """
    <html><head><title>Personal Profile</title></head><body style="font-family:sans-serif; text-align:center; background:#111; color:#eee;">
      <h1>Personal Profile</h1>
      <p>Hi there, I'm <strong>Macharia Samuel Kibunja</strong> (alias: DRAVIS55), a passionate Full-Stack Developer specializing in Django, Next.js, software engineering, cybersecurity, and AI. I hold a BSc in Computer Science from Chuka University.</p>
      <a href="/" style="color:#08c5ff; text-decoration:none;">Return Home</a>
    </body></html>
    """
    return HttpResponse(html)

def education(request):
    html = """
    <html><head><title>Education Background</title></head><body style="font-family:sans-serif; text-align:center; background:#111; color:#eee;">
      <h1>Education Background</h1>
      <p>I earned my BSc in Computer Science from Chuka University.</p>
      <a href="/" style="color:#08c5ff; text-decoration:none;">Return Home</a>
    </body></html>
    """
    return HttpResponse(html)

def skills(request):
    html = """
    <html><head><title>Tech Skills</title></head><body style="font-family:sans-serif; text-align:center; background:#111; color:#eee;">
      <h1>Tech Skills</h1>
      <ul style="list-style:none; line-height:1.5; display:inline-block; text-align:left;">
        <li>Languages: Python, JavaScript, TypeScript, C++, C#, SQL</li>
        <li>Backend: Django, Django REST Framework, FastAPI, PostgreSQL, MySQL, Firebase</li>
        <li>Frontend: Next.js, React.js, Tailwind CSS, Redux</li>
        <li>Mobile: Android (Java/Kotlin), React Native</li>
        <li>Databases: PostgreSQL, MySQL, SQLite, pgAdmin</li>
        <li>Blockchain: Smart Contracts, Web3.js, Solidity</li>
        <li>API: REST, GraphQL, Netflix API</li>
        <li>Cybersecurity & AI: Ethical Hacking, Machine Learning, Neural Networks</li>
        <li>Tools: Docker, Git, Linux (Arch), Nginx, AWS, DigitalOcean</li>
      </ul>
      <a href="/" style="color:#08c5ff; text-decoration:none;">Return Home</a>
    </body></html>
    """
    return HttpResponse(html)

def experience(request):
    html = """
    <html><head><title>Experiences</title></head><body style="font-family:sans-serif; text-align:center; background:#111; color:#eee;">
      <h1>Experiences</h1>
      <p>As a Full-Stack Developer, I've built scalable applications using Django, React, Next.js, and mobile technologies. I'm actively enhancing my work in cybersecurity and AI, including development of a Loan Management System with Django & Chart.js.</p>
      <a href="/" style="color:#08c5ff; text-decoration:none;">Return Home</a>
    </body></html>
    """
    return HttpResponse(html)

def projects(request):
    html = """
    <html><head><title>Projects</title></head><body style="font-family:sans-serif; text-align:center; background:#111; color:#eee;">
      <h1>Projects</h1>
      <p>Here are some repositories from my GitHub profile (<a href="https://github.com/dravis55" style="color:#08c5ff;">DRAVIS55</a>):</p>
      <ul style="list-style:none; line-height:1.5; display:inline-block; text-align:left;">
        <li>JAVA-projects — Java templates and implementations</li>
        <li>django-web-developmentbasic-shoplenty — Basic HTML template for Django web shop</li>
        <li>django-web-development-backend-basic — Django back-end starter</li>
        <li>django-web-development-full-stack-development — Full-stack Django starter</li>
        <li>portal-django-website — Website system for a higher-education learning institution</li>
        <li>html-js-and-css-calculator — Basic calculator implementation using HTML, JS and CSS</li>
      </ul>
      <a href="/" style="color:#08c5ff; text-decoration:none;">Return Home</a>
    </body></html>
    """
    return HttpResponse(html)

def references(request):
    html = """
    <html><head><title>References</title></head><body style="font-family:sans-serif; text-align:center; background:#111; color:#eee;">
      <h1>References</h1>
      <p>References available upon request.</p>
      <a href="/" style="color:#08c5ff; text-decoration:none;">Return Home</a>
    </body></html>
    """
    return HttpResponse(html)

def contact(request):
    html = """
    <html><head><title>Contact Info</title></head><body style="font-family:sans-serif; text-align:center; background:#111; color:#eee;">
      <h1>Contact Info</h1>
      <p>Email: samuelkibunja55@gmail.com | dravislotum@gmail.com</p>
      <p>Phone / WhatsApp: 0714026439 | 0758067458</p>
      <p>LinkedIn: <a href="https://www.linkedin.com/in/samuelkibunja" style="color:#08c5ff;">in/samuelkibunja</a></p>
      <p>Twitter: <a href="https://x.com/Dravis55" style="color:#08c5ff;">@Dravis55</a></p>
      <a href="/" style="color:#08c5ff; text-decoration:none;">Return Home</a>
    </body></html>
    """
    return HttpResponse(html)


def about_us(request):
    html_content = """
    <html>
    <head>
        <title>About DravTech</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #111;
                color: #eee;
                text-align: center;
                padding: 40px;
            }
            h1 { color: #08c5ff; }
            p { max-width: 700px; margin: auto; line-height: 1.6; }
            .btn {
                display: inline-block;
                background: #08c5ff;
                color: #000;
                padding: 10px 20px;
                border-radius: 8px;
                text-decoration: none;
                margin-top: 20px;
                transition: 0.3s;
            }
            .btn:hover { background: #0ee066; color: #fff; }
        </style>
    </head>
    <body>
        <h1>About DravTech</h1>
        <p>
            DravTech is a technology company founded by <strong>Samuel Kibunja (Dravis)</strong>, 
            dedicated to delivering world-class IT solutions. Our mission is to provide
            innovative, customer-driven services across software development, 
            networking, and emerging technologies.
        </p>
        <p>
            Over the years, DravTech has built a reputation for delivering scalable,
            secure, and efficient systems. We believe in combining expertise and passion
            to create solutions that solve real-world problems.
        </p>
        <a href="/" class="btn">Return Home</a>
    </body>
    </html>
    """
    return HttpResponse(html_content)



from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ContactMessage


# Existing views ...

def clear_messages(request):
    if request.method == "POST":
        ContactMessage.objects.all().delete()
        return redirect("admin_messages")  # Redirect back to the messages panel


# Home page with contact form
def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )
            return HttpResponse("<h2>Message Sent Successfully!</h2><a href='/'>Return Home</a>")

    return render(request, "index.html")

# Admin panel to view messages
def admin_messages(request):
    messages = ContactMessage.objects.all().order_by("-created_at")
    return render(request, "admin_messages.html", {"messages": messages})
