# साझा समस्या — Sajha Samasya

A civic complaint and tracking platform for Nepal — where citizens can report local problems (water, roads, electricity, waste) and communities can upvote issues affecting them.

> **"ChatGPT can answer general questions, but it can't tell you that Ward 5's water hasn't come in 3 days. Only locals know that."**

---

## 🌟 Features

- 📝 **Report Problems** — Submit complaints with photo, GPS location, category
- 🗺️ **Map View** — See all complaints on an interactive map (Leaflet + OpenStreetMap)
- 👍 **Community Upvoting** — "+1 I have the same problem in my ward"
- 📊 **Dashboard** — Ward/district/category wise statistics
- 🇳🇵 **Nepali/English** — Full bilingual support with one-click toggle
- 📍 **Nepal Location Data** — All 7 provinces, 77 districts, 750+ municipalities, 6000+ wards
- 🔌 **REST API** — Full DRF API for mobile app integration
- 🔐 **Auth** — Register, login, logout

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.x |
| API | Django REST Framework |
| Database | PostgreSQL (production) / SQLite (dev) |
| Maps | Leaflet.js + OpenStreetMap |
| Frontend | Django Templates + Vanilla JS |
| Auth | Django built-in auth |
| Deploy | Railway |

---

## 🚀 Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/sajha-samasya.git
cd sajha-samasya
```

### 2. Virtual environment banau
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Dependencies install gar
```bash
pip install -r requirements.txt
```

### 4. `.env` file banau
```bash
# Project root ma .env file banau
SECRET_KEY=your_secret_key_here
DEBUG=True
```

### 5. Database setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Nepal data seed gar
```bash
python seed_full.py
```

### 7. Server run gar
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 📡 API Endpoints

### Complaints
```
GET    /api/complaints/              → List all complaints (with filters)
POST   /api/complaints/              → Create new complaint (auth required)
GET    /api/complaints/<id>/         → Complaint detail
PUT    /api/complaints/<id>/         → Update complaint
DELETE /api/complaints/<id>/         → Delete complaint
POST   /api/complaints/<id>/upvote/  → Toggle upvote (auth required)
```

### Location
```
GET /api/provinces/                          → All 7 provinces
GET /api/districts/?province_id=1            → Districts by province
GET /api/municipalities/?district_id=1       → Municipalities by district
GET /api/wards/?municipality_id=1            → Wards by municipality
```

### Stats
```
GET /api/stats/   → Total complaints, by category, top districts
```

### Map Data
```
GET /api/map-data/   → All complaints with GPS coordinates
```

### Query Filters
```
GET /api/complaints/?category=water
GET /api/complaints/?status=open
GET /api/complaints/?district=Kathmandu
GET /api/complaints/?ward_id=5
```

---

## 📁 Project Structure

```
sajha-samasya/
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── complaints/
│   ├── models.py          ← Province, District, Municipality, Ward, Complaint, Upvote
│   ├── views.py           ← Web views + REST API views
│   ├── serializers.py     ← DRF serializers
│   ├── urls.py            ← URL routing
│   ├── admin.py           ← Admin panel config
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── map.html
│       ├── dashboard.html
│       ├── complaint_detail.html
│       ├── submit_complaint.html
│       ├── login.html
│       └── register.html
├── seed_full.py           ← Nepal full data seeder
├── requirements.txt
├── .env                   ← Not committed (secret keys)
├── .gitignore
└── manage.py
```

---

## 🗄️ Data Models

```
Province (7)
  └── District (77)
        └── Municipality (750+)
              └── Ward (6000+)
                    └── Complaint
                          └── Upvote
```

---

## 🎯 Why This Project?

Nepal ma ward/municipality notices ra civic complaints:
- Facebook page ma post hunchha — sabai le dekhidainan
- Hoarding board ma — digital xaina  
- Ward office ma — physically januparchha

**Sajha Samasya** = one platform for everything. Real community-generated data that AI cannot replace — because only locals know their ward's problems.

---

## 🔮 Roadmap

- [ ] Ward admin role — notices post garna milxa
- [ ] SMS notifications (Sparrow SMS)
- [ ] Mobile app (Flutter)
- [ ] Government/municipality dashboard
- [ ] Complaint status tracking with timeline

---

## 👨‍💻 Developer

Built with ❤️ for Nepal's civic tech ecosystem.

---

## 📄 License

MIT License