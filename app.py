const express = require('express');
const cors = require('cors');
const { OpenAI } = require('openai');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors()); // ✅ allows any frontend to access this backend
app.use(express.json());

// test route
app.get('/', (req, res) => {
  res.send('✅ GPTGRIDX backend is working!');
});

// chat route
app.post('/api/chat', async (req, res) => {
  try {
    const { message } = req.body;

    const openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });

    const response = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: message }],
    });

    const reply = response.choices[0].message.content.trim();
    res.json({ reply });
  } catch (err) {
    console.error('❌ OpenAI error:', err);
    res.status(500).json({ reply: 'Something went wrong.' });
  }
});

app.listen(port, () => {
  console.log(`✅ Server running on http://localhost:${port}`);
});
