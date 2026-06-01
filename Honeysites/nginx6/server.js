import express from 'express';
import fetch from 'node-fetch';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const PORT = 3002;

app.post('/verify-turnstile', async (req, res) => {
  const token = req.body['cf-turnstile-response'];
  const backendUrl = "https://api.example.org";
  const domainKey = "site6";
  if (!token) return res.status(400).json({ verified: false });

  try {
    const verify = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        secret: process.env.TURNSTILE_SECRET_SITE6,
        response: token,
        remoteip: req.headers['x-forwarded-for'] || req.ip
      })
    });
    const result = await verify.json();
    // save to DB 
    await fetch(`${backendUrl}/challenges`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        siteKey: domainKey,
        challenge: result,
        headers: req.headers
      }),
    })

    if (result.success) {
      return res.json({ verified: true });
    } else {
      return res.status(403).json({ verified: false, errors: result['error-codes'] });
    }
  } catch (err) {
    console.error('Turnstile verification error:', err);
    res.status(500).json({ verified: false, message: 'Server error' });
  }
});

app.listen(PORT, () => {
  console.log(`Turnstile backend running on port ${PORT}`);
});
