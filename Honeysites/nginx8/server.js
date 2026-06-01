import express from 'express';
import fetch from 'node-fetch';
import dotenv from 'dotenv';
dotenv.config();

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
const PORT = 3003;

app.post('/verify-prosopo', async (req, res) => {
  const token = req.body.output
  const backendUrl = "https://api.example.org";
  const domainKey = "site8";
  if (!token) return res.status(400).json({ success: false, message: 'Missing token' });
  try {
    const result = await fetch('https://api.prosopo.io/siteverify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        secret: process.env.PROSOPO_SECRET,
        token,
      })
    });
    const responseyJson = await result.json();

    // save to DB 
    await fetch(`${backendUrl}/challenges`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        siteKey: domainKey,
        challenge: responseyJson,
        headers: req.headers
      }),
    })

    if (result.status == 200) {
      res.status(200).json({ verified: responseyJson.verified });
    } else {
      res.status(result.status).json(responseyJson)
    }

  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

app.listen(PORT, () => console.log(`Prosopo backend running on port ${PORT}`));