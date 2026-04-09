# Compliance To-Do — Connected Talking Candle

Actionable checklist organised by phase. See `compliance_overview.md` for the full
regulatory rationale behind each item.

> **Legend:** 🔴 Blocks market entry · 🟠 Legal obligation · 🟡 Risk mitigation · 🟢 Best practice

---

## Phase 1 — Documentation & Planning (Months 1–2)

### Supplier & component documentation
- [ ] 🔴 Collect RoHS declarations of conformity from all electronic component suppliers (PCB, ESP32/RPi module, connectors, solder)
- [ ] 🔴 Obtain CE certificate and Declaration of Conformity for the radio module (ESP32 or equivalent)
- [ ] 🔴 Obtain Safety Data Sheets (SDS) from all fragrance and essential oil suppliers
- [ ] 🔴 Obtain full fragrance composition from suppliers (allergen disclosure for CLP)
- [ ] 🟠 Confirm candle wax and dye formulations are REACH-compliant (no SVHC > 0.1% w/w)
- [ ] 🟠 Verify power adapter / PSU carries CE + LVD certification

### Legal & business setup
- [ ] 🔴 Register company with the **BCE** (Banque-Carrefour des Entreprises), Belgium
- [ ] 🔴 Obtain intra-community **VAT number** (BE 0XXX.XXX.XXX)
- [ ] 🔴 Designate an **EU-responsible economic operator** (name + address for all product labelling)
- [ ] 🟠 Assess whether a **Data Protection Officer (DPO)** is required; appoint if yes
- [ ] 🟠 Engage a legal advisor specialised in GDPR and product safety

### Technical documentation drafts
- [ ] 🔴 Start **CE Technical File**: product description, risk assessment, applied standards, test reports (placeholder), DoC draft
- [ ] 🟠 Draft **Record of Processing Activities (RoPA)** covering: voice messages, account data, burn session telemetry
- [ ] 🟠 Identify and shortlist **accredited test laboratories** for EN candle standards and CE (EMC + RED)
- [ ] 🟡 Draft **AI system description** for AI Act technical documentation (model, training data, risk assessment)

---

## Phase 2 — Testing & Certification (Months 3–4)

### Candle physical safety
- [ ] 🔴 Submit candle wax formulation for **EN 15426:2018** testing (flame stability, self-extinction, combustion)
- [ ] 🔴 Test the complete candle + base assembly for holder stability (EN 15493)
- [ ] 🔴 Validate minimum safe distance between candle flame and electronics; document thermal performance
- [ ] 🟠 Verify enclosure plastic meets **UL 94 V-0 or V-1** flame-retardant rating
- [ ] 🟠 Classify all fragrance components under **CLP Regulation** (EC 1272/2008); apply hazard labels if required

### Electronic device certification
- [ ] 🔴 Submit device for **EMC testing** — emissions (EN 55032) and immunity (EN 55035)
- [ ] 🔴 Submit device for **RED radio testing** (EN 300 328 for Wi-Fi 2.4 GHz, EN 301 489 for antenna)
- [ ] 🔴 Submit power adapter for **LVD electrical safety testing** (IEC 62368-1)
- [ ] 🟠 Verify all components pass **RoHS** substance limits (lab analysis if supplier documentation is insufficient)
- [ ] 🟡 Conduct **ETSI EN 303 645** IoT security self-assessment (no universal default passwords, TLS, secure update mechanism)

### GDPR technical implementation
- [ ] 🔴 Implement **TLS 1.2+** for all device-to-cloud and portal communications
- [ ] 🔴 Implement **encryption at rest** for stored voice messages (AES-256 or equivalent)
- [ ] 🔴 Build user **account deletion** flow (messages + account data fully purged)
- [ ] 🔴 Build **data export** (portability) feature for voice messages
- [ ] 🟠 Implement **cookie consent** mechanism on the QR web portal (no pre-ticked boxes)
- [ ] 🟠 Implement **message retention policy** — auto-delete or user-configurable expiry
- [ ] 🟠 Implement **explicit consent** capture for voice message recording at portal onboarding
- [ ] 🟠 Set up **data breach response** procedure and internal notification chain

---

## Phase 3 — Legal & Administrative (Months 5–6)

### Declarations & registrations
- [ ] 🔴 Sign and date the **Declaration of Conformity (DoC)** — CE marking, covering RED + LVD + EMC + RoHS
- [ ] 🔴 Register with **Recupel** (Belgian WEEE take-back scheme)
- [ ] 🟠 Register with Belgian battery take-back scheme if device contains a rechargeable battery (Bebat)
- [ ] 🟠 Sign **Data Processing Agreements (DPA)** with all cloud infrastructure providers (AWS, GCP, etc.)
- [ ] 🟠 If cloud servers are outside EU — implement **Standard Contractual Clauses (SCCs)** for data transfers

### Privacy & legal documents (website + app)
- [ ] 🔴 Publish **Privacy Policy** covering: data collected, legal basis, retention, user rights, DPA contact
- [ ] 🔴 Publish **Terms & Conditions** covering: purchase, digital content, 2-year legal guarantee, 14-day withdrawal right
- [ ] 🔴 Publish **Legal Mentions** page (company name, address, BCE, VAT, email, DPA contact)
- [ ] 🟠 Add **AI disclosure** statement: "This product uses an AI system to generate voice responses"
- [ ] 🟠 Add **microphone active indicator** in app/portal whenever mic is recording
- [ ] 🟡 Publish an **Accessibility Statement** (WCAG 2.1 AA) for the QR web portal

### Labelling & packaging finalisation
- [ ] 🔴 Finalise product labels in **French and Dutch** with all required content:
  - Company name + address (EU responsible entity)
  - CE mark
  - WEEE symbol (crossed-out wheelie bin)
  - EN 15493/15494 safety pictograms
  - Batch code and manufacturing date
  - CLP hazard labels (if fragrance triggers thresholds)
- [ ] 🔴 Include **printed instructions** (French + Dutch) covering: candle use, electronic base, voice features, data privacy summary, disposal
- [ ] 🟠 Ensure packaging materials are labelled with recyclable material type

---

## Phase 4 — Market Preparation (Months 6–7)

### Final compliance verification
- [ ] 🔴 Receive and archive all **test reports** from accredited labs
- [ ] 🔴 Complete and file the **CE Technical File** (retain for 10 years)
- [ ] 🔴 Conduct a final **GDPR compliance audit** before launch
- [ ] 🟠 Complete **AI Act technical documentation** (system description, risk assessment, bias monitoring plan)
- [ ] 🟡 Conduct a **penetration test** on the cloud backend and QR portal

### Customer service & operations
- [ ] 🟠 Train customer service team on: GDPR user rights requests, product safety complaint handling, WEEE/battery take-back questions
- [ ] 🟠 Set up **GPSR incident reporting** procedure (serious incidents reported to Belgian authorities via EU Safety Gate within 3 days)
- [ ] 🟡 Set up **vulnerability disclosure policy** and contact channel (security@yourdomain.com)

### Marketing & claims
- [ ] 🟠 Review all "eco-friendly" and sustainability claims for substantiation (Green Claims Directive readiness)
- [ ] 🟡 Ensure AI voice licence (ElevenLabs or equivalent) explicitly permits use in a commercial consumer product
- [ ] 🟡 Audit all open-source software licences in firmware and backend (GPL/LGPL compatibility)

---

## Ongoing — Post-Launch

### Periodic reviews
- [ ] 🟠 Annual compliance review (all frameworks)
- [ ] 🟠 Annual Privacy Policy review / update
- [ ] 🟠 Review fragrance SDS and CLP classification when supplier changes formulation
- [ ] 🟡 Monitor EU regulatory pipeline: AI Act implementing acts, Cyber Resilience Act (2027), updated Battery Regulation requirements
- [ ] 🟡 Re-assess WEEE and battery take-back registrations when entering new EU markets

### Incident & complaint handling
- [ ] 🟠 Log all product safety complaints
- [ ] 🟠 Report serious incidents to Belgian market surveillance authority and EU Safety Gate
- [ ] 🟠 Notify Belgian DPA (APD/GBA) of personal data breaches within **72 hours**

---

## Quick Reference — Costs & Timeline

| Phase | Key deliverable | Est. cost | Duration |
|---|---|---|---|
| 1 — Documentation | Supplier docs, legal setup, RoPA | €5,500 – €9,000 | Months 1–2 |
| 2 — Testing | EN candle tests, CE (EMC+RED+LVD), GDPR dev | €14,000 – €22,000 | Months 3–4 |
| 3 — Legal & Admin | DoC, WEEE, privacy docs, labels | included above | Months 5–6 |
| 4 — Market prep | Final audit, pen test, training | included above | Months 6–7 |
| **Total** | | **€19,500 – €31,000** | **8–12 weeks** |
