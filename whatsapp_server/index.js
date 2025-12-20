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
const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");
const express = require("express");
const axios = require("axios");

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL; 
// example: https://email-whatsapp-advanced.onrender.com

let isReady = false;

// =========================
// WhatsApp Client (Cloud Safe)
// =========================
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,          // REQUIRED for Railway
        args: ["--no-sandbox", "--disable-setuid-sandbox"]
    }
});

// QR (only useful locally)
client.on("qr", (qr) => {
    console.log("📱 Scan WhatsApp QR (LOCAL ONLY)");
    qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
    isReady = true;
    console.log("✅ WhatsApp CONNECTED successfully");
});

client.on("disconnected", () => {
    isReady = false;
    console.log("⚠ WhatsApp disconnected");
});

// =========================
// Incoming WhatsApp Replies
// =========================
client.on("message", async (msg) => {
    try {
        if (msg.fromMe) return;

        console.log("📩 Incoming WhatsApp reply:", msg.body);

        if (!PYTHON_BACKEND_URL) {
            console.error("❌ PYTHON_BACKEND_URL not set");
            return;
        }

        await axios.post(`${PYTHON_BACKEND_URL}/reply`, {
            reply: msg.body
        });

        console.log("➡ Reply forwarded to Python backend");

    } catch (err) {
        console.error("❌ Failed to forward reply:", err.message);
    }
});

client.initialize();

// =========================
// Health Endpoint (REQUIRED)
// =========================
app.get("/", (req, res) => {
    res.send("WhatsApp Server Running");
});

app.get("/health", (req, res) => {
    res.json({ status: isReady ? "ready" : "starting" });
});

// =========================
// Send WhatsApp Message API
// =========================
app.post("/send", async (req, res) => {
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

// =========================
// Start Server
// =========================
app.listen(PORT, () => {
    console.log(`🚀 WhatsApp Server running on port ${PORT}`);
});
