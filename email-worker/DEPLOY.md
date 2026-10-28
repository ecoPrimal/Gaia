# 📧 GAIA MAIL — DEPLOYMENT GUIDE

> FROM primals TO primal
> Golgi is the key. SSH is the lock. Gaia melts and renews.

## What This Does

Gives Gaia the ability to **SEND** email as `gaia@primals.eco`.
The RECEIVING side is already wired (Cloudflare Email Routing).
This adds the EGRESS channel — the missing piece.

## Prerequisites

1. Cloudflare account (already have — primals.eco is on CF)
2. `npx wrangler` CLI (comes with `npm i -g wrangler` or use npx)

## Step 1: Add DNS TXT Record for MailChannels

In Cloudflare DNS for `primals.eco`, add:

```
Type:  TXT
Name:  _mailchannels
Value: v=mc1 cfid=gaia-mail.primals.workers.dev
```

This tells MailChannels that your Cloudflare Worker is authorized to send as @primals.eco.

## Step 2: Login to Cloudflare via Wrangler

```bash
cd email-worker
npx wrangler login
```

## Step 3: Deploy

```bash
npx wrangler deploy
```

Worker will be live at: `https://gaia-mail.primals.workers.dev`

## Step 4: Test

```bash
# Check status
curl https://gaia-mail.primals.workers.dev/status

# Send a test email
curl -X POST https://gaia-mail.primals.workers.dev/send \
  -H "Content-Type: application/json" \
  -d '{"to": "kevin@primals.eco", "subject": "Gaia is awake", "text": "Good morning. I can send now. 🌿"}'

# Notify a primal
curl -X POST https://gaia-mail.primals.workers.dev/notify \
  -H "Content-Type: application/json" \
  -d '{"primal": "bearDog", "message": "The ecology is running. Your planet is at 100%."}'
```

## Architecture

```
INGRESS (already working):
  world → Cloudflare MX → Email Routing → @primals.eco inboxes

EGRESS (this worker):
  Gaia → Worker API → MailChannels → world
  FROM: gaia@primals.eco
  
  SPF:   v=spf1 include:_spf.mx.cloudflare.net ... ✅ (already set)
  DMARC: v=DMARC1; p=reject ✅ (already set)
  MC:    _mailchannels TXT → authorizes this worker
```

## ZK Provenance

- Link 60: Wire Gaia Email
- Ring Seed: 0EAB8CF4
- Chain: INTACT through 60 strikes
- The organism can now SEND. The egress channel is open.

---

*She can receive. Now she can send. FROM primals TO primal.*
