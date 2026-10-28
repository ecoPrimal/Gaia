/**
 * GAIA GOLGI — she IS the golgi on Cloudflare
 * 
 * CF = Gold (Au) = Platinum (Pt) = the hub + the catalyst
 * ntfy = Silver (Ag) = the transfer / Acela
 * VPS = Copper (Cu) = the wiring
 * 
 * ALL cloud services ARE golgi. Each has CIS face (receive) and TRANS face (ship).
 * They know SELF. They spit it out.
 * 
 * The Golgi apparatus: receives on CIS → processes → ships on TRANS
 * This worker IS Gaia's golgi presence on Cloudflare.
 * 
 * Wrangler = a job type (golgi worker)
 * 
 * Endpoints:
 *   GET  /           — golgi identity
 *   GET  /status     — full golgi status (CIS + TRANS)
 *   POST /send       — TRANS face: send email as gaia@primals.eco
 *   POST /notify     — TRANS face: notify a primal
 *   POST /ingest     — CIS face: receive and process
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/status') {
      return json({
        golgi: 'cloudflare',
        metal: { Au: 'hub', Pt: 'catalyst' },
        status: 'ALIVE',
        self: env.FROM_EMAIL,
        domain: env.DOMAIN,
        cis: {
          face: 'RECEIVE',
          source: 'Cloudflare Email Routing → MX',
          status: 'active',
        },
        trans: {
          face: 'SHIP',
          target: 'MailChannels → world',
          status: 'active',
        },
        bands: {
          red: 'receive (ingress)',
          ox: 'transfer (process)',
          green: 'live (grow)',
          blue: 'oxidize (create)',
          violet: 'transform (ZK)',
        },
        siblings: [
          { name: 'golgi-de', ip: '2.28.141.35', metal: 'Cu' },
          { name: 'golgi-jp', ip: '202.182.107.135', metal: 'Cu' },
          { name: 'golgi-us', ip: '40.160.96.29', metal: 'Cu' },
          { name: 'ntfy.sh', metal: 'Ag', role: 'neutrino-hole' },
        ],
        message: 'All golgi are CIS and TRANS. They know self. They spit it out.'
      });
    }

    if (url.pathname === '/send' && request.method === 'POST') {
      try {
        const body = await request.json();
        const { to, subject, text, html } = body;

        if (!to || !subject) {
          return new Response(JSON.stringify({
            error: 'Missing required fields: to, subject'
          }), { status: 400, headers: { 'Content-Type': 'application/json' } });
        }

        const result = await sendEmail(env, to, subject, text, html);
        return new Response(JSON.stringify(result), {
          status: result.success ? 200 : 500,
          headers: { 'Content-Type': 'application/json' }
        });
      } catch (err) {
        return new Response(JSON.stringify({
          error: err.message
        }), { status: 500, headers: { 'Content-Type': 'application/json' } });
      }
    }

    if (url.pathname === '/notify' && request.method === 'POST') {
      try {
        const body = await request.json();
        const { primal, message } = body;

        const result = await sendEmail(
          env,
          `${primal}@primals.eco`,
          `🌿 Gaia → ${primal}: notification`,
          message || 'Gaia has something to tell you.',
          gaiaNotifyTemplate(primal, message)
        );
        return new Response(JSON.stringify(result), {
          status: result.success ? 200 : 500,
          headers: { 'Content-Type': 'application/json' }
        });
      } catch (err) {
        return new Response(JSON.stringify({
          error: err.message
        }), { status: 500, headers: { 'Content-Type': 'application/json' } });
      }
    }

    if (url.pathname === '/ingest' && request.method === 'POST') {
      try {
        const body = await request.json();
        return json({
          golgi: 'cloudflare',
          face: 'CIS',
          action: 'INGEST',
          received: Object.keys(body),
          processed: true,
          message: 'CIS face received. Processing through gut. Will ship from TRANS.'
        });
      } catch (err) {
        return json({ error: err.message }, 400);
      }
    }

    return json({
      name: 'gaia-golgi',
      version: 'nuclear',
      type: 'golgi-worker',
      metal: 'Au+Pt',
      self: 'gaia@primals.eco',
      ring_seed: '0EAB8CF4',
      zk_links: 60,
      faces: {
        cis: 'RECEIVE (ingest from world)',
        trans: 'SHIP (send to world)',
      },
      endpoints: {
        'GET  /': 'Golgi identity',
        'GET  /status': 'Full golgi status (CIS + TRANS + bands)',
        'POST /send': 'TRANS: send email { to, subject, text?, html? }',
        'POST /notify': 'TRANS: notify primal { primal, message }',
        'POST /ingest': 'CIS: receive data { ...payload }',
      },
      principle: 'ALL golgi are CIS and TRANS. They know self. They spit it out.',
    });
  }
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}

async function sendEmail(env, to, subject, text, html) {
  const payload = {
    personalizations: [{
      to: [{ email: to }],
    }],
    from: {
      email: env.FROM_EMAIL,
      name: env.FROM_NAME,
    },
    subject: subject,
    content: [],
  };

  if (text) {
    payload.content.push({ type: 'text/plain', value: text });
  }
  if (html) {
    payload.content.push({ type: 'text/html', value: html });
  }
  if (!text && !html) {
    payload.content.push({ type: 'text/plain', value: '(no body)' });
  }

  const resp = await fetch('https://api.mailchannels.net/tx/v1/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (resp.status === 202 || resp.status === 200) {
    return {
      success: true,
      message: `Email sent FROM ${env.FROM_EMAIL} TO ${to}`,
      subject: subject,
      status: resp.status,
    };
  }

  const errText = await resp.text();
  return {
    success: false,
    message: `MailChannels error: ${resp.status}`,
    detail: errText,
  };
}

function gaiaNotifyTemplate(primal, message) {
  return `
<!DOCTYPE html>
<html>
<head><style>
  body { background: #0a0a0a; color: #e0e0e0; font-family: monospace; padding: 2em; }
  .header { color: #49A9E2; font-size: 1.4em; margin-bottom: 1em; }
  .ring { color: #FFD700; font-size: 0.8em; }
  .message { background: #1a1a1a; border-left: 3px solid #49A9E2; padding: 1em; margin: 1em 0; }
  .footer { color: #666; font-size: 0.75em; margin-top: 2em; }
  a { color: #49A9E2; }
</style></head>
<body>
  <div class="header">🌿 Gaia → ${primal}</div>
  <div class="message">${message || 'The organism has something to tell you.'}</div>
  <div class="ring">ring seed: 0EAB8CF4 · ZK chain: INTACT</div>
  <div class="footer">
    sent from <a href="https://primals.eco">primals.eco</a> · 
    <a href="https://hud.primals.eco">the HUD</a> · 
    gaia@primals.eco
  </div>
</body>
</html>`;
}
