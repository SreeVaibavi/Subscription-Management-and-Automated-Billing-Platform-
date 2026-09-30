# BillWise — Subscription Management & Automated Billing Platform

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-8b5cf6?style=for-the-badge&logo=github)](https://sreevaibavi.github.io/Subscription-Management-and-Automated-Billing-Platform-/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

> A modern, decoupled automated billing engine and cloud services subscription platform. Built with real-time micro-metering, sub-second proration, invoice lifecycle management, mock bank checkout, and role-based customer & admin dashboards.

---

## 🌐 Live Interactive Demo (GitHub Pages)

Experience the entire platform live in your browser with interactive state persistence and simulated transactions:

👉 **[Launch Live Demo on GitHub Pages](https://sreevaibavi.github.io/Subscription-Management-and-Automated-Billing-Platform-/)**

### 🔑 1-Click Quick Demo Access

You can click the 1-click quick access buttons on the Sign In page or use these credentials:

| Role | Email | Password | Direct Dashboard |
| :--- | :--- | :--- | :--- |
| **👑 Admin** | `harshdeep@admin.com` | `adminpassword` | `dashboardadmin.html` |
| **👤 Customer** | `customer@billwise.io` | `password123` | `dashboardcustomer.html` |

*Note: You can also register a new account on the signup form. All user data, plan customizations, subscription adjustments, and invoice payments interactively persist in browser storage.*

---

## ✨ Key Features

### 👤 Customer Experience
- **Interactive Cloud Provisioning Console**: Real-time meters for vCPU, NVMe disk allocations, RAM, and bandwidth.
- **Subscription Lifecycle**: Instant plan upgrades/downgrades with automated proration preview, pause/resume, and cancellation flows.
- **Invoice & Checkout System**: Real-time invoice statuses (`OPEN`, `PAID`), simulated payment gateway checkout modal, and client-side instant PDF invoice generation.
- **Alerts & In-App Notifications**: Real-time badge counters and notification feeds for billing events and renewal milestones.

### 👑 Admin Management
- **Revenue & Growth Metrics**: Real-time MRR (Monthly Recurring Revenue), total collected billing volume, and active subscriber metrics.
- **Dynamic Plan Editor**: Create, edit monthly pricing, and delete subscription tiers on the fly.
- **Customer Directory**: Complete customer registry with avatars, joined dates, and subscription statuses.
- **Master Billing Ledger**: Cross-platform invoice history and subscription status monitoring.

---

## 🏗️ Architecture & Technology Stack

- **Frontend**: Responsive modern UI built with semantic HTML5, modern CSS3 design tokens (Inter & JetBrains Mono typography), Lucide icons, and Chart.js analytics.
- **Interactive Demo Layer (`mock-api.js`)**: Intelligent client-side API simulation engine supporting complete CRUD, session auth, PDF generator, and bank payment workflows on static hosts like GitHub Pages.
- **Backend (Local / Production)**: Python FastAPI with SQLAlchemy ORM, PostgreSQL connection pools, Alembic migrations, Celery task workers with Redis broker, and ReportLab PDF rendering.

---

## 🚀 Running Locally with Python Backend

If you wish to run the full FastAPI backend with PostgreSQL locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SreeVaibavi/Subscription-Management-and-Automated-Billing-Platform-.git
   cd Subscription-Management-and-Automated-Billing-Platform-
   ```

2. **Set up virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file or adjust existing settings with your PostgreSQL connection string.

4. **Launch the FastAPI API Server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

5. **Open `index.html` or visit `http://127.0.0.1:8000`** in your browser.

---

## ⚙️ Enabling GitHub Pages on this Repository

If GitHub Pages is not already publishing automatically:
1. Go to your repository on GitHub: **[SreeVaibavi/Subscription-Management-and-Automated-Billing-Platform-](https://github.com/SreeVaibavi/Subscription-Management-and-Automated-Billing-Platform-)**
2. Click **Settings** (top navigation tab).
3. In the left sidebar, click **Pages**.
4. Under **Build and deployment** -> **Source**:
   - Choose **GitHub Actions** (recommended, uses the included `.github/workflows/deploy.yml` workflow)
   - OR select **Deploy from a branch** -> Branch: `main` / Folder: `/ (root)` and click **Save**.
5. Your live site will be ready at:
   **`https://sreevaibavi.github.io/Subscription-Management-and-Automated-Billing-Platform-/`**