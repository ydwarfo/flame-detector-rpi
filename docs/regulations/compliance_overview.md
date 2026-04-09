# Regulatory Compliance Guide — Connected Talking Candle (Belgium / EU)

> **Scope:** Belgian and EU market. Product combines a physical scented candle,
> an IoT electronic base, cloud services, and an AI voice system.
> **Last reviewed:** 2026-04-09

---

## Product Feature Map

| Feature | Applicable frameworks |
|---|---|
| Scented candle (wax, fragrance) | EN 15426, EN 15493/15494, CLP (EC 1272/2008), REACH |
| Electronic base (RPi / ESP32, sensors) | CE (RED + LVD + EMC), RoHS, WEEE |
| Wi-Fi / Bluetooth radio | RED 2014/53/EU, FCC Part 15 (if US) |
| Speaker + microphone | RED, GDPR (audio data), recording consent |
| Voice message cloud storage | GDPR, ePrivacy, data processor agreements |
| AI conversational personality | EU AI Act 2024/1689/EU |
| QR code web portal | GDPR, ePrivacy/cookie law, EAA/WCAG |
| Eco-refill claims | Green Claims Directive, CLP |
| Consumer gift product | GPSR 2023/988, Consumer Rights Dir. 2011/83/EU |

---

## 1. Physical Product — Candle Components

### 1.1 EN 15426:2018 — Candle Safety

**Requirement:** Flame stability, self-extinction, stable combustion.

**Compliance actions:**
- Test candle wax formulation for stable burn characteristics.
- Verify self-extinguishing properties under normal and fault conditions.
- Document flame stability under normal use conditions.
- Obtain certification from an accredited testing laboratory.

### 1.2 EN 15493 / EN 15494 — Candle Safety & Labelling

**Requirement:** Mandatory safety labelling — standardised pictograms and usage instructions.

**Compliance actions:**
- Design labels with all required safety pictograms.
- Include usage instructions in **French and Dutch** for the Belgian market.
- Implement standardised warning symbols (never leave unattended, keep away from children/flammables, burn on heat-resistant surface, trim wick).
- Ensure label durability and legibility throughout product shelf life.

> The electronic base doubles as the candle holder and must independently comply with EN 15493 as a candle accessory.

### 1.3 CLP Regulation — EC No 1272/2008

**Scope:** Classification, Labelling and Packaging of scented candles containing potentially allergenic substances.

**Compliance actions:**
- Classify all fragrance components for allergen content (IFRA / ECHA guidelines).
- Create appropriate hazard labels if allergen thresholds are exceeded.
- Implement packaging warnings for sensitising substances.
- Maintain ingredient documentation (full fragrance composition).

### 1.4 Safety Data Sheets (SDS)

**Scope:** Required for each fragrance or essential oil used.

**Compliance actions:**
- Obtain SDS from all fragrance suppliers.
- Maintain an updated SDS database.
- Ensure SDS are available to customers and distributors upon request.
- Include SDS references in product technical documentation.

---

## 2. Electronic Components — IoT Device

### 2.1 CE Marking

#### Radio Equipment Directive (RED) — 2014/53/EU

**Scope:** All devices with radio modules (Wi-Fi, Bluetooth — ESP32 or RPi).

**Compliance actions:**
- Obtain CE marking for the radio module (ESP32 carries its own CE; verify it covers your use case).
- Conduct radio frequency testing if module certification does not cover the final product configuration.
- Prepare a Declaration of Conformity (DoC).
- Maintain a technical documentation file (retained 10 years).

#### RoHS Directive — 2011/65/EU (amended by 2015/863/EU)

**Scope:** Restriction of hazardous substances in electronic components.

**Compliance actions:**
- Verify all electronic components are RoHS-compliant (obtain supplier declarations).
- Document material composition of PCB, solder, connectors.
- Implement supply chain verification process.

#### WEEE Directive — 2012/19/EU

**Scope:** Electronic waste management.

**Compliance actions:**
- Include the crossed-out wheelie bin symbol on product and packaging.
- Register with the Belgian WEEE scheme (Recupel).
- Provide take-back information to customers.
- Implement end-of-life recycling programme.

### 2.2 Low Voltage Directive (LVD) — 2014/35/EU

**Scope:** Components powered by mains electricity (power adapters, DC modules).

**Compliance actions:**
- Ensure power adapters meet LVD safety standards (IEC 62368-1 or IEC 60950-1).
- Conduct electrical safety testing (insulation, creepage, clearance distances).
- Verify insulation and protection measures around the open-flame proximity zone.
- Obtain certification for all mains-connected power components.

### 2.3 EMC Directive — 2014/30/EU

**Scope:** Devices that may generate or be susceptible to electromagnetic interference.

**Compliance actions:**
- Conduct EMC emissions testing (EN 55032).
- Conduct EMC immunity testing (EN 55035).
- Verify electromagnetic immunity in the presence of typical household RF sources.
- Obtain EMC compliance certification from an accredited lab.

---

## 3. Data Protection & Privacy

### 3.1 GDPR — Regulation EU 2016/679

**Scope:** Collection and processing of voice messages and personal data (gift-giver identity, recipient identity, burn session data, account data).

> Voice messages may qualify as **biometric data** under Art. 4(14) if processed to identify a natural person. This requires **explicit consent** (Art. 9) and stricter safeguards.

#### Lawful basis & consent

- Obtain explicit, freely given, specific consent before recording or storing voice messages.
- Consent must be unbundled from product activation — users can use the product without voice messaging.
- Maintain timestamped consent records.

#### Transparency

- Publish a clear Privacy Policy covering: what data is collected, why, for how long, who has access, and user rights.
- Surface privacy information at account creation and via the QR portal.
- Clearly state whether voice data is processed by an AI system.

#### Data minimisation & storage limitation

- Collect only data strictly necessary for the service.
- Define and enforce message retention periods (e.g., auto-delete after 12 months or on account closure).
- Allow users to set their own retention preferences.

#### User rights (must be implemented)

| Right | Implementation |
|---|---|
| Access (Art. 15) | User can view/download all their data |
| Rectification (Art. 16) | User can edit account data |
| Erasure (Art. 17) | User can delete messages and close account |
| Portability (Art. 20) | User can export messages in standard format |
| Objection (Art. 21) | User can opt out of non-essential processing |

#### Security measures

- Encrypt voice data **in transit** (TLS 1.2+) and **at rest** (AES-256 or equivalent).
- Implement secure authentication (strong passwords, MFA option).
- Conduct regular security audits and penetration tests.
- Establish and document incident response procedures.
- Data breach notification to Belgian DPA (APD/GBA) within **72 hours** of discovery (Art. 33).

#### Third parties & international transfers

- Sign Data Processing Agreements (DPA) with all cloud providers.
- Prefer EU-based servers; if outside EU, use Standard Contractual Clauses (SCCs).
- Maintain a Record of Processing Activities (RoPA).
- Assess whether a Data Protection Officer (DPO) is required.

### 3.2 ePrivacy Directive — Cookie & Tracking Compliance

**Requirements for the QR web portal:**
- Obtain cookie consent before setting any non-essential cookies.
- Provide clear information about tracking technologies used.
- Implement functional opt-out mechanisms.
- Cookie banner must meet Belgian DPA guidance (no pre-ticked boxes, equal prominence of accept/reject).

---

## 4. AI Act Compliance — Regulation EU 2024/1689

### 4.1 Risk Classification

The conversational AI personality feature is classified as a **Limited Risk AI system** (AI interacting directly with humans — Art. 52).

### 4.2 Transparency obligations (Art. 52)

Users must be informed they are interacting with an AI system. This is **mandatory** and cannot be waived.

**Implementation:**
- Display "You are interacting with an AI system" at first interaction and in product documentation.
- Explain AI capabilities and limitations in plain language.
- Inform users about what data is processed to generate AI responses.

### 4.3 User control mechanisms

- Provide an **ON/OFF control** for AI voice functionality (hardware or app).
- Provide volume and interaction controls.
- Implement opt-out mechanisms for AI features without disabling the core product.

### 4.4 Technical documentation

- Describe the AI system and its capabilities.
- Document training data sources and model information.
- Conduct and document a risk assessment and mitigation measures.
- Monitor for bias in AI-generated content.

---

## 5. Commercial & Labelling Requirements

### 5.1 Mandatory product information (GPSR 2023/988)

- **Company details:** Name and postal address of the EU-responsible economic operator.
- **Traceability:** Batch codes and manufacturing dates on product or packaging.
- **Language:** All mandatory information in **French and Dutch** for Belgium.
- **Instructions:** Clear usage and safety instructions in both languages.
- **Unique product identifier:** Required for GPSR traceability.

### 5.2 Consumer rights — Directive 2011/83/EU

- **2-year legal guarantee** on the electronic base (mandatory in EU).
- **14-day right of withdrawal** for distance sales (online/QR purchase flow).
- For digital content (personality packs, message storage): right of withdrawal applies until digital service delivery begins, with explicit consumer consent and acknowledgement.
- Inform consumers of the **minimum software support period** for the device.

### 5.3 Belgian business registration & e-commerce

| Requirement | Detail |
|---|---|
| BCE registration | Register with the Banque-Carrefour des Entreprises |
| VAT number | Obtain intra-community VAT number (BE 0XXX.XXX.XXX) |
| Legal mentions | Website must display company name, address, VAT, email, BCE number |
| Terms & conditions | Clear T&C covering purchase, subscription, data use |

---

## 6. Estimated Compliance Costs

| Category | Estimated cost | Timeline |
|---|---|---|
| Candle safety testing (EN standards) | €3,000 – €5,000 | 4–6 weeks |
| Electronic device certification (CE) | €8,000 – €12,000 | 6–8 weeks |
| Legal consultation (GDPR, AI Act) | €5,000 – €8,000 | 2–4 weeks |
| GDPR technical implementation | €3,000 – €5,000 | 4–6 weeks |
| Belgian business registration | €500 – €1,000 | 2–3 weeks |
| **Total estimated** | **€19,500 – €31,000** | **8–12 weeks** |

---

## 7. Ongoing Compliance Obligations

### Regular requirements
- Annual compliance reviews across all frameworks.
- Keep Safety Data Sheets current when fragrance suppliers change formulations.
- Monitor GDPR compliance continuously; conduct annual internal audits.
- Handle customer complaints and safety incidents per GPSR procedures.
- Report serious incidents to Belgian authorities via the EU Safety Gate.

### Documentation maintenance
- Keep all CE certificates and test reports current (re-test on hardware changes).
- Maintain and update the technical documentation file.
- Review and update the Privacy Policy annually or when processing changes.
- Monitor EU regulatory updates (AI Act implementing acts, CRA, Green Claims).

---

## 8. Risk Matrix

| Risk area | Level | Financial exposure | Blocks market entry? |
|---|---|---|---|
| GDPR violation | High | Up to 4% global turnover | No, but operational risk |
| Missing CE marking | High | Market withdrawal, fines | **Yes** |
| EN 15426/15493 candle safety | High | Product liability, recalls | **Yes** |
| GPSR non-compliance | High | Market withdrawal | **Yes (Dec 2024)** |
| AI Act transparency | Medium | Fines + reputational damage | No (from 2026) |
| Audio recording consent | Medium | Legal liability | No |
| WEEE non-registration | Medium | Administrative fines | No |
| Missing Belgian BCE/VAT | Medium | Cannot trade legally | **Yes** |
| Green Claims unsubstantiated | Low | Greenwashing enforcement | Blocks eco-marketing |
