# 📚 StudyBuddy - Django Web App

**StudyBuddy** is a full-stack Django application that allows users to join discussion rooms, post messages, upload files, and collaborate in real-time. It includes powerful features like email/password and social authentication (Google & GitHub), password reset via email, user profiles, topic filtering, and media uploads.

---

## 🚀 Features

✅ **User Authentication**
- Register/login using email and password
- Social login via **Google** and **GitHub**
- Secure password reset via email with reset password link (valid for 10 minutes)

✅ **User Profiles**
- Update profile picture, name, bio, and email
- View other users’ profiles with rooms created

✅ **Room Management**
- Create, update, and delete discussion rooms
- Assign topics to rooms
- Join discussions as a participant

✅ **Chat Functionality**
- Post messages in rooms
- Upload media (images, audio, video, PDFs – up to 10MB)
- Delete your own messages and attached files

✅ **Search & Browse**
- Filter rooms by topic, name, or description
- Browse all available topics

✅ **Responsive UI**
- Clean, mobile-friendly interface using custom CSS and media queries

---

## 🛠️ Technologies Used

- **Backend**: Django 5.2  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**: SQLite (for development)  
- **Email**: Gmail SMTP  
- **OAuth**: Google & GitHub (via `django-allauth`)  
- **File Handling**: Django FileField + Media  
- **Hosting**: [PythonAnywhere](https://www.pythonanywhere.com/) (for deployment)

---

## 🔒 Environment Variables

Rename `.env.example` to `.env` and add your credentials:

```ini
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

OAUTH_GOOGLE_CLIENT_ID=your-google-client-id
OAUTH_GOOGLE_SECRET=your-google-secret

OAUTH_GITHUB_CLIENT_ID=your-github-client-id
OAUTH_GITHUB_SECRET=your-github-secret
