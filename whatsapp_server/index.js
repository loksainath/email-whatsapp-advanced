// const { Client, LocalAuth } = require('whatsapp-web.js');
// const qrcode = require('qrcode-terminal');
// const express = require('express');

// const app = express();
// app.use(express.json());

// let isReady = false;

// const client = new Client({
//     authStrategy: new LocalAuth(),
//     puppeteer: {
//         headless: false,
//         executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
//     }
// });

// client.on('qr', (qr) => {
//     console.log('📱 Scan WhatsApp QR');
//     qrcode.generate(qr, { small: true });
// });

// client.on('ready', () => {
//     isReady = true;
//     console.log('✅ WhatsApp CONNECTED successfully');
// });

// client.on('disconnected', () => {
//     isReady = false;
// });

// client.initialize();

// app.get('/health', (req, res) => {
//     res.json({ status: isReady ? "ready" : "starting" });
// });

// app.post('/send', async (req, res) => {
//     const { number, message } = req.body;

//     if (!isReady) {
//         return res.status(503).json({ error: "WhatsApp not ready" });
//     }

//     try {
//         await client.sendMessage(`${number}@c.us`, message);
//         res.json({ success: true });
//     } catch (err) {
//         res.status(500).json({ error: err.message });
//     }
// });

// app.listen(3000, () => {
//     console.log('🚀 WhatsApp Server running on port 3000');
// });
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

let isReady = false;

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: false,
        executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    }
});

client.on('qr', (qr) => {
    console.log('📱 Scan WhatsApp QR');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    isReady = true;
    console.log('✅ WhatsApp CONNECTED successfully');
});

client.on('disconnected', () => {
    isReady = false;
    console.log('⚠ WhatsApp disconnected');
});

// 🔥 LISTEN FOR INCOMING WHATSAPP MESSAGES
client.on('message', async (msg) => {
    try {
        // Ignore messages sent by bot itself
        if (msg.fromMe) return;

        console.log("📩 Incoming WhatsApp reply:", msg.body);

        // ✅ FORCE IPv4 (THIS FIXES ECONNREFUSED ::1)
        await axios.post("http://127.0.0.1:5000/reply", {
            reply: msg.body
        });

        console.log("➡ Reply forwarded to email system");

    } catch (err) {
        console.error("❌ Failed to forward reply:", err.message);
    }
});

client.initialize();

// 🔍 Health API
app.get('/health', (req, res) => {
    res.json({ status: isReady ? "ready" : "starting" });
});

// 📤 Send WhatsApp message
app.post('/send', async (req, res) => {
    const { number, message } = req.body;

    if (!isReady) {
        return res.status(503).json({ error: "WhatsApp not ready" });
    }

    try {
        await client.sendMessage(`${number}@c.us`, message);
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.listen(3000, () => {
    console.log('🚀 WhatsApp Server running on port 3000');
});
