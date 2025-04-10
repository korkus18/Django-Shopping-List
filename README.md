````markdown
# 🍎 Django Shopping List

Jednoduchá webová aplikace pro správu nákupního seznamu, vytvořená v Django.

## 📦 Funkce
- Přidávání položek do nákupního seznamu
- Označení položek jako "koupené"
- Mazání položek
- Uživatelské rozhraní postavené na Django templates

---

## ⚙️ Lokální spuštění

### 1. Klonuj nebo stáhni projekt

```bash
git clone https://github.com/korkus18/Django-Shopping-List.git
cd shoppping_list-list
```

> Pokud máš ZIP, tak ho stačí rozbalit a přejít do složky.

---

### 2. Vytvoř a aktivuj virtuální prostředí

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

---

### 3. Nainstaluj závislosti

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Migrace databáze

```bash
python manage.py migrate
```

---

### 5. Vytvoř admin účet

```bash
python manage.py createsuperuser
```

Zadej jméno, e-mail a heslo.

---

### 6. Spusť server

```bash
python manage.py runserver
```

Otevři [http://127.0.0.1:8000](http://127.0.0.1:8000) ve svém prohlížeči.

---

## 💡 Tipy

- Admin rozhraní: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## 📁 Struktura

```
django-shopping-list/
│
├── shopping_list/         # Aplikace s nákupním seznamem
├── shopping_project/      # Projektové nastavení
├── db.sqlite3             # SQLite databáze
├── requirements.txt
└── manage.py
```

---

