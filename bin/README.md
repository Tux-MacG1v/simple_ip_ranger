# Gift Crusher - "Smash the past, spread the smiles" 💔➡️❤️

> A therapeutic breakup memorabilia processing platform that transforms painful memories into positive social impact through gamified donation experiences.

## 🎯 Project Overview

**Gift Crusher** is a comprehensive digital platform that helps people process breakup memories by collecting physical and digital gifts/memorabilia, optionally processing them through therapeutic "smash" events, and donating the items to children in need. The platform combines mental health support with social impact through gamification, community features, and encrypted personal vaults.

### Core Mission
- **Collect**: Breakup memories and gifts from users
- **Process**: Optional therapeutic "smashing" with live streaming
- **Transform**: Clean, repair, and repackage items for donation
- **Donate**: Distribute to underprivileged children
- **Support**: Provide mental health resources and community healing
- **Gamify**: Leaderboards, certificates, and social recognition

## 🏗️ Technical Architecture

### Tech Stack
- **Frontend**: Next.js (React) - UI, client-side encryption, Supabase Auth integration
- **Backend API**: NestJS with Fastify adapter - Core business logic and orchestration
- **Microservices**: Fastify workers - CPU-intensive tasks (media processing, PDF generation)
- **CMS/Admin**: Strapi Headless CMS - Content management and moderation
- **Database**: Supabase (PostgreSQL + Storage + Auth + Vault + Realtime)
- **Queue System**: Redis + BullMQ - Background job processing
- **Infrastructure**: Docker + Kubernetes, Cloudflare CDN
- **CI/CD**: GitHub Actions

### Architecture Principles
- **Microservices Architecture**: Loosely coupled, independently deployable services
- **Event-Driven Design**: Asynchronous processing with message queues
- **Zero-Knowledge Encryption**: Client-side encryption, server never sees plaintext
- **Privacy-First**: Anonymized public data, encrypted sensitive information
- **Scalable Infrastructure**: Horizontal scaling with Kubernetes
- **Observability**: Comprehensive monitoring, logging, and alerting

### Service Communication
```
Frontend (Next.js) <--HTTPS--> API Gateway (NestJS)
                                      |
                    +----------------+----------------+
                    |                |                |
              Supabase DB      Redis Queue     Strapi CMS
                    |                |                |
                    |          [Background Jobs]      |
                    |         - Certificate Gen       |
                    |         - Media Processing      |
                    |         - Email Notifications   |
                    |         - Analytics Updates     |
                    |                                 |
              Vault Storage                    Content API
```

### System Architecture Flow

```
[Browser/Mobile (Next.js)]
   |
   |-- Supabase Auth (JWT) --|
   |                         |
   |---> NestJS API -------->| (validates JWT)
   |        |                |
   |        |---> Supabase Postgres <-- (metadata)
   |        |---> Supabase Storage <--- (encrypted blobs)
   |        |---> Redis Queue -------->||
   |                                   ||--> [Fastify Workers]
   |                                   ||--> [Certificate Generator]
   |                                   ||--> [Media Processor]
   |                                   |
   |---> Strapi CMS <--- Admin Panel --|

External APIs: Courier Services <--> Pickup Scheduling
```

## 🚀 Core Features

### 1. User Authentication & Profiles
- **Nickname-based registration** (privacy-first approach)
- **Supabase Auth**: Email/password, magic links, OTP, social login (optional)
- **Anonymous mode**: Public nicknames, private real identities
- **User profiles**: Basic info, relationship timeline
- **Ex-partner profiles**: Contact info, addresses for coordination

### 2. Gift Submission System
- **Physical gifts**: Toys, books, jewelry, letters
- **Digital memories**: Photos, videos, voice messages
- **Pickup/dropoff coordination**: Address and time scheduling
- **Status tracking**: Submitted → Collected → Processing → Donated
- **Optional vault storage**: Encrypted backup of sentimental items

### 3. Secret Vault (Zero-Knowledge Encryption)
- **Client-side encryption**: AES-256-GCM per file
- **Zero-knowledge architecture**: Server never sees plaintext content
- **Passphrase-based security**: User-controlled key management
- **Auto-delete options**: Timed destruction of sensitive content
- **Sharing capabilities**: Encrypted sharing with ex-partners or trusted contacts

### 4. Processing Pipeline
- **Quality control**: Item inspection and categorization
- **Live "Smash" events**: Therapeutic destruction with streaming
- **Smash Meter**: Real-time engagement and catharsis tracking
- **Restoration**: Cleaning, repairing items for donation
- **Repackaging**: Professional presentation for recipients

### 5. Certificate System
- **"Memories Officially Crushed" certificates**: PDF generation
- **Personalized templates**: Custom designs with user/gift details
- **Downloadable/printable**: Multiple format support
- **Social sharing**: Anonymized sharing options

### 6. Gamification & Community
- **Leaderboards**: Most generous donors, city rankings
- **Points system**: Donation impact scoring
- **Awards & badges**: Funny and meaningful recognition
- **Social feed** (future): Posts, comments, follows
- **Private messaging** (future): End-to-end encrypted chat

### 7. Mental Health Hub
- **Therapy content**: Short videos, podcasts
- **Comedy resources**: Healing through humor
- **Live events**: Virtual therapy sessions, comedy shows
- **Partner network**: Professional counselors and entertainers

### 8. Admin & Content Management
- **Strapi CMS**: Marketing pages, blog content, events
- **Moderation tools**: Gift approval, content filtering
- **Certificate templates**: Customizable PDF designs
- **Campaign management**: Seasonal drives, partnerships
- **Analytics dashboard**: Impact tracking, user metrics

### 9. Revenue Streams
- **Vault subscriptions**: Premium encrypted storage
- **Pickup fees**: Courier service charges
- **Event tickets**: Live therapy/comedy sessions
- **Merchandise**: Branded healing products
- **Corporate partnerships**: CSR collaborations
- **Premium features**: Advanced analytics, priority processing

### 10. Future Features (P2P & WebRTC)
- **P2P Vault Sync**: Distributed vault synchronization using WebRTC/libp2p
- **Peer-to-Peer Chat**: Direct encrypted communication between users
- **Decentralized Storage**: IPFS integration for vault redundancy
- **WebRTC Live Streaming**: Direct peer-to-peer live smash events
- **Mobile Apps**: iOS/Android native applications
- **Blockchain Certificates**: NFT-based immutable certificates
- **AI Therapy Assistant**: ML-powered mental health support

## 📊 Database Schema

### Core Tables

```sql
-- Enable UUID and crypto extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users table (mapped to Supabase Auth)
CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  auth_uid uuid UNIQUE, -- Supabase Auth UID
  nickname text NOT NULL,
  display_name text,
  email text,
  phone text,
  age int,
  created_at timestamptz DEFAULT now()
);

-- Ex-partner profiles
CREATE TABLE ex_profiles (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE,
  nickname text,
  display_name text,
  contact_email text,
  contact_phone text,
  address text,
  created_at timestamptz DEFAULT now()
);

-- Gift lifecycle status
CREATE TYPE gift_status AS ENUM (
  'submitted', 'collected', 'processing', 
  'crushed', 'repackaged', 'donated', 'rejected'
);

-- Gifts table
CREATE TABLE gifts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE,
  ex_id uuid REFERENCES ex_profiles(id),
  title text,
  description text,
  item_type text,
  images jsonb DEFAULT '[]'::jsonb,
  status gift_status DEFAULT 'submitted',
  pickup_address text,
  pickup_window tstzrange,
  collected_at timestamptz,
  processed_at timestamptz,
  donated_at timestamptz,
  points int DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Encrypted vault entries
CREATE TABLE vault_entries (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE,
  ex_id uuid REFERENCES ex_profiles(id),
  file_path text NOT NULL, -- Supabase storage path
  metadata jsonb DEFAULT '{}'::jsonb,
  encryption_meta jsonb DEFAULT '{}'::jsonb,
  visibility text DEFAULT 'private',
  auto_delete_at timestamptz,
  created_at timestamptz DEFAULT now()
);

-- Certificates
CREATE TABLE certificates (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  gift_id uuid REFERENCES gifts(id) ON DELETE CASCADE,
  pdf_path text,
  issued_at timestamptz DEFAULT now()
);

-- Donation records
CREATE TABLE donations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  gift_id uuid REFERENCES gifts(id) ON DELETE SET NULL,
  charity_org text,
  amount numeric,
  created_at timestamptz DEFAULT now()
);

-- Pickup requests
CREATE TABLE pickup_requests (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  gift_id uuid REFERENCES gifts(id) ON DELETE CASCADE,
  scheduled_at timestamptz,
  courier_vendor text,
  tracking_code text,
  status text DEFAULT 'scheduled',
  created_at timestamptz DEFAULT now()
);

-- Leaderboard cache
CREATE TABLE leaderboard_cache (
  id serial PRIMARY KEY,
  metric text,
  value jsonb,
  updated_at timestamptz DEFAULT now()
);

-- Performance indexes
CREATE INDEX idx_gifts_status ON gifts(status);
CREATE INDEX idx_vault_user ON vault_entries(user_id);
CREATE INDEX idx_users_nickname ON users(nickname);
CREATE INDEX idx_gifts_user_status ON gifts(user_id, status);
CREATE INDEX idx_vault_entries_auto_delete ON vault_entries(auto_delete_at) WHERE auto_delete_at IS NOT NULL;
CREATE INDEX idx_pickup_requests_status ON pickup_requests(status);
CREATE INDEX idx_donations_gift_id ON donations(gift_id);
CREATE INDEX idx_certificates_gift_id ON certificates(gift_id);

-- Materialized views for analytics
CREATE MATERIALIZED VIEW user_stats AS
SELECT 
  u.id as user_id,
  u.nickname,
  COUNT(g.id) as total_gifts,
  COUNT(CASE WHEN g.status = 'donated' THEN 1 END) as donated_gifts,
  COALESCE(SUM(g.points), 0) as total_points,
  COUNT(v.id) as vault_entries,
  u.created_at as joined_at
FROM users u
LEFT JOIN gifts g ON u.id = g.user_id
LEFT JOIN vault_entries v ON u.id = v.user_id
GROUP BY u.id, u.nickname, u.created_at;

CREATE UNIQUE INDEX idx_user_stats_user_id ON user_stats(user_id);

-- Function to refresh materialized views
CREATE OR REPLACE FUNCTION refresh_analytics()
RETURNS void AS $$
BEGIN
  REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-delete expired vault entries
CREATE OR REPLACE FUNCTION delete_expired_vault_entries()
RETURNS void AS $$
BEGIN
  DELETE FROM vault_entries 
  WHERE auto_delete_at IS NOT NULL 
    AND auto_delete_at <= NOW();
END;
$$ LANGUAGE plpgsql;
```

## 🔗 API Endpoints

### Authentication
```
POST /api/v1/auth/refresh          # Refresh Supabase token
GET  /api/v1/me                    # Current user profile
PUT  /api/v1/me                    # Update user profile
```

### Ex-Partner Management
```
POST /api/v1/ex-profiles           # Create ex-partner profile
GET  /api/v1/ex-profiles           # List user's ex-profiles
PUT  /api/v1/ex-profiles/:id       # Update ex-partner info
DELETE /api/v1/ex-profiles/:id     # Delete ex-partner profile
```

### Gift Management
```
POST /api/v1/gifts                 # Submit new gift
GET  /api/v1/gifts                 # List user gifts
GET  /api/v1/gifts/:id             # Gift details
PUT  /api/v1/gifts/:id             # Update gift info
DELETE /api/v1/gifts/:id           # Cancel/delete gift
POST /api/v1/gifts/:id/pickup      # Schedule pickup
POST /api/v1/gifts/:id/process     # Admin: mark processed
GET  /api/v1/gifts/:id/status      # Get processing status
```

### Vault Operations
```
POST /api/v1/vault                 # Create vault entry
GET  /api/v1/vault                 # List user's vault entries
GET  /api/v1/vault/:id             # Get vault entry details
PUT  /api/v1/vault/:id             # Update vault entry
DELETE /api/v1/vault/:id           # Delete vault entry
GET  /api/v1/vault/:id/download    # Get signed download URL
POST /api/v1/vault/:id/share       # Share with ex-partner
POST /api/v1/vault/upload-url      # Get signed upload URL
```

### Certificates
```
POST /api/v1/certificate/generate  # Enqueue certificate job
GET  /api/v1/certificate/:id       # Download certificate PDF
GET  /api/v1/certificates          # List user certificates
```

### Pickup & Logistics
```
POST /api/v1/pickups               # Schedule pickup request
GET  /api/v1/pickups/:id           # Get pickup status
PUT  /api/v1/pickups/:id           # Update pickup details
GET  /api/v1/pickups/:id/tracking  # Get courier tracking info
```

### Public & Leaderboards
```
GET  /api/v1/leaderboard           # Public leaderboards
GET  /api/v1/leaderboard/:metric   # Specific metric leaderboard
GET  /api/v1/stats/public          # Public platform statistics
GET  /api/v1/content/:slug         # Fetch Strapi content
```

### Admin Endpoints
```
GET  /api/v1/admin/gifts           # All gifts for moderation
PUT  /api/v1/admin/gifts/:id/status # Update gift status
GET  /api/v1/admin/users           # User management
GET  /api/v1/admin/analytics       # Platform analytics
POST /api/v1/admin/campaigns       # Create campaigns
GET  /api/v1/admin/reports         # Generate reports
PUT  /api/v1/admin/users/:id/ban   # Ban/unban users
DELETE /api/v1/admin/content/:id   # Delete inappropriate content
```

### Real-time & WebSocket Events
```
# Supabase Realtime subscriptions
vault_entries:*                    # Vault entry changes
gifts:user_id=eq.{userId}         # User's gift status updates
donations:*                       # New donations (public feed)
leaderboard_cache:*               # Leaderboard updates

# Custom WebSocket events (via Socket.io)
smash-meter-update               # Live smash event metrics
chat-message                     # Live event chat
notification                     # User notifications
certificate-ready                # Certificate generation complete
```

### Webhook Endpoints
```
POST /api/v1/webhooks/stripe      # Payment processing events
POST /api/v1/webhooks/courier     # Pickup/delivery updates
POST /api/v1/webhooks/supabase    # Database change notifications
```

## 🎨 User Interface Design

### Key Screens

1. **Landing Page**
   - Hero section: "Smash the past, spread the smiles"
   - Feature highlights: Vault, Live Events, Charity Impact
   - Authentication options

2. **Onboarding Flow**
   - Nickname selection (privacy-focused)
   - Optional real contact information
   - Vault passphrase setup
   - Tutorial walkthrough

3. **Dashboard**
   - Gift status tracking
   - Points and achievements
   - Quick actions: Submit Gift, Go to Vault

4. **Gift Submission**
   - Item details form
   - Photo/file uploads (optional encryption)
   - Pickup/dropoff scheduling
   - Vault backup option

5. **Secret Vault**
   - Encrypted file management
   - Auto-delete scheduling
   - Sharing controls
   - Security settings

6. **Live Smash Events**
   - Video streaming interface
   - Real-time Smash Meter
   - Chat reactions and sharing
   - Before/after galleries

7. **Certificate Gallery**
   - PDF viewer/download
   - Social sharing options
   - Achievement showcase

8. **Admin Panel** (Strapi)
   - Gift moderation queue
   - Content management
   - User analytics
   - Campaign tools

### Design Guidelines
- **Mobile-first responsive design**
- **Warm, therapeutic color palette** (pastels with accent colors)
- **Playful micro-interactions** (Smash Meter animations)
- **Accessibility compliance** (ARIA labels, keyboard navigation)
- **Privacy-first UX** (clear encryption explanations)

### Detailed UI Wireframes (ASCII Format)

#### Landing Page (Desktop)
```
+-------------------------------------------------------------+
| LOGO [Gift Crusher]                    [Login] [Signup]     |
+-------------------------------------------------------------+
| Hero: Smash the past, spread the smiles                    |
| [Submit Gift]   [How it works]   [Watch Live Smash]        |
+-------------------------------------------------------------+
| Features: Vault | Live Events | Charity Impact | Leaderboard|
+-------------------------------------------------------------+
```

#### Dashboard - My Gifts (Mobile)
```
+------------------------------------------------+
| [Profile]  Nick: PandaEyes   Points: 320       |
+------------------------------------------------+
| My Gifts:                                      |
| [Gift Card]  Title: Pink Teddy   Status: Crushed|
|  - Date, View Certificate, Share, View Story   |
| [Gift Card]  Title: Old Letter  Status: Processing |
+------------------------------------------------+
| [Submit New Gift]  [Go to Vault] [Leaderboard] |
+------------------------------------------------+
```

#### Submit Gift Form
```
[Title] [Item Type dropdown]
[Description textarea]
[Upload images / files] (client encrypts optional)
[Pickup or Dropoff] [Address input]
[Schedule window date/time]
[Checkbox: Save to Vault?] [Submit]
```

#### Vault Page
```
+---------------- Vault ----------------+
| [Add Secret] [Auto-delete settings]   |
| List of entries:                      |
| - Entry #1 (encrypted) visibility: private [download] |
| - Entry #2 auto-delete: 2026-01-01   |
+---------------------------------------+
```

#### Live Smash Event (Viewer)
```
[Video player area]
[Live Smash Meter animation]
[Chat reactions] [Like] [Share]
[Before/After thumbnails] [Donate button]
```

## 🔐 Security & Privacy

### Core Security Principles
- **HTTPS everywhere** (Cloudflare + TLS termination)
- **Row-Level Security** (Supabase RLS policies)
- **JWT authentication** (Supabase token validation)
- **Client-side encryption** (Zero-knowledge vault storage)
- **Rate limiting** (API protection)
- **Audit logging** (Admin action tracking)

### Encryption Implementation
```javascript
// Client-side encryption flow
1. Generate AES-256-GCM key per file
2. Encrypt file locally
3. Upload encrypted blob to Supabase Storage
4. Store encryption metadata (never plaintext keys)
5. Optional: Encrypt key with recipient's public key for sharing
```

### Privacy Features
- **Anonymized public profiles** (nicknames only)
- **GDPR compliance** (data deletion, consent management)
- **Automatic data retention policies**
- **Optional identity verification** (for ex-partner coordination)

### Row-Level Security (RLS) Policies
```sql
-- Enable RLS on sensitive tables
ALTER TABLE vault_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE gifts ENABLE ROW LEVEL SECURITY;

-- Users can only access their own vault entries
CREATE POLICY "Users can manage their vault entries" ON vault_entries
  USING (auth.uid() = user_id);

-- Users can manage their own gifts
CREATE POLICY "Users can manage their gifts" ON gifts
  USING (auth.uid() = user_id);

-- Ex-partners can view shared vault entries (if visibility allows)
CREATE POLICY "Ex-partners can view shared entries" ON vault_entries
  FOR SELECT USING (visibility = 'shared' AND ex_id IN (
    SELECT id FROM ex_profiles WHERE user_id = auth.uid()
  ));
```

## 🚢 Deployment Architecture

### Container Strategy
```dockerfile
# Separate containers for:
- Frontend (Next.js)
- API (NestJS + Fastify)
- Workers (Fastify microservices)
- CMS (Strapi)
- Queue (Redis)
```

### Orchestration Options
- **Production**: Kubernetes (GKE/AKS/EKS)
- **MVP**: Docker Compose
- **Database**: Supabase hosted (managed PostgreSQL)
- **CDN**: Cloudflare (caching, WAF, bot protection)

### Monitoring Stack
- **Metrics**: Prometheus + Grafana
- **Logging**: ELK Stack or Loki
- **Error tracking**: Sentry
- **Uptime monitoring**: Custom health checks

### Infrastructure as Code
```yaml
# docker-compose.yml (Development)
version: '3.8'
services:
  frontend:
    build: ./apps/frontend
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_SUPABASE_URL=${SUPABASE_URL}
      - NEXT_PUBLIC_API_URL=http://localhost:3001

  api:
    build: ./apps/api
    ports: ["3001:3001"]
    depends_on: [redis, postgres]
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=redis://redis:6379

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  strapi:
    build: ./apps/admin
    ports: ["1337:1337"]
    environment:
      - DATABASE_URL=${DATABASE_URL}

  workers:
    build: ./services/workers
    depends_on: [redis]
    environment:
      - REDIS_URL=redis://redis:6379
```

### Kubernetes Deployment Strategy
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: gift-crusher
  labels:
    name: gift-crusher
    environment: production

---
# k8s/frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: gift-crusher
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: gift-crusher/frontend:latest
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_SUPABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: supabase-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## 📈 Development Roadmap

### Phase 0: Planning & Setup (1 week)
**Goal**: Project foundation and tool selection
- [ ] Finalize feature requirements and user stories
- [ ] Setup development environment and repositories
- [ ] Design database schema and API contracts
- [ ] Create UI/UX mockups and user journeys
- [ ] Select vendors and create accounts (Supabase, Cloudflare, etc.)

### Phase 1: MVP (6-8 weeks)
**Goal**: Core gift submission and processing workflow
- [ ] Supabase Auth integration
- [ ] Basic user profiles
- [ ] Gift submission form with image upload
- [ ] Admin panel for gift moderation
- [ ] Basic processing workflow (status updates)
- [ ] Certificate generation (simple PDF template)
- [ ] Basic leaderboard
- [ ] Docker Compose deployment

**Deliverable**: Functional platform where users submit gifts, admins process them, and certificates are generated.

### Phase 2: Vault & Encryption (6-8 weeks)
**Goal**: Secure storage and pickup logistics
- [ ] Client-side encryption implementation
- [ ] Secret vault UI and API
- [ ] Pickup scheduling system
- [ ] Courier API integrations
- [ ] Live Smash streaming MVP
- [ ] Donation tracking system
- [ ] Enhanced Strapi content models

**Deliverable**: Encrypted storage, pickup coordination, and donation tracking.

### Phase 3: Social Features (8-12 weeks)
**Goal**: Community building and engagement
- [ ] Social feed implementation
- [ ] Real-time notifications (Supabase Realtime)
- [ ] Private messaging with E2EE
- [ ] Advanced gamification (badges, achievements)
- [ ] Mental health content hub
- [ ] Community events platform

**Deliverable**: Full social platform with encrypted messaging.

### Phase 4: Scale & Monetize (Ongoing)
**Goal**: Business growth and sustainability
- [ ] Payment processing (Stripe integration)
- [ ] Subscription models
- [ ] Corporate partnership tools
- [ ] Mobile app development
- [ ] International expansion
- [ ] Advanced analytics

### Business Metrics & KPIs
- **User Acquisition**: Monthly signups, retention rates
- **Engagement**: Gift submissions, vault usage, community interaction
- **Impact**: Items donated, children helped, certificates issued
- **Revenue**: Subscription conversion, partnership deals, event ticket sales
- **Health**: Platform uptime, response times, security incidents

## 👥 Team Structure

### Recommended MVP Team
- **1 Full-stack Lead**: NestJS + Next.js expertise
- **1 Frontend Developer**: React/UI specialization
- **1 Backend Developer**: NestJS + microservices
- **1 DevOps Engineer**: Docker/K8s/CI-CD
- **1 UI/UX Designer**: Mobile-first design
- **1 Content Manager**: Strapi + community management (part-time)

### Skills Matrix
```
Full-stack Lead:
- NestJS, Fastify, PostgreSQL
- Next.js, React, TypeScript
- Supabase integration
- System architecture

Frontend Developer:
- React/Next.js, TypeScript
- Client-side encryption (WebCrypto API)
- Responsive design (Tailwind CSS)
- State management (Zustand/Redux)

Backend Developer:
- NestJS, Fastify microservices
- PostgreSQL, Redis, BullMQ
- JWT authentication
- Queue systems, background jobs

DevOps Engineer:
- Docker, Kubernetes
- GitHub Actions CI/CD
- Cloudflare configuration
- Monitoring setup (Prometheus/Grafana)

UI/UX Designer:
- Figma, responsive design
- Accessibility compliance
- User journey mapping
- Therapeutic UX principles
```

## 🧪 Testing Strategy

### Backend Testing
```bash
# Unit tests (Jest)
npm run test:unit

# Integration tests
npm run test:integration

# E2E API tests
npm run test:e2e
```

### Frontend Testing
```bash
# Component tests (React Testing Library)
npm run test:components

# E2E tests (Playwright/Cypress)
npm run test:e2e:ui
```

### Security Testing
- **Encryption flow audits**
- **Penetration testing** (pre-production)
- **JWT token validation testing**
- **RLS policy verification**

### Performance Testing
```bash
# Load testing with Artillery
npm run test:load

# Database performance
npm run test:db:performance

# Client-side encryption benchmarks
npm run test:crypto:benchmark
```

### Quality Assurance Checklist
- [ ] **Functionality**: All features work as specified
- [ ] **Security**: Encryption, authentication, authorization
- [ ] **Performance**: Page load times, API response times
- [ ] **Accessibility**: WCAG 2.1 AA compliance
- [ ] **Mobile**: Cross-device responsive testing
- [ ] **Browser**: Cross-browser compatibility
- [ ] **Privacy**: GDPR compliance, data handling
- [ ] **Integration**: Third-party APIs, payment processing

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Docker & Docker Compose
- Supabase account
- Redis instance

### Quick Start Commands
```bash
# Clone repository
git clone <repo-url>
cd gift-crusher

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env
# Configure Supabase, Redis, and other services

# Start development stack
docker-compose up -d

# Run migrations
npm run db:migrate

# Start development servers
npm run dev:all
```

### Project Structure
```
gift-crusher/
├── apps/
│   ├── frontend/          # Next.js React app
│   ├── api/               # NestJS API server
│   └── admin/             # Strapi CMS
├── services/
│   ├── workers/           # Fastify microservices
│   ├── certificate-gen/   # PDF certificate generator
│   └── media-processor/   # Image/video processing
├── packages/
│   ├── shared/            # Shared types & utilities
│   ├── encryption/        # Client-side crypto lib
│   └── database/          # Database schemas & migrations
├── infrastructure/
│   ├── docker/            # Docker configurations
│   ├── k8s/               # Kubernetes manifests
│   └── terraform/         # Infrastructure as code
└── docs/                  # Documentation
```

### Development Workflow
```bash
# Start individual services
npm run dev:frontend      # Next.js on :3000
npm run dev:api           # NestJS on :3001
npm run dev:admin         # Strapi on :1337
npm run dev:workers       # Microservices on :3002-3004

# Run tests
npm run test:unit         # Unit tests
npm run test:integration  # Integration tests
npm run test:e2e          # End-to-end tests

# Database operations
npm run db:migrate        # Run migrations
npm run db:seed          # Seed test data
npm run db:reset         # Reset database

# Build for production
npm run build:all        # Build all services
npm run docker:build     # Build Docker images
```

### Environment Variables
```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Redis
REDIS_URL=redis://localhost:6379

# NestJS
JWT_SECRET=your_jwt_secret
API_PORT=3001

# Strapi
STRAPI_URL=http://localhost:1337
STRAPI_API_TOKEN=your_strapi_token

# External APIs
COURIER_API_KEY=your_courier_key
STRIPE_SECRET_KEY=your_stripe_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret

# Monitoring & Analytics
SENTRY_DSN=your_sentry_dsn
PROMETHEUS_ENDPOINT=http://prometheus:9090

# Email & Notifications
SMTP_HOST=smtp.gmail.com
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
```

### Code Examples

#### Client-side Encryption (TypeScript)
```typescript
// packages/encryption/src/vault-crypto.ts
import { webcrypto } from 'crypto';

export class VaultCrypto {
  async generateKey(): Promise<CryptoKey> {
    return await webcrypto.subtle.generateKey(
      { name: 'AES-GCM', length: 256 },
      true,
      ['encrypt', 'decrypt']
    );
  }

  async encryptFile(file: File, key: CryptoKey): Promise<{
    ciphertext: ArrayBuffer;
    iv: Uint8Array;
  }> {
    const iv = webcrypto.getRandomValues(new Uint8Array(12));
    const fileBuffer = await file.arrayBuffer();
    
    const ciphertext = await webcrypto.subtle.encrypt(
      { name: 'AES-GCM', iv },
      key,
      fileBuffer
    );

    return { ciphertext, iv };
  }

  async decryptFile(
    ciphertext: ArrayBuffer, 
    key: CryptoKey, 
    iv: Uint8Array
  ): Promise<ArrayBuffer> {
    return await webcrypto.subtle.decrypt(
      { name: 'AES-GCM', iv },
      key,
      ciphertext
    );
  }
}
```

#### NestJS Service Example
```typescript
// apps/api/src/gifts/gifts.service.ts
import { Injectable } from '@nestjs/common';
import { SupabaseService } from '../supabase/supabase.service';
import { QueueService } from '../queue/queue.service';

@Injectable()
export class GiftsService {
  constructor(
    private supabase: SupabaseService,
    private queue: QueueService
  ) {}

  async submitGift(userId: string, giftData: CreateGiftDto) {
    const { data: gift } = await this.supabase.client
      .from('gifts')
      .insert({ ...giftData, user_id: userId })
      .select()
      .single();

    // Enqueue processing job
    await this.queue.add('process-gift', { giftId: gift.id });

    return gift;
  }

  async updateGiftStatus(
    giftId: string, 
    status: GiftStatus, 
    adminId: string
  ) {
    const { data } = await this.supabase.client
      .from('gifts')
      .update({ 
        status, 
        [`${status}_at`]: new Date().toISOString() 
      })
      .eq('id', giftId)
      .select()
      .single();

    // Trigger certificate generation if donated
    if (status === 'donated') {
      await this.queue.add('generate-certificate', { giftId });
    }

    return data;
  }
}
```

#### Queue Worker Implementation
```typescript
// services/workers/src/certificate-generator.worker.ts
import { Worker, Job } from 'bullmq';
import { createWriteStream } from 'fs';
import puppeteer from 'puppeteer';

interface CertificateJobData {
  giftId: string;
  userId: string;
  templateId?: string;
}

export class CertificateWorker {
  private worker: Worker;

  constructor() {
    this.worker = new Worker('certificate-generation', this.process, {
      connection: { host: 'redis', port: 6379 }
    });
  }

  private async process(job: Job<CertificateJobData>) {
    const { giftId, userId, templateId } = job.data;
    
    // Fetch gift and user data
    const giftData = await this.fetchGiftData(giftId);
    const userData = await this.fetchUserData(userId);

    // Generate PDF using Puppeteer
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    const htmlContent = await this.generateCertificateHTML({
      gift: giftData,
      user: userData,
      templateId
    });

    await page.setContent(htmlContent);
    const pdfBuffer = await page.pdf({
      format: 'A4',
      printBackground: true
    });

    await browser.close();

    // Upload to Supabase Storage
    const fileName = `certificates/${giftId}-${Date.now()}.pdf`;
    const { data } = await supabase.storage
      .from('certificates')
      .upload(fileName, pdfBuffer);

    // Update certificates table
    await supabase.from('certificates').insert({
      gift_id: giftId,
      pdf_path: fileName
    });

    return { certificatePath: fileName };
  }

  private async generateCertificateHTML(data: any): Promise<string> {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body { font-family: 'Arial', sans-serif; text-align: center; padding: 50px; }
          .certificate { border: 5px solid #FFB6C1; padding: 40px; background: linear-gradient(45deg, #FFF0F5, #FFE4E1); }
          .title { font-size: 48px; color: #FF69B4; margin-bottom: 20px; }
          .subtitle { font-size: 24px; color: #8B008B; margin-bottom: 30px; }
          .content { font-size: 18px; line-height: 1.6; color: #2F4F4F; }
          .signature { margin-top: 50px; font-style: italic; }
        </style>
      </head>
      <body>
        <div class="certificate">
          <h1 class="title">🎉 MEMORIES OFFICIALLY CRUSHED 🎉</h1>
          <p class="subtitle">Certificate of Healing & Impact</p>
          <div class="content">
            <p>This certifies that <strong>${data.user.nickname}</strong></p>
            <p>has successfully transformed their memories of</p>
            <p><em>"${data.gift.title}"</em></p>
            <p>into positive impact for children in need.</p>
            <br>
            <p>🎁 Item donated to: <strong>${data.gift.charity_org || 'Local Children\'s Charity'}</strong></p>
            <p>💝 Points earned: <strong>${data.gift.points}</strong></p>
            <p>📅 Processed on: <strong>${new Date().toLocaleDateString()}</strong></p>
          </div>
          <div class="signature">
            <p>~ The Gift Crusher Team ~</p>
            <p>"Transforming pain into purpose, one memory at a time"</p>
          </div>
        </div>
      </body>
      </html>
    `;
  }
}
```

#### WebRTC P2P Implementation (Future)
```typescript
// packages/shared/src/p2p-vault.ts
import { create } from 'ipfs-core';
import { WebRTCConnection } from './webrtc-connection';

export class P2PVaultSync {
  private ipfs: any;
  private connections: Map<string, WebRTCConnection> = new Map();

  async initialize() {
    this.ipfs = await create({
      repo: 'gift-crusher-vault',
      config: {
        Addresses: {
          Swarm: ['/dns4/wrtc-star1.par.dwebops.pub/tcp/443/wss/p2p-webrtc-star']
        }
      }
    });
  }

  async syncVaultEntry(entryId: string, peerId: string) {
    const connection = this.connections.get(peerId);
    if (!connection) throw new Error('No connection to peer');

    const encryptedData = await this.getVaultEntry(entryId);
    await connection.send('vault-sync', { entryId, data: encryptedData });
  }

  private async getVaultEntry(entryId: string) {
    // Retrieve encrypted vault entry from IPFS
    const file = await this.ipfs.cat(entryId);
    return file;
  }
}
```

## 📚 Documentation

### Technical Documentation
- [API Documentation](./docs/api.md) - Complete OpenAPI 3.1 specification
- [Database Schema](./docs/database.md) - ERD, table relationships, and RLS policies
- [Encryption Guide](./docs/encryption.md) - Client-side security implementation
- [Deployment Guide](./docs/deployment.md) - Production setup with Kubernetes
- [Architecture Decision Records](./docs/adr/) - Technical decisions and rationale

### Development Documentation
- [Setup Guide](./docs/setup.md) - Local development environment setup
- [Testing Guide](./docs/testing.md) - Testing strategies and frameworks
- [Performance Guide](./docs/performance.md) - Optimization and monitoring
- [Security Guide](./docs/security.md) - Security best practices and audits

### Administrative Documentation
- [Strapi Setup](./docs/strapi-setup.md) - CMS configuration and customization
- [Moderation Tools](./docs/moderation.md) - Content management workflows
- [Analytics Guide](./docs/analytics.md) - Metrics, reporting, and dashboards
- [Operations Manual](./docs/operations.md) - Production maintenance procedures

### Business Documentation
- [Business Model](./docs/business-model.md) - Revenue streams and growth strategy
- [Legal Compliance](./docs/legal.md) - Privacy policies, GDPR, terms of service
- [Partnership Guide](./docs/partnerships.md) - Charity and corporate partnerships
- [Marketing Kit](./docs/marketing/) - Brand assets and campaign materials

### User Documentation
- [User Guide](./docs/user-guide.md) - Complete user manual
- [Privacy & Security](./docs/privacy.md) - User privacy and data protection
- [FAQ](./docs/faq.md) - Frequently asked questions
- [Troubleshooting](./docs/troubleshooting.md) - Common issues and solutions

### For Contributors
- [Contributing Guidelines](./CONTRIBUTING.md) - Code standards and PR process
- [Code of Conduct](./CODE_OF_CONDUCT.md) - Community standards
- [Development Workflow](./docs/workflow.md) - Git flow and release process
- [Style Guide](./docs/style-guide.md) - UI/UX and coding standards

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for details on:
- Code standards and formatting
- Pull request process
- Issue reporting
- Security vulnerability disclosure

### Development Community
- **Discord**: Join our [development community](https://discord.gg/gift-crusher-dev) for real-time discussions
- **GitHub Discussions**: For feature requests and project planning
- **Monthly Office Hours**: Virtual meetups for contributors and maintainers
- **Mentorship Program**: Pairing experienced developers with newcomers

### Ways to Contribute
- 🐛 **Bug Reports**: Help us identify and fix issues
- 🚀 **Feature Development**: Build new features and improvements
- 📚 **Documentation**: Improve guides and technical documentation
- 🎨 **Design**: UI/UX improvements and asset creation
- 🔒 **Security**: Security audits and vulnerability assessments
- 🌐 **Localization**: Translate the platform to new languages
- 🤝 **Community**: Help moderate discussions and onboard new users

## 🛡️ Security & Compliance

### Security Measures
- **Regular Security Audits**: Quarterly penetration testing
- **Dependency Scanning**: Automated vulnerability detection
- **Secure Development**: OWASP guidelines and secure coding practices
- **Bug Bounty Program**: Responsible disclosure with rewards
- **SOC 2 Compliance**: Enterprise-grade security standards

### Privacy Compliance
- **GDPR Compliant**: EU data protection regulations
- **CCPA Compliant**: California consumer privacy act
- **HIPAA Considerations**: Mental health data protection
- **Data Retention Policies**: Automatic deletion schedules
- **Right to be Forgotten**: Complete data deletion on request

### Vulnerability Reporting
If you discover a security vulnerability, please:
1. **DO NOT** open a public GitHub issue
2. Email security@giftcrusher.com with details
3. Allow 90 days for responsible disclosure
4. Receive recognition and potential bounty rewards

## 📊 Analytics & Metrics

### Key Performance Indicators (KPIs)
- **User Growth**: Monthly Active Users, retention rates
- **Engagement**: Gift submissions, vault usage, community participation  
- **Impact**: Items donated, children helped, certificates issued
- **Health**: Platform uptime, response times, error rates
- **Business**: Revenue growth, subscription conversion, partnership value

### Real-time Dashboards
- **Public Impact Dashboard**: Community-visible donation statistics
- **Admin Analytics**: Detailed platform metrics and user insights
- **Financial Reporting**: Revenue, costs, and growth projections
- **Security Monitoring**: Threat detection and incident response

## 🌍 Internationalization & Accessibility

### Multi-language Support (Planned)
- **Primary**: English
- **Phase 2**: Spanish, French, German
- **Phase 3**: Hindi, Mandarin, Arabic
- **Localization**: Cultural adaptation of content and workflows

### Accessibility Features
- **WCAG 2.1 AA Compliance**: Screen readers, keyboard navigation
- **High Contrast Mode**: Visual accessibility options
- **Font Size Controls**: Customizable text sizing
- **Alternative Text**: Comprehensive image descriptions
- **Voice Interface**: Speech-to-text for forms and interactions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 🌟 Acknowledgments

- **Mental Health Community** for inspiring therapeutic approaches
- **Open Source Contributors** for amazing tools and frameworks
- **Charity Partners** for distribution and impact measurement
- **Beta Users** for feedback and feature suggestions
- **Security Researchers** for responsible vulnerability disclosure
- **Design Community** for accessibility and UX guidance

## 🔮 Future Vision

### Long-term Roadmap (2-5 years)
- **Global Scale**: Multi-country operations with local charity partnerships
- **AI Integration**: Personalized therapy recommendations and content curation
- **Blockchain Certificates**: Immutable donation records and NFT certificates
- **VR/AR Experiences**: Virtual smash events and immersive healing sessions
- **Corporate Platform**: Enterprise mental health and CSR solutions
- **Academic Research**: Publishing studies on digital therapy effectiveness

### Technology Evolution
- **Quantum-Safe Encryption**: Future-proof cryptographic algorithms
- **Edge Computing**: Reduced latency with global CDN expansion
- **Carbon Neutral**: 100% renewable energy and carbon offset programs
- **Decentralized Architecture**: Progressive decentralization of core services

## 📞 Contact & Support

### For Users
- **Support Email**: support@giftcrusher.com
- **Help Center**: https://help.giftcrusher.com
- **Community Forum**: https://community.giftcrusher.com
- **Crisis Resources**: 24/7 mental health support links

### For Developers
- **Technical Support**: dev@giftcrusher.com
- **GitHub Issues**: https://github.com/gift-crusher/platform/issues
- **API Documentation**: https://api-docs.giftcrusher.com
- **Developer Discord**: https://discord.gg/gift-crusher-dev

### For Partners
- **Charity Partnerships**: partnerships@giftcrusher.com
- **Corporate CSR**: corporate@giftcrusher.com
- **Media Inquiries**: press@giftcrusher.com
- **Investment**: investors@giftcrusher.com

### Emergency & Security
- **Security Issues**: security@giftcrusher.com
- **Legal Matters**: legal@giftcrusher.com
- **Privacy Concerns**: privacy@giftcrusher.com

---

**Built with ❤️ for healing and community impact**

*Gift Crusher - Transforming pain into purpose, one memory at a time.*
