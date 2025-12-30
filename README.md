# stas-backend

This project contains a Django REST API (backend) and a Vue 3 + Vite SPA (frontend) for the storefront. Run the backend and frontend separately during development.

## Backend (Django)
1. Create and activate a virtual environment (Python 3.11+ recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   .\venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Apply migrations and create a superuser for the Django admin:
   ```bash
   python backend/manage.py migrate
   python backend/manage.py createsuperuser
   ```
4. Start the API on port 8000:
   ```bash
   python backend/manage.py runserver 0.0.0.0:8000
   ```
   - Admin panel: http://localhost:8000/admin/
   - API base: http://localhost:8000/api/
   - Media files (product images) served from http://localhost:8000/media/

## Frontend (Vue 3 + Vite)
1. Create a frontend environment file `frontend/.env.local` to point the app at the Django API:
   ```bash
   VITE_API_BASE=http://localhost:8000/api/
   VITE_BACKEND_ORIGIN=http://localhost:8000
   ```
2. Install dependencies (Node 18+ recommended):
   ```bash
   cd frontend
   npm install
   ```
3. Run the dev server (opens on http://localhost:5173 by default):
   ```bash
   npm run dev -- --host
   ```
   Vite is already allowed by CORS in the Django settings (`http://localhost:5173`).

## Running both together
- Start the backend first so the frontend can call `http://localhost:8000/api/`.
- With both servers running, you can browse the storefront at http://localhost:5173/ and use the admin panel at http://localhost:8000/admin/.

## Быстрый старт (коротко, по-русски)
1. **Backend**
   - Создайте окружение и поставьте зависимости: `python -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt`.
   - Примените миграции и создайте админа: `python backend/manage.py migrate && python backend/manage.py createsuperuser`.
   - Запустите API: `python backend/manage.py runserver 0.0.0.0:8000`.
2. **Frontend**
   - Создайте `frontend/.env.local` со строками:
     ```bash
     VITE_API_BASE=http://localhost:8000/api/
     VITE_BACKEND_ORIGIN=http://localhost:8000
     ```
   - Установите зависимости и запустите дев-сервер: `cd frontend && npm install && npm run dev -- --host`.
3. **Проверка**
   - Магазин и фильтры: http://localhost:5173/
   - Админ-панель (редактирование товаров): http://localhost:8000/admin/
   - Медиа для картинок: http://localhost:8000/media/