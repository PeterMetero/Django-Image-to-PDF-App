# Image to PDF Converter

A Django web app that combines PNG and JPEG images into a downloadable PDF. Select up to 30 images, drag them into the order you want, and convert them in your browser.

## Requirements

- Python 3.10 or newer
- pip

The Python packages are listed in `requirements.txt`.

## Run locally on Windows

Open PowerShell in the project folder:

```powershell
cd "C:\Users\Admin\Desktop\Image to PDF DJANGO App"
```

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, you can run the environment's Python directly as shown below instead.

Install dependencies, create database migrations, and start the development server:

```powershell
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

If you did not activate the virtual environment, replace `python` with:

```powershell
.\.venv\Scripts\python.exe
```

For example:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser. Keep the terminal open while using the app; press **Ctrl+C** to stop the server.

## Using the app

1. Choose PNG or JPEG images.
2. Drag the thumbnails into the order you want in the PDF.
3. Select **Convert to PDF** and use the download link when conversion finishes.

The app accepts up to 30 images per conversion. Converted PDFs and uploaded images are stored under `media/pdfs/` and `media/uploads/`, respectively.

## Project structure

```text
core/                 Conversion view, URL routes, model, and migrations
pdf_converter/        Django project settings and URL configuration
static/               CSS and other static assets
templates/core/       Converter page
manage.py             Django management entry point
requirements.txt      Python dependencies
```

## API

`POST /api/convert` accepts multipart form data containing one or more `images` file fields and optional repeated `order` fields containing image filenames in the desired order.

On success, the endpoint returns JSON with `success: true` and a `pdf_url`. Invalid methods, missing files, or more than 30 files return an error response.

## Notes

- The default settings are for local development. Before deploying publicly, configure a production secret key, `DEBUG`, `ALLOWED_HOSTS`, HTTPS, and suitable media-file storage and serving.
- `gunicorn` is included in the requirements for WSGI serving, but the included development settings are not production-ready.
