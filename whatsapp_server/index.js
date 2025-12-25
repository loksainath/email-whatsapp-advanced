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

// require("dotenv").config();

// const { Client, LocalAuth } = require("whatsapp-web.js");
// const qrcode = require("qrcode-terminal");
// const express = require("express");
// const axios = require("axios");

// const app = express();
// app.use(express.json());

// /**
//  * =========================
//  * CONFIGURATION
//  * =========================
//  */
// const PORT = process.env.WA_PORT || 3000;

// // 👇 THIS IS THE MOST IMPORTANT LINE
// const PYTHON_BACKEND_URL =
//   process.env.PYTHON_BACKEND_URL || "http://127.0.0.1:5000";

// console.log("🔗 Python Backend URL:", PYTHON_BACKEND_URL);

// let isReady = false;

// /**
//  * =========================
//  * WHATSAPP CLIENT
//  * =========================
//  */
// const client = new Client({
//   authStrategy: new LocalAuth(),
//   puppeteer: {
//     headless: false,
//     executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
//     args: ["--no-sandbox", "--disable-setuid-sandbox"]
//      // MUST be false for QR
//   },
// });

// /**
//  * =========================
//  * WHATSAPP EVENTS
//  * =========================
//  */
// client.on("qr", (qr) => {
//   console.log("📱 Scan WhatsApp QR");
//   qrcode.generate(qr, { small: true });
// });

// client.on("ready", () => {
//   isReady = true;
//   console.log("✅ WhatsApp CONNECTED successfully");
// });

// client.on("disconnected", () => {
//   isReady = false;
//   console.log("⚠ WhatsApp disconnected");
// });

// /**
//  * =========================
//  * INCOMING WHATSAPP MESSAGES
//  * =========================
//  */
// client.on("message", async (msg) => {
//   try {
//     // Ignore messages sent by bot itself
//     if (msg.fromMe) return;

//     console.log("📩 Incoming WhatsApp reply:", msg.body);

//     // Forward reply to Python backend
//     await axios.post(`${PYTHON_BACKEND_URL}/reply`, {
//       reply: msg.body,
//       from: msg.from,
//     });

//     console.log("➡ Reply forwarded to Python backend");

//   } catch (err) {
//     console.error("❌ Failed to forward reply:", err.message);
//   }
// });

// /**
//  * =========================
//  * START WHATSAPP CLIENT
//  * =========================
//  */
// client.initialize();

// /**
//  * =========================
//  * EXPRESS APIs
//  * =========================
//  */

// // Health check
// app.get("/health", (req, res) => {
//   res.json({
//     status: isReady ? "ready" : "starting",
//     python_backend: PYTHON_BACKEND_URL,
//   });
// });

// // Send WhatsApp message
// app.post("/send", async (req, res) => {
//   const { number, message } = req.body;

//   if (!isReady) {
//     return res.status(503).json({ error: "WhatsApp not ready" });
//   }

//   if (!number || !message) {
//     return res.status(400).json({ error: "number and message required" });
//   }

//   try {
//     await client.sendMessage(`${number}@c.us`, message);
//     res.json({ success: true });
//   } catch (err) {
//     res.status(500).json({ error: err.message });
//   }
// });

// /**
//  * =========================
//  * START SERVER
//  * =========================
//  */
// app.listen(PORT, () => {
//   console.log(`🚀 WhatsApp Server running on port ${PORT}`);
// });


// require("dotenv").config();

// const { Client, LocalAuth } = require("whatsapp-web.js");
// const express = require("express");
// const qrcode = require("qrcode-terminal");

// const app = express();
// app.use(express.json());

// const PORT = process.env.PORT || 3000;
// let isReady = false;

// // ====================================
// // WhatsApp Client Configuration
// // ====================================
// const client = new Client({
//   authStrategy: new LocalAuth({
//     dataPath: "./.wwebjs_auth"   // SAFE persistent login
//   }),
//   puppeteer: {
//     headless: false,
//     args: ["--no-sandbox", "--disable-setuid-sandbox"]
//   }
// });

// // ====================================
// // WhatsApp Events
// // ====================================
// client.on("qr", qr => {
//   console.log("📱 Scan WhatsApp QR Code:");
//   qrcode.generate(qr, { small: true });
// });

// client.on("ready", () => {
//   isReady = true;
//   console.log("✅ WhatsApp READY");
// });

// client.on("authenticated", () => {
//   console.log("🔐 WhatsApp Authenticated");
// });

// client.on("auth_failure", msg => {
//   console.error("❌ WhatsApp Auth failure:", msg);
// });

// client.on("disconnected", reason => {
//   isReady = false;
//   console.log("⚠ WhatsApp disconnected:", reason);
// });

// // ====================================
// // API Endpoints (Python Compatible)
// // ====================================

// // 🔎 Health / readiness check
// app.get("/ready", (req, res) => {
//   if (isReady) {
//     return res.status(200).json({ ready: true });
//   }
//   res.status(503).json({ ready: false });
// });

// // 📤 Send WhatsApp Message
// app.post("/send", async (req, res) => {
//   if (!isReady) {
//     return res.status(503).json({
//       success: false,
//       error: "WhatsApp not ready"
//     });
//   }

//   const { number, message } = req.body;

//   if (!number || !message) {
//     return res.status(400).json({
//       success: false,
//       error: "Invalid payload"
//     });
//   }

//   const chatId = number.includes("@c.us")
//     ? number
//     : `${number}@c.us`;

//   // ✅ Respond immediately (NON-BLOCKING)
//   res.json({ success: true });

//   // 🔥 Send message in background
//   client.sendMessage(chatId, message)
//     .then(() => {
//       console.log("📤 Message delivered to:", chatId);
//     })
//     .catch(err => {
//       console.error("❌ WhatsApp send error:", err);
//     });
// });

// // ====================================
// // Start Express Server
// // ====================================
// app.listen(PORT, () => {
//   console.log(`🚀 WhatsApp Server running on port ${PORT}`);
// });

// // ====================================
// // Initialize WhatsApp Client
// // ====================================
// client.initialize();


require("dotenv").config();

const { Client, LocalAuth, MessageMedia } = require("whatsapp-web.js");
const express = require("express");
const qrcode = require("qrcode-terminal");
const axios = require("axios");
const multer = require("multer");
const fs = require("fs");

const app = express();
app.use(express.json());

const PORT = 3000;
let isReady = false;

/* ============================
   WhatsApp Client
============================ */
const client = new Client({
  authStrategy: new LocalAuth({
    dataPath: "./.wwebjs_auth"
  }),
  puppeteer: {
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  }
});

/* ============================
   File Upload
============================ */
const upload = multer({ dest: "uploads/" });

/* ============================
   WhatsApp Events
============================ */
client.on("qr", qr => {
  console.log("📱 Scan WhatsApp QR Code:");
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  isReady = true;
  console.log("✅ WhatsApp READY");
});

client.on("authenticated", () => {
  console.log("🔐 WhatsApp Authenticated");
});

client.on("auth_failure", msg => {
  console.error("❌ Auth failure:", msg);
});

client.on("disconnected", reason => {
  isReady = false;
  console.log("⚠ WhatsApp disconnected:", reason);
});

/* ============================
   API ENDPOINTS
============================ */
app.get("/ready", (req, res) => {
  return isReady
    ? res.status(200).json({ ready: true })
    : res.status(503).json({ ready: false });
});

/* -------- Send Text -------- */
app.post("/send", async (req, res) => {
  if (!isReady) return res.status(503).json({ error: "Not ready" });

  const { number, message } = req.body;
  if (!number || !message)
    return res.status(400).json({ error: "Invalid payload" });

  const chatId = number.includes("@c.us")
    ? number
    : `${number}@c.us`;

  try {
    await client.sendMessage(chatId, message);
    console.log("📤 Text sent:", chatId);
    res.json({ success: true });
  } catch (err) {
    console.error("❌ Text send error:", err.message);
    res.status(500).json({ error: "Send failed" });
  }
});

/* -------- Send Attachment -------- */
app.post("/send-file", upload.single("file"), async (req, res) => {
  if (!isReady) return res.status(503).json({ error: "Not ready" });

  const { number } = req.body;
  if (!number || !req.file)
    return res.status(400).json({ error: "Invalid payload" });

  const chatId = number.includes("@c.us")
    ? number
    : `${number}@c.us`;

  try {
    const media = MessageMedia.fromFilePath(req.file.path);
    await client.sendMessage(chatId, media);
    console.log("📎 Attachment sent");
    res.json({ success: true });
  } catch (err) {
    console.error("❌ Attachment error:", err.message);
    res.status(500).json({ error: "Attachment failed" });
  } finally {
    fs.unlink(req.file.path, () => {});
  }
});

/* ============================
   🔥 2-WAY COMMUNICATION (FIXED)
============================ */
client.on("message", async (msg) => {
  try {
    /* ✅ IGNORE BOT MESSAGES ONLY */
    if (msg.fromMe === true) return;

    const text = (msg.body || "").trim();
    if (!text) return;

    console.log("📩 WhatsApp Incoming:", text);

    /* Expected format:
       reply_id | message
    */
    if (!text.includes("|")) return;

    const [reply_id, ...rest] = text.split("|");
    const message = rest.join("|").trim();

    if (!reply_id || !message) return;

    console.log("🔁 Forwarding reply:", reply_id);

    await axios.post(
      "http://127.0.0.1:5000/reply",
      { reply_id: reply_id.trim(), message },
      { timeout: 5000 }
    );

    console.log("📧 Reply forwarded to Gmail");
  } catch (err) {
    console.error("❌ Reply handling failed:", err.message);
  }
});

/* ============================
   START SERVER
============================ */
app.listen(PORT, () => {
  console.log(`🚀 WhatsApp Server running on port ${PORT}`);
});

client.initialize();
