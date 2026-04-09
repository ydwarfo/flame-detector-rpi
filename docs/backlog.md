# Product Backlog — Connected Talking Candle

Items derived from:
- Regulatory requirements → `regulations/compliance_overview.md`
- User journey (device provisioning, configuration, notifications)
- Personality & personalization user stories

Each item is traceable to its source.

> **Priority:** 🔴 Must-have (blocks launch) · 🟠 Should-have (legal obligation) · 🟡 Nice-to-have (risk mitigation)
> **Layer:** `device` = RPi firmware · `api` = cloud backend · `portal` = web app (gift-giver / recipient)

---

## Epic 1 — Account & Identity

| # | User story | Priority | Layer | Compliance source |
|---|---|---|---|---|
| 1.1 | As a gift-giver, I can create an account with email + password so that I can send voice messages to a candle. | 🔴 | api, portal | GDPR Art. 6 |
| 1.2 | As a recipient, I can create an account linked to my candle's QR code so that I can manage my messages and preferences. | 🔴 | api, portal | GDPR Art. 6 |
| 1.3 | As a user, I can edit my profile information (name, email) at any time so that my data stays accurate. | 🔴 | api, portal | GDPR Art. 16 (rectification) |
| 1.4 | As a user, I can permanently close my account and have all my data deleted so that I can exercise my right to erasure. | 🔴 | api, portal | GDPR Art. 17 |
| 1.5 | As a user, I can log in with a strong password and optionally enable two-factor authentication so that my account is secure. | 🟠 | api, portal | GDPR Art. 32 (security) |

---

## Epic 2 — Consent Management

| # | User story | Priority | Layer | Compliance source |
|---|---|---|---|---|
| 2.1 | As a gift-giver, I am shown a clear, standalone consent request before recording or uploading any voice message, so that consent is freely given and specific. | 🔴 | portal | GDPR Art. 7 + Art. 9 (biometric/voice data) |
| 2.2 | As a new user, I can activate the product (candle flame detection, burn tracking) without consenting to voice messaging, so that voice consent is unbundled from product activation. | 🔴 | portal, api | GDPR Art. 7 (unbundled consent) |
| 2.3 | As a user, I can withdraw my consent for voice message processing at any time, and my existing messages are deleted upon withdrawal. | 🔴 | portal, api | GDPR Art. 7(3) |
| 2.4 | As a system, each consent event is recorded with a timestamp and the consent text version shown, so that the company can demonstrate compliance. | 🔴 | api | GDPR Art. 7(1) |
| 2.5 | As a first-time visitor to the web portal, I see a cookie consent banner before any non-essential cookies are set, with equal-prominence accept and reject buttons. | 🔴 | portal | ePrivacy Directive, Belgian DPA guidance |
| 2.6 | As a user, I can manage my cookie preferences at any time via a clearly accessible link in the footer. | 🟠 | portal | ePrivacy Directive |

---

## Epic 3 — GDPR User Rights

| # | User story | Priority | Layer | Compliance source |
|---|---|---|---|---|
| 3.1 | As a user, I can download a complete export of all my data (account info, voice messages, burn history) in a standard format (JSON or ZIP). | 🔴 | api, portal | GDPR Art. 20 (portability) |
| 3.2 | As a user, I can view a list of all voice messages associated with my account, including who sent them and when. | 🔴 | portal | GDPR Art. 15 (access) |
| 3.3 | As a user, I can delete any individual voice message I own at any time. | 🔴 | portal, api | GDPR Art. 17 (erasure) |
| 3.4 | As a user, I can opt out of non-essential data processing (analytics, personalisation) without affecting core product functionality. | 🟠 | portal, api | GDPR Art. 21 (objection) |
| 3.5 | As a user, I can submit a data subject request (access, erasure, portability) through a dedicated form, and receive a response within 30 days. | 🟠 | portal | GDPR Art. 12 |

---

## Epic 4 — Privacy & Data Security

| # | User story | Priority | Layer | Compliance source |
|---|---|---|---|---|
| 4.1 | As the system, all communication between the device and the cloud is encrypted with TLS 1.2+ so that voice data cannot be intercepted in transit. | 🔴 | device, api | GDPR Art. 32, ETSI EN 303 645 |
| 4.2 | As the system, voice messages stored in the cloud are encrypted at rest (AES-256 or equivalent) so that a database breach does not expose content. | 🔴 | api | GDPR Art. 32 |
| 4.3 | As the system, device API credentials are unique per device and never shared or hardcoded as universal defaults. | 🔴 | device, api | ETSI EN 303 645 provision 1 |
| 4.4 | As the system, the device checks for firmware/software updates at startup and on a regular schedule, and applies them securely (verified signature). | 🟠 | device, api | RED Art. 10(8), ETSI EN 303 645, EU Cyber Resilience Act |
| 4.5 | As an admin, I am alerted when a data breach is detected so that I can notify the Belgian DPA (APD/GBA) within 72 hours. | 🔴 | api | GDPR Art. 33 |
| 4.6 | As the system, all data processing activities are logged in a Record of Processing Activities (RoPA) maintained in the admin backend. | 🟠 | api | GDPR Art. 30 |
| 4.7 | As a security researcher, I can report a vulnerability via a published contact channel (security@…) so that issues are handled responsibly. | 🟡 | portal | ETSI EN 303 645 provision 2 |

---

## Epic 5 — Data Retention

| # | User story | Priority | Layer | Compliance source |
|---|---|---|---|---|
| 5.1 | As a recipient, I can set a retention period for received voice messages (e.g., keep for 6 months, 1 year, or until I delete them). | 🔴 | portal, api | GDPR Art. 5(1)(e) (storage limitation) |
| 5.2 | As the system, voice messages that have exceeded their retention period are automatically and permanently deleted. | 🔴 | api | GDPR Art. 5(1)(e) |
| 5.3 | As a user, I receive a notification before my messages are auto-deleted so that I can take action if I want to keep them. | 🟠 | portal, api | GDPR Art. 5(1)(e), transparency |
| 5.4 | As the system, all personal data is deleted within 30 days of account closure. | 🔴 | api | GDPR Art. 17 |

---

## Epic 6 — AI Voice & Disclosure

| # | User story | Priority | Layer | Compliance source |
|---|---|---|---|---|
| 6.1 | As a new user activating the candle, I see a clear disclosure that the candle uses an AI system to generate voice responses, before the AI feature is used for the first time. | 🔴 | portal, device | EU AI Act Art. 52 (transparency) |
| 6.2 | As a user, I can read a plain-language explanation of what the AI does, what data it uses, and its limitations, accessible from the portal. | 🔴 | portal | EU AI Act Art. 52 |
| 6.3 | As a recipient, I can turn the AI voice feature ON or OFF from the portal or a physical control on the base, without disabling flame detection or message playback. | 🔴 | portal, device, api | EU AI Act Art. 52 (user control) |
| 6.4 | As a recipient, I can adjust the volume of the AI voice and message playback from the portal. | 🟠 | portal, device, api | EU AI Act Art. 52 (user control) |
| 6.5 | As a recipient, I can select or change the AI personality pack (e.g., warm, playful, romantic) from the portal. | 🟡 | portal, api, device | Product feature |
| 6.6 | As the system, AI-generated responses are monitored for content that may be biased, offensive, or harmful, and flagged for review. | 🟡 | api | EU AI Act Art. 9 (risk management) |

---

## Epic 7 — Voice Messaging Portal

| # | User story | Priority | Layer | Compliance source |
|---|---|---|---|---|
| 7.1 | As a gift-giver, I can record or upload a voice message of up to [X] seconds via the web portal and associate it with a recipient's candle. | 🔴 | portal, api | Core feature |
| 7.2 | As a gift-giver, I can preview my recorded message before sending it. | 🟠 | portal | Core feature / UX |
| 7.3 | As a gift-giver, I can delete a message I have sent, provided it has not yet been played by the candle. | 🟠 | portal, api | GDPR Art. 17 |
| 7.4 | As a recipient, I can view the list of messages queued for my candle, including sender and date. | 🟠 | portal | GDPR Art. 15 |
| 7.5 | As the device, when the candle is lit and a new message is available, I download and play it through the speaker. | 🔴 | device, api | Core feature |
| 7.6 | As the device, I indicate (LED or audio cue) when the microphone is actively recording so that users are always aware of recording activity. | 🔴 | device | GDPR recording consent, Belgian DPA guidance |

---

## Epic 8 — Burn Life Tracking

| # | User story | Priority | Layer | Compliance source |
|---|---|---|---|---|
| 8.1 | As the device, I log every burn session (start time, duration) and send it to the cloud so that total burn life can be tracked. | 🟠 | device, api | Product feature / GDPR data minimisation |
| 8.2 | As a recipient, I can view my candle's remaining estimated burn life in the portal. | 🟠 | portal, api | Product feature (eco-refill) |
| 8.3 | As a recipient, I receive a notification (portal, email, or voice from the candle) when the estimated burn life falls below a threshold, prompting a refill. | 🟠 | portal, api, device | Eco-refill feature, Green Claims substantiation |
| 8.4 | As the system, burn session data is stored only in aggregate after the retention period; raw session logs are deleted after 12 months. | 🟠 | api | GDPR Art. 5(1)(e) (data minimisation) |

---

## Epic 9 — Product QR & Information Pages

| # | User story | Priority | Layer | Compliance source |
|---|---|---|---|---|
| 9.1 | As a customer scanning the Product QR, I am taken to a page showing fragrance details, ingredient list, origin, eco tips, and a link to the Safety Data Sheet, in French and Dutch. | 🔴 | portal | EN 15493/15494, CLP, SDS obligations |
| 9.2 | As a customer, I can download the Safety Data Sheet (SDS) for the candle's fragrance directly from the product information page. | 🟠 | portal | SDS availability requirement |
| 9.3 | As a customer scanning the Message QR, I am taken to the gift-giver portal where I can send a voice message to the candle's owner. | 🔴 | portal | Core feature |
| 9.4 | As the system, each candle has a unique identifier that links its QR codes to its cloud account, enabling per-device traceability. | 🔴 | api | GPSR 2023/988 (traceability) |

---

## Epic 10 — Legal & Transparency Pages

| # | User story | Priority | Layer | Compliance source |
|---|---|---|---|---|
| 10.1 | As a visitor, I can read the Privacy Policy from any page via a footer link, in French and Dutch. | 🔴 | portal | GDPR Art. 13/14 |
| 10.2 | As a visitor, I can read the Terms & Conditions, covering purchase, subscription, 2-year guarantee, and 14-day right of withdrawal. | 🔴 | portal | Consumer Rights Directive 2011/83/EU |
| 10.3 | As a visitor, I can see the Legal Mentions page displaying company name, address, BCE number, VAT number, and contact email. | 🔴 | portal | Belgian e-commerce law |
| 10.4 | As a customer purchasing online, I am presented with the 14-day right of withdrawal notice and can initiate a return from my account. | 🔴 | portal, api | Consumer Rights Directive Art. 9 |
| 10.5 | As a customer purchasing a digital personality pack, I explicitly acknowledge that downloading/activating it waives my right of withdrawal before the download begins. | 🔴 | portal | Consumer Rights Directive Art. 16(m) |
| 10.6 | As a visitor, I can read the Accessibility Statement for the web portal, confirming WCAG 2.1 AA compliance. | 🟠 | portal | European Accessibility Act (EAA) |
| 10.7 | As a user, I can access the portal in French or Dutch, with all mandatory legal content available in both languages. | 🔴 | portal | Belgian market requirement |

---

## Epic 11 — Device Pairing & Management

| # | User story | Priority | Layer | Compliance source |
|---|---|---|---|---|
| 11.1 | As a new owner, I can pair my candle base to my account by scanning the Message QR code, without requiring technical knowledge. | 🔴 | portal, device, api | Core feature / GPSR traceability |
| 11.2 | As the device, I report my current firmware version to the cloud at each connection so that outdated devices can be identified and updated. | 🟠 | device, api | RED Art. 10(8), CRA readiness |
| 11.3 | As the device, I download and apply firmware updates automatically when a verified update is available, without requiring user action. | 🟠 | device, api | ETSI EN 303 645, CRA readiness |
| 11.4 | As a recipient, I can see the firmware version of my device and the last update date in the portal. | 🟡 | portal, api | Transparency / CRA readiness |
| 11.5 | As a recipient, I can unpair my candle from my account, which removes all messages from the device. | 🟠 | portal, device, api | GDPR Art. 17 |

---

## Epic 12 — Internal Compliance & Admin

| # | User story | Priority | Layer | Compliance source |
|---|---|---|---|---|
| 12.1 | As an admin, I can view an audit log of all data subject requests (access, deletion, export) and their resolution status. | 🟠 | api | GDPR Art. 12 (response within 30 days) |
| 12.2 | As an admin, I receive an automated alert when a potential data breach is detected (unusual access patterns, failed auth spikes) so that the 72-hour DPA notification window can be met. | 🔴 | api | GDPR Art. 33 |
| 12.3 | As an admin, I can generate a report of all active data processing activities (RoPA) for DPA submission. | 🟠 | api | GDPR Art. 30 |
| 12.4 | As an admin, I can trigger an incident report and track its status through to DPA notification and resolution. | 🟠 | api | GDPR Art. 33, GPSR incident reporting |
| 12.5 | As an admin, I can view per-device burn session statistics to support eco-refill program reporting and green claims substantiation. | 🟡 | api | Green Claims Directive |

---

## Epic 13 — Device Provisioning & Configuration

Items derived from the user journey: unique QR identification, cloud-based product
profile retrieval, sensor auto-configuration, remote parameter management, real-time
dashboard, sensor data sync, and QR-based configuration delivery.

| # | User story | Priority | Layer | Source |
|---|---|---|---|---|
| 13.1 | As a new owner, I scan my candle's QR code and the system uniquely identifies my device, retrieves its product profile (candle type, scent, burn time, default personality), and completes provisioning automatically. | 🔴 | portal, api, device | User journey #1, #2 |
| 13.2 | As the device, once paired, I automatically fetch my configuration from the cloud (sensor thresholds, check intervals, personality, voice files) so that I am ready to operate without manual setup. | 🔴 | device, api | User journey #4 |
| 13.3 | As the system, when a candle product profile is loaded, the relevant sensors and their parameters (flame detection, burn timer, temperature if present) are automatically activated and calibrated for that product type. | 🔴 | device, api | User journey #3 |
| 13.4 | As a recipient, I can view a live dashboard showing my candle's current state (flame on/off, burn session duration, estimated remaining life, last message played, firmware version). | 🔴 | portal, api | User journey #5 |
| 13.5 | As the device, I synchronise sensor readings and session events to the cloud automatically at regular intervals and on every state change, so that the dashboard always reflects the current state. | 🔴 | device, api | User journey #6 |
| 13.6 | As a recipient, I can modify sensor parameters (flame detection sensitivity, debounce time, burn life threshold for refill alert) directly from the portal, and the device applies the new configuration within one polling cycle. | 🟠 | portal, api, device | User journey #7 |
| 13.7 | As an installer or retailer, I can encode a configuration payload into a QR code and the device reads it on scan to apply initial settings (Wi-Fi credentials, product ID, personality pack) without needing a smartphone app. | 🟡 | device, api | User journey #8 |
| 13.8 | As a recipient, I receive a real-time notification (push, email, or SMS) for key candle events: flame detected, flame extinguished, message received, refill needed, firmware updated. | 🟠 | api, portal | User journey #9 |
| 13.9 | As the device, I personalise the voice message spoken at each event using contextual data from the cloud (time of day, recipient name, burn session count, personality) so that each interaction feels unique. | 🟠 | device, api | User journey #10 |

---

## Epic 14 — Personality & Personalization

Items derived from the personality user journey: personality assignment, custom
message configuration, AI-generated message content, event-triggered voice, lighting
tied to personality, adaptive preferences, physical interaction triggers, and
full identity setup at purchase.

| # | User story | Priority | Layer | Source |
|---|---|---|---|---|
| 14.1 | As a gift-giver or recipient, I can assign a personality to my candle (e.g., Warm & Comforting, Playful, Romantic, Mindful) from the portal so that all AI-generated speech reflects that character. | 🔴 | portal, api | Personality #1, #10 |
| 14.2 | As a gift-giver, I can write custom message templates (greetings, affirmations, bedtime wishes) that the candle delivers in the chosen personality's voice at the right moment. | 🔴 | portal, api | Personality #2 |
| 14.3 | As the system, when an event is triggered (candle lit, candle out, message received, burn milestone reached), I generate a contextual phrase in the style of the assigned personality using the AI voice engine. | 🔴 | api, device | Personality #3 |
| 14.4 | As a recipient, my candle greets me, responds to my actions, and speaks in its own personality — making each interaction feel like a conversation with a character, not a device. | 🔴 | device, api | Personality #4 |
| 14.5 | As a gift-giver, I can schedule or trigger a personalised voice message to be delivered the next time the candle is lit (e.g., a birthday wish played the morning of a birthday). | 🔴 | portal, api, device | Personality #5 |
| 14.6 | As a recipient, the LED ring (if present) on the base glows in a colour associated with the active personality (e.g., warm amber for Comforting, soft blue for Mindful) and changes with mood or event. | 🟠 | device, api | Personality #6 |
| 14.7 | As a recipient, I can view my candle's personality profile, message history, and usage story (first light, total hours burned, messages received) on my portal dashboard. | 🟠 | portal, api | Personality #7 |
| 14.8 | As a recipient, the candle personality adapts subtly over time based on my preferences and interactions — e.g., if I always light it in the evening it begins opening with a calming evening phrase. | 🟡 | api, device | Personality #8 |
| 14.9 | As the device, I detect physical interactions beyond flame on/off (e.g., a gentle tap on the base, proximity of a hand) and trigger a personality-appropriate voice response or lighting change. | 🟡 | device, api | Personality #9 |
| 14.10 | As a gift-giver purchasing the candle, I complete a guided setup flow that collects the recipient's name, relationship, occasion, and preferred tone — and uses these to pre-configure the personality, voice, and a first surprise message ready for the first lighting. | 🔴 | portal, api | Personality #10 |

---

## Epic 15 — PicoClaw LLM Orchestration Layer

PicoClaw (https://picoclaw.io) runs as a daemon on the RPi, connecting a local LLM
(via Ollama) to the sensors, speaker, LED, and cloud through MCP servers.
Each MCP server wraps one concern and is called as a tool by the LLM agent.

| # | User story | Priority | Layer | Source |
|---|---|---|---|---|
| 15.1 | As a developer, I can deploy the PicoClaw ARM64 binary to the Pi via `deploy.sh` so that the AI orchestration layer is installed in one step alongside the Python code. | 🔴 | device | Architecture |
| 15.2 | As the system, PicoClaw is configured with a `model_list` pointing at the local Ollama instance (e.g. `ollama/gemma2:2b`) so that all LLM inference runs locally without internet. | 🔴 | device | Architecture / offline-first |
| 15.3 | As the LLM agent, I can call a `sensor` MCP server to get the current flame state, active burn session duration, and total burn history so that I can reason about context before speaking. | 🔴 | device | Backlog 13.3, 13.5 |
| 15.4 | As the LLM agent, I can call an `audio` MCP server to play a pre-generated audio file or speak a short synthesised phrase so that voice output is driven by reasoning, not hardcoded logic. | 🔴 | device | Replaces candle_voice.py hello/goodbye |
| 15.5 | As the LLM agent, I can call a `messages` MCP server to fetch unplayed gift-giver messages and mark them as played so that emotional messages are delivered at the right moment. | 🔴 | device, api | Backlog 7.5, 14.5 |
| 15.6 | As the LLM agent, I can call a `led` MCP server to set the LED ring colour and pattern so that lighting reflects the active personality and event state. | 🟠 | device | Backlog 14.6 |
| 15.7 | As the LLM agent, I can call a `cloud` MCP server to push burn session data and pull the latest device config so that the Pi and cloud stay in sync. | 🟠 | device, api | Backlog 13.5, 13.6 |
| 15.8 | As the system, PicoClaw is configured with a system prompt that encodes the candle's personality, the owner's name, and behavioural rules (keep speech short, respond to events, don't repeat messages) so that every interaction is consistent with the chosen character. | 🔴 | device | Backlog 14.1–14.4 |
| 15.9 | As the system, PicoClaw's JSONL memory store persists personality state, played message IDs, and burn session events so that context survives device reboots. | 🟠 | device | Backlog 14.8 |
| 15.10 | As a developer, I can swap the `model_list` entry between `ollama/gemma2:2b` (local, RPi) and `anthropic/claude-haiku-4-5` (cloud, dev machine) without changing any other config so that the same setup works in development and production. | 🟡 | device | Developer experience |

---

## Summary by Layer

### Device (RPi firmware)
Items: 4.1, 4.3, 4.4, 6.3, 6.4, 7.5, 7.6, 8.1, 8.3, 11.2, 11.3, 11.5,
13.2, 13.3, 13.5, 13.6, 13.7, 13.9, 14.3, 14.4, 14.6, 14.8, 14.9,
15.1–15.10

### Cloud API (backend)
Items: 1.1–1.5, 2.1–2.4, 3.1–3.5, 4.1–4.7, 5.1–5.4, 6.3–6.4, 6.6, 7.3–7.5,
8.1–8.4, 9.4, 11.2–11.5, 12.1–12.5,
13.1–13.9, 14.1–14.10

### Web Portal (gift-giver / recipient)
Items: 1.1–1.5, 2.1–2.6, 3.1–3.5, 5.1–5.3, 6.1–6.5, 7.1–7.4, 8.2–8.3,
9.1–9.3, 10.1–10.7, 11.1, 11.4–11.5, 12.1,
13.1, 13.4, 13.6, 13.7, 13.8, 14.1, 14.2, 14.5, 14.7, 14.10

---

## Must-Have for Launch (🔴)

| # | Item |
|---|---|
| 1.1–1.4 | Account creation, editing, deletion |
| 2.1–2.4 | Voice consent flow, unbundled consent, consent records |
| 2.5 | Cookie consent banner |
| 3.1–3.3 | Data export, message list, message deletion |
| 4.1–4.3 | TLS, encryption at rest, unique device credentials |
| 4.5 | Data breach alert to admin |
| 5.1, 5.2, 5.4 | Retention settings, auto-delete, post-closure purge |
| 6.1–6.3 | AI disclosure at first use, AI explanation page, AI on/off control |
| 7.1, 7.5, 7.6 | Send message, device playback, mic active indicator |
| 9.1, 9.3, 9.4 | Product QR info page, Message QR portal, unique device ID |
| 10.1–10.5, 10.7 | Privacy policy, T&C, legal mentions, withdrawal flow, FR/NL support |
| 11.1 | Device pairing via QR |
| 12.2 | Breach alert to admin |
| 13.1–13.5 | QR provisioning, cloud config fetch, sensor auto-config, dashboard, data sync |
| 14.1–14.5, 14.10 | Personality assignment, custom messages, AI generation, event triggers, purchase setup |
| 15.1–15.5, 15.8 | PicoClaw deploy, Ollama config, sensor/audio/message MCP servers, system prompt |
