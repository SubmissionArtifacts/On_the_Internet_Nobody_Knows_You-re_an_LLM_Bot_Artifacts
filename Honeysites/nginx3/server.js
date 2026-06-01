import express from 'express';
import fetch from 'node-fetch';
import dotenv from 'dotenv';
dotenv.config();

const app = express();
app.use(express.json());
const PORT = 3000; 

app.post('/verify', async (req, res) => {
  const token = req.body.token;
  if (!token) return res.status(400).json({ success: false, message: 'Missing token' });

  const secret = process.env.RECAPTCHA_SECRET;
  const verificationUrl = `https://www.google.com/recaptcha/api/siteverify`;
  const backendUrl = "https://api.example.org";
  const domainKey = "site3";
  
  try {
    const response = await fetch(verificationUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ secret: secret, response: token })
    });

    const data = await response.json();

    // save to DB 
    
    await  fetch(`${backendUrl}/challenges`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        siteKey: domainKey,
        challenge: data,
        headers: req.headers
      }),
    })
    
   
    if (data.success && data.score >= 0.5) { // Adjust score threshold as needed
      res.json({ success: true });
    } else {
      res.status(403).json({ success: false, score: data.score });
    }
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

app.listen(PORT, () => console.log(`CAPTCHA backend running on port ${PORT}`));
