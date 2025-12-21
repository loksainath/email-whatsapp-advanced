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
/**
 * WhatsApp Server
 * ----------------
 * - Sends WhatsApp messages from Python backend
 * - Forwards WhatsApp replies back to Python backend
 * - Supports LOCAL + CLOUD (Render) Python backend
 */

require("dotenv").config();

const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");
const express = require("express");
const axios = require("axios");

const app = express();
app.use(express.json());

/**
 * =========================
 * CONFIGURATION
 * =========================
 */
const PORT = process.env.WA_PORT || 3000;

// 👇 THIS IS THE MOST IMPORTANT LINE
const PYTHON_BACKEND_URL =
  process.env.PYTHON_BACKEND_URL || "http://127.0.0.1:5000";

console.log("🔗 Python Backend URL:", PYTHON_BACKEND_URL);

let isReady = false;

/**
 * =========================
 * WHATSAPP CLIENT
 * =========================
 */
const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: {
    headless: false,
    executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
     // MUST be false for QR
  },
});

/**
 * =========================
 * WHATSAPP EVENTS
 * =========================
 */
client.on("qr", (qr) => {
  console.log("📱 Scan WhatsApp QR");
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

/**
 * =========================
 * INCOMING WHATSAPP MESSAGES
 * =========================
 */
client.on("message", async (msg) => {
  try {
    // Ignore messages sent by bot itself
    if (msg.fromMe) return;

    console.log("📩 Incoming WhatsApp reply:", msg.body);

    // Forward reply to Python backend
    await axios.post(`${PYTHON_BACKEND_URL}/reply`, {
      reply: msg.body,
      from: msg.from,
    });

    console.log("➡ Reply forwarded to Python backend");

  } catch (err) {
    console.error("❌ Failed to forward reply:", err.message);
  }
});

/**
 * =========================
 * START WHATSAPP CLIENT
 * =========================
 */
client.initialize();

/**
 * =========================
 * EXPRESS APIs
 * =========================
 */

// Health check
app.get("/health", (req, res) => {
  res.json({
    status: isReady ? "ready" : "starting",
    python_backend: PYTHON_BACKEND_URL,
  });
});

// Send WhatsApp message
app.post("/send", async (req, res) => {
  const { number, message } = req.body;

  if (!isReady) {
    return res.status(503).json({ error: "WhatsApp not ready" });
  }

  if (!number || !message) {
    return res.status(400).json({ error: "number and message required" });
  }

  try {
    await client.sendMessage(`${number}@c.us`, message);
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/**
 * =========================
 * START SERVER
 * =========================
 */
app.listen(PORT, () => {
  console.log(`🚀 WhatsApp Server running on port ${PORT}`);
});
