# Legal Compliance Management Module



A comprehensive Odoo module for tracking legal compliance requirements across tax, HR, safety, and other regulatory areas.

---

## 🚀 Features

- 📋 **Rule Management**: Create and categorize compliance rules with priorities.
- 🔄 **Recurring Checks**: Schedule automatic compliance checks (daily/weekly/monthly).
- 📂 **Document Proofs**: Attach supporting documents for audits.
- 🔔 **Alerts & Notifications**: Get automatic reminders for upcoming checks.
- 📊 **Dashboard**: Visual overview of compliance status.
- 📈 **Reporting**: Track compliance history and results.

---

## 📂 Code Structure

```
legal_compliance/
├── __init__.py
├── __manifest__.py
├── README.md
│
├── controllers/
│   ├── __init__.py
│   └── controllers.py        # Web controllers for dashboards/API
│
├── data/
│   └── compliance_data.xml   # Default data, email templates, sequences
│
├── demo/
│   └── demo.xml              # Demonstration data
│
├── models/
│   ├── __init__.py
│   ├── compliance_category.py
│   ├── compliance_rule.py
│   ├── compliance_check.py
│   ├── compliance_document.py
│   └── res_config_settings.py # Configuration settings
│
├── security/
│   ├── ir.model.access.csv   # Access rights
│   └── security_rules.xml    # User groups
│
├── static/
│   ├── description/
│   │   └── icon.png          # Module icon
│   └── src/
│       ├── css/
│       │   └── compliance.css
│       └── js/
│           └── compliance.js
│
└── views/
    ├── compliance_alert_views.xml
    ├── compliance_category_views.xml
    ├── compliance_check_views.xml
    ├── compliance_document_views.xml
    ├── compliance_rule_views.xml
    ├── menu_views.xml
    ├── res_config_settings_views.xml
    └── templates.xml         # QWeb templates
```

---

## 🛠 Installation

1. Clone or copy the module to your Odoo addons directory:
   ```bash
   git clone https://github.com/manziosee/legal_compliance.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install the module via:
   - Odoo Apps interface, or
   ```bash
   odoo-bin -i legal_compliance
   ```

---

## ⚙️ Configuration

1. Navigate to **Settings → Compliance → Configuration**.
2. Set default parameters:
   - Alert days before due date.
   - Compliance manager.
3. Create compliance categories (e.g., Tax, HR, Safety).

---

## 📚 Usage

### 1️⃣ Setting Up Compliance Rules
- Navigate to **Compliance → Rules**.
- Create new rules with fields like:
  - Category.
  - Department.
  - Priority level.
  - Recurrence schedule.

### 2️⃣ Performing Compliance Checks
- Scheduled checks appear in the dashboard.
- Manual checks can be initiated from rules.
- Record results (Compliant/Non-Compliant).
- Upload supporting documents.

### 3️⃣ Document Management
- Attach PDFs, images, or other files.
- Set expiry dates for documents.
- Track document validity.

---

## 🧑‍💻 Technical Implementation

### Core Models

1. **Compliance Category** (`compliance.category`)
   - Classification of rules (Tax, HR, Safety).
   - Color coding and sequencing.

2. **Compliance Rule** (`compliance.rule`)
   - Core requirements with scheduling.
   - State management (Draft/Active/Archived).
   - Automatic next check date calculation.

3. **Compliance Check** (`compliance.check`)
   - Records of individual verifications.
   - Result tracking with notes.
   - Document attachments.

4. **Compliance Document** (`compliance.document`)
   - Evidence storage.
   - Expiry date tracking.
   - Integrated with Odoo attachments.

---

## 🔑 Key Features Implementation

- **Recurring Checks**: Cron job checks for due dates daily.
- **Alerts**: Email templates with dynamic content.
- **Dashboard**: Custom JS widget with RPC calls.
- **Document Handling**: Integrated with Odoo's attachment system.

---

## 📋 Dependencies

- **Odoo Community Edition** 15.0+
- **Python** 3.6+
- Required Odoo modules:
  - `base`
  - `mail`
  - `calendar`

---

## 🛠 Development
### Contributing
1. **Fork** the repository.
2. Create your feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add my feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/my-feature
   ```
5. Submit a **pull request**.

---

## 📞 Support

For issues or feature requests, contact:
- **Author**: Manzi Osee
- **Company**: SIC Rwanda
- **Website**: [https://www.sicrwanda.com](https://www.sicrwanda.com)

---

## ⚖️ License

This module is licensed under the **LGPL-3** license.

---

Thank you for using the **Legal Compliance Management Module**! 🚀