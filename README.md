# eCommerce Store Application

## Project information

This Django eCommerce project was developed for the HyperionDev Web Development Bootcamp. It supports buyer and vendor accounts, store and product management, a session-based shopping cart, checkout, product reviews, password reset pages, Django Admin, and REST API endpoints.

The default database is **MariaDB**. Configuration values and secrets are loaded from a local `.env` file; `.env` is ignored by Git so credentials are not committed.

## Technology

- Python 3.10 or newer
- Django 4.2
- Django REST Framework
- MariaDB 10.6 or newer
- HTML, CSS, and Bootstrap

## Sequence diagrams

The corrected Store, Buyer, and Review interaction sequences are available as an editable, three-page [draw.io diagram](docs/ecommerce_sequence_diagrams.drawio) and in [Mermaid Markdown](docs/sequence_diagrams.md). They replace the unrelated external-post/Reddit-style interaction diagram.

## Step-by-step installation

The commands below assume Git, Python, and MariaDB are installed. Replace `YOUR_REPOSITORY_URL` with the URL supplied for this project.

### 1. Clone the project and enter its folder

```bash
git clone YOUR_REPOSITORY_URL ecommerce_app_3
cd ecommerce_app_3
```

If you received a ZIP instead, extract it and run `cd ecommerce_app_3` from the folder containing `manage.py`.

### 2. Create and activate a virtual environment

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

When activation succeeds, the terminal prompt normally starts with `(.venv)`.

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `mysqlclient` cannot build, install the MariaDB development package first. On Ubuntu/Debian use `sudo apt install libmariadb-dev pkg-config`; on macOS with Homebrew use `brew install mariadb-connector-c pkg-config`.

### 4. Start MariaDB and create the database

Open the MariaDB console as an administrator:

```bash
mariadb -u root -p
```

At the `MariaDB>` prompt, copy and paste the following SQL. Replace the example password in both this command and the `.env` file created in the next step.

```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'replace-with-a-strong-database-password';
CREATE USER 'ecommerce_user'@'127.0.0.1' IDENTIFIED BY 'replace-with-a-strong-database-password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'127.0.0.1';
FLUSH PRIVILEGES;
EXIT;
```

### 5. Create the environment configuration

macOS or Linux:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Open `.env` in a text editor. Set `DB_PASSWORD` to the MariaDB password used above and replace `DJANGO_SECRET_KEY`. To generate a key, run:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Paste the printed value after `DJANGO_SECRET_KEY=`. The final file should contain:

```dotenv
DJANGO_SECRET_KEY=your-generated-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=your-mariadb-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Do not commit `.env` because it contains secrets. The safe `.env.example` file documents every required variable.

### 6. Check the project and create the database tables

```bash
python manage.py check
python manage.py migrate
```

Optional: create an administrator account for `/admin/`:

```bash
python manage.py createsuperuser
```

Optional: if you were given fixture data and want to import it:

```bash
python manage.py loaddata database_backup.json
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in a browser. The admin site is at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and the API begins at [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/).

Stop the server with `Ctrl+C`. Activate `.venv` again whenever you open a new terminal before running project commands.

## Database configuration

MariaDB is configured directly as Django's default database in `ecommerce_app/settings.py`. The application reads its database name, user, password, host, and port from `.env`. It does not silently fall back to SQLite.

SQLite can be used only as an intentional local alternative by replacing the `DATABASES` value in `ecommerce_app/settings.py` with Django's SQLite configuration; MariaDB remains the submitted/default implementation.

## Template organisation

Shared project templates are limited to `templates/base.html` and `templates/authentication/`. Store-owned templates are namespaced under `store/templates/store/` and grouped into `buyer`, `cart`, `integrations`, `orders`, `products`, `reviews`, and `stores` folders.

## Author

William Santos
