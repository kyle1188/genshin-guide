// Vercel serverless function: capture newsletter subscribers.
// Set SUBSCRIBE_SHEET_URL (a Google Apps Script webhook, or any endpoint)
// in Vercel project env to persist emails. Without it, the function still
// returns success and logs the address (degraded, no storage).

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'method_not_allowed' });

  let email;
  try {
    const body = req.body;
    if (typeof body === 'object' && body !== null) {
      email = body.email;
    } else {
      email = JSON.parse(body || '{}').email;
    }
  } catch (e) {
    try {
      email = new URLSearchParams(req.body || '').get('email');
    } catch (_) {
      email = undefined;
    }
  }

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(email))) {
    return res.status(400).json({ ok: false, error: 'invalid_email' });
  }
  email = String(email).toLowerCase().trim();

  const sheet = process.env.SUBSCRIBE_SHEET_URL;
  if (sheet) {
    try {
      await fetch(sheet, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, ts: new Date().toISOString() })
      });
    } catch (e) {
      console.error('subscribe forward failed:', e);
    }
  }

  console.log('new subscriber:', email);
  return res.status(200).json({ ok: true });
};
