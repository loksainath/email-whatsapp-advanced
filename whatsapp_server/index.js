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


// require("dotenv").config();

// const { Client, LocalAuth, MessageMedia } = require("whatsapp-web.js");
// const express = require("express");
// const qrcode = require("qrcode-terminal");
// const axios = require("axios");
// const multer = require("multer");
// const fs = require("fs");

// const app = express();
// app.use(express.json());

// const PORT = 3000;
// let isReady = false;

// /* ============================
//    WhatsApp Client
// ============================ */
// const client = new Client({
//   authStrategy: new LocalAuth({
//     dataPath: "./.wwebjs_auth"
//   }),
//   puppeteer: {
//     headless: false,
//     args: ["--no-sandbox", "--disable-setuid-sandbox"]
//   }
// });

// /* ============================
//    File Upload
// ============================ */
// const upload = multer({ dest: "uploads/" });

// /* ============================
//    WhatsApp Events
// ============================ */
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
//   console.error("❌ Auth failure:", msg);
// });

// client.on("disconnected", reason => {
//   isReady = false;
//   console.log("⚠ WhatsApp disconnected:", reason);
// });

// /* ============================
//    API ENDPOINTS
// ============================ */
// app.get("/ready", (req, res) => {
//   return isReady
//     ? res.status(200).json({ ready: true })
//     : res.status(503).json({ ready: false });
// });

// /* -------- Send Text -------- */
// app.post("/send", async (req, res) => {
//   if (!isReady) return res.status(503).json({ error: "Not ready" });

//   const { number, message } = req.body;
//   if (!number || !message)
//     return res.status(400).json({ error: "Invalid payload" });

//   const chatId = number.includes("@c.us")
//     ? number
//     : `${number}@c.us`;

//   try {
//     await client.sendMessage(chatId, message);
//     console.log("📤 Text sent:", chatId);
//     res.json({ success: true });
//   } catch (err) {
//     console.error("❌ Text send error:", err.message);
//     res.status(500).json({ error: "Send failed" });
//   }
// });

// /* -------- Send Attachment -------- */
// app.post("/send-file", upload.single("file"), async (req, res) => {
//   if (!isReady) return res.status(503).json({ error: "Not ready" });

//   const { number } = req.body;
//   if (!number || !req.file)
//     return res.status(400).json({ error: "Invalid payload" });

//   const chatId = number.includes("@c.us")
//     ? number
//     : `${number}@c.us`;

//   try {
//     const media = MessageMedia.fromFilePath(req.file.path);
//     await client.sendMessage(chatId, media);
//     console.log("📎 Attachment sent");
//     res.json({ success: true });
//   } catch (err) {
//     console.error("❌ Attachment error:", err.message);
//     res.status(500).json({ error: "Attachment failed" });
//   } finally {
//     fs.unlink(req.file.path, () => {});
//   }
// });

// /* ============================
//    🔥 2-WAY COMMUNICATION (FIXED)
// ============================ */
// client.on("message", async (msg) => {
//   try {
//     /* ✅ IGNORE BOT MESSAGES ONLY */
//     if (msg.fromMe === true) return;

//     const text = (msg.body || "").trim();
//     if (!text) return;

//     console.log("📩 WhatsApp Incoming:", text);

//     /* Expected format:
//        reply_id | message
//     */
//     if (!text.includes("|")) return;

//     const [reply_id, ...rest] = text.split("|");
//     const message = rest.join("|").trim();

//     if (!reply_id || !message) return;

//     console.log("🔁 Forwarding reply:", reply_id);

//     await axios.post(
//       "http://127.0.0.1:5000/reply",
//       { reply_id: reply_id.trim(), message },
//       { timeout: 5000 }
//     );

//     console.log("📧 Reply forwarded to Gmail");
//   } catch (err) {
//     console.error("❌ Reply handling failed:", err.message);
//   }
// });

// /* ============================
//    START SERVER
// ============================ */
// app.listen(PORT, () => {
//   console.log(`🚀 WhatsApp Server running on port ${PORT}`);
// });

// client.initialize();


// require("dotenv").config();

// const { Client, LocalAuth, MessageMedia } = require("whatsapp-web.js");
// const express = require("express");
// const qrcode = require("qrcode-terminal");
// const axios = require("axios");
// const fs = require("fs");
// const path = require("path");

// const app = express();
// app.use(express.json());

// const PORT = 3000;
// let isReady = false;

// // ===============================
// // WhatsApp Client
// // ===============================
// const client = new Client({
//   authStrategy: new LocalAuth({
//     clientId: "email_whatsapp_bot_v1",
//     dataPath: "./.wwebjs_auth",
//   }),
//   puppeteer: {
//     headless: false,
//     args: [
//       "--no-sandbox",
//       "--disable-setuid-sandbox",
//       "--disable-dev-shm-usage",
//       "--disable-gpu",
//       "--disable-extensions",
//       "--disable-features=site-per-process"
//     ]
//   }
// });

// // ===============================
// // WhatsApp Events
// // ===============================
// client.on("qr", qr => {
//   console.log("📱 Scan WhatsApp QR:");
//   qrcode.generate(qr, { small: true });
// });

// client.on("ready", () => {
//   isReady = true;
//   console.log("✅ WhatsApp READY");
// });

// client.on("disconnected", reason => {
//   isReady = false;
//   console.log("⚠ WhatsApp disconnected:", reason);
//   // ❌ DO NOT call logout()
//   // ❌ DO NOT delete auth files
// });

// // ===============================
// // Incoming WhatsApp → Python
// // ===============================
// client.on("message", async msg => {
//   try {
//     if (msg.fromMe) return;

//     const body = (msg.body || "").trim();

//     // -------------------------------
//     // TEXT REPLY
//     // -------------------------------
//     if (body.includes("|")) {
//       const [reply_id, ...rest] = body.split("|");
//       const message = rest.join("|").trim();

//       await axios.post("http://127.0.0.1:5000/reply", {
//         reply_id: reply_id.trim(),
//         message
//       });

//       console.log("📩 Reply forwarded:", reply_id);
//     }

//     // -------------------------------
//     // ATTACHMENT REPLY
//     // -------------------------------
//     if (msg.hasMedia) {
//       const media = await msg.downloadMedia();

//       const fileName =
//         Date.now() + "_" + (media.filename || "attachment");

//       const savePath = path.join(
//         __dirname,
//         "incoming_files",
//         fileName
//       );

//       fs.mkdirSync(path.dirname(savePath), { recursive: true });

//       fs.writeFileSync(savePath, Buffer.from(media.data, "base64"));

//       await axios.post("http://127.0.0.1:5000/reply-attachment", {
//         reply_id: body.split("|")[0],
//         file_path: savePath
//       });

//       console.log("📎 Attachment forwarded:", savePath);
//     }

//   } catch (err) {
//     console.error("❌ Incoming message error:", err.message);
//   }
// });

// // ===============================
// // API
// // ===============================
// app.get("/ready", (req, res) => {
//   if (isReady) return res.sendStatus(200);
//   res.sendStatus(503);
// });

// app.post("/send", async (req, res) => {
//   if (!isReady) return res.status(503).json({ error: "Not ready" });

//   const { number, message } = req.body;
//   const chatId = number.includes("@c.us")
//     ? number
//     : `${number}@c.us`;

//   await client.sendMessage(chatId, message);
//   res.json({ success: true });
// });

// // ===============================
// app.listen(PORT, () => {
//   console.log(`🚀 WhatsApp Server running on ${PORT}`);
// });

// client.initialize();


// require("dotenv").config();

// const { Client, LocalAuth } = require("whatsapp-web.js");
// const express = require("express");
// const qrcode = require("qrcode-terminal");
// const axios = require("axios");
// const fs = require("fs");
// const path = require("path");

// const app = express();
// app.use(express.json());

// const PORT = 3000;
// let isReady = false;

// // ===============================
// // WhatsApp Client
// // ===============================
// const client = new Client({
//   authStrategy: new LocalAuth({
//     clientId: "email_whatsapp_bot_v1",
//     dataPath: "./.wwebjs_auth"
//   }),
//   puppeteer: {
//     headless: false,
//     args: [
//       "--no-sandbox",
//       "--disable-setuid-sandbox",
//       "--disable-dev-shm-usage",
//       "--disable-gpu"
//     ]
//   }
// });

// // ===============================
// // WhatsApp Events
// // ===============================
// client.on("qr", qr => {
//   console.log("📱 Scan WhatsApp QR:");
//   qrcode.generate(qr, { small: true });
// });

// client.on("ready", () => {
//   isReady = true;
//   console.log("✅ WhatsApp READY");
// });

// client.on("disconnected", reason => {
//   isReady = false;
//   console.log("⚠ WhatsApp disconnected:", reason);
// });

// // ===================================================
// // 🔥 INCOMING WHATSAPP → GMAIL (FIXED)
// // USE message_create (NOT message)
// // ===================================================
// client.on("message_create", async msg => {
//   try {
//     const body = (msg.body || "").trim();

//     console.log("\n📩 MESSAGE EVENT");
//     console.log("fromMe:", msg.fromMe);
//     console.log("body:", body);
//     console.log("hasMedia:", msg.hasMedia);

//     // Ignore bot echoes
//     if (msg.fromMe && !body.includes("|")) return;
//     if (!body.includes("|")) return;

//     // -------------------------------
//     // TEXT REPLY
//     // Format: reply_id | message
//     // -------------------------------
//     const [rawReplyId, ...rest] = body.split("|");
//     const replyId = rawReplyId.trim();
//     const messageText = rest.join("|").trim();

//     if (!replyId || !messageText) {
//       console.log("⚠ Invalid reply format");
//       return;
//     }

//     console.log("🔁 Forwarding TEXT reply →", replyId);

//     await axios.post("http://127.0.0.1:5000/reply", {
//       reply_id: replyId,
//       message: messageText
//     });

//     console.log("✅ TEXT reply sent to Gmail");

//     // -------------------------------
//     // ATTACHMENT (optional)
//     // -------------------------------
//     if (msg.hasMedia) {
//       const media = await msg.downloadMedia();
//       if (!media?.data) return;

//       const saveDir = path.join(__dirname, "incoming_files");
//       fs.mkdirSync(saveDir, { recursive: true });

//       const filePath = path.join(
//         saveDir,
//         Date.now() + "_" + (media.filename || "attachment")
//       );

//       fs.writeFileSync(filePath, Buffer.from(media.data, "base64"));

//       console.log("📎 Attachment saved:", filePath);

//       await axios.post("http://127.0.0.1:5000/reply-attachment", {
//         reply_id: replyId,
//         file_path: filePath
//       });

//       console.log("✅ Attachment forwarded to Gmail");
//     }

//   } catch (err) {
//     console.error("❌ WhatsApp processing error:", err.message);
//   }
// });

// // ===============================
// // API
// // ===============================
// app.get("/ready", (req, res) => {
//   if (isReady) return res.sendStatus(200);
//   res.sendStatus(503);
// });

// app.post("/send", async (req, res) => {
//   try {
//     if (!isReady) {
//       return res.status(503).json({ error: "WhatsApp not ready" });
//     }

//     const { number, message } = req.body;
//     const chatId = number.includes("@c.us")
//       ? number
//       : `${number}@c.us`;

//     await client.sendMessage(chatId, message);
//     res.json({ success: true });
//   } catch (err) {
//     res.status(500).json({ error: "Send failed" });
//   }
// });

// // ===============================
// app.listen(PORT, () => {
//   console.log(`🚀 WhatsApp Server running on ${PORT}`);
// });

// client.initialize();


// require("dotenv").config();

// const { Client, LocalAuth } = require("whatsapp-web.js");
// const express = require("express");
// const qrcode = require("qrcode-terminal");
// const axios = require("axios");
// const fs = require("fs");
// const path = require("path");

// const app = express();
// app.use(express.json());

// const PORT = 3000;
// let isReady = false;

// /**
//  * ✅ Extract UUID safely from ANY WhatsApp text
//  * Works with emojis, formatting, pasted blocks, etc.
//  */
// function extractReplyId(text) {
//   const match = text.match(/[0-9a-fA-F-]{36}/);
//   return match ? match[0] : null;
// }

// // ===============================
// // WhatsApp Client
// // ===============================
// const client = new Client({
//   authStrategy: new LocalAuth({
//     clientId: "email_whatsapp_bot_v1",
//     dataPath: "./.wwebjs_auth"
//   }),
//   puppeteer: {
//     headless: false,
//     args: [
//       "--no-sandbox",
//       "--disable-setuid-sandbox",
//       "--disable-dev-shm-usage",
//       "--disable-gpu"
//     ]
//   }
// });

// // ===============================
// // WhatsApp Events
// // ===============================
// client.on("qr", qr => {
//   console.log("📱 Scan WhatsApp QR:");
//   qrcode.generate(qr, { small: true });
// });

// client.on("ready", () => {
//   isReady = true;
//   console.log("✅ WhatsApp READY");
// });

// client.on("disconnected", reason => {
//   isReady = false;
//   console.log("⚠ WhatsApp disconnected:", reason);
// });

// // ===================================================
// // 🔥 INCOMING WHATSAPP → GMAIL (100% FIXED)
// // ===================================================
// client.on("message_create", async msg => {
//   try {
//     const body = (msg.body || "").trim();

//     console.log("\n📩 WhatsApp MESSAGE");
//     console.log("fromMe:", msg.fromMe);
//     console.log("body:", body);
//     console.log("hasMedia:", msg.hasMedia);

//     // Ignore bot echo messages
//     if (msg.fromMe && !body.includes("|")) return;
//     if (!body.includes("|")) return;

//     // ===============================
//     // 🔑 Extract reply_id SAFELY
//     // ===============================
//     const replyId = extractReplyId(body);
//     const messageText = body.split("|").slice(1).join("|").trim();

//     if (!replyId || !messageText) {
//       console.log("⚠ Invalid reply format");
//       return;
//     }

//     console.log("🔁 Forwarding TEXT reply →", replyId);

//     // ===============================
//     // TEXT → GMAIL
//     // ===============================
//     await axios.post("http://127.0.0.1:5000/reply", {
//       reply_id: replyId,
//       message: messageText
//     });

//     console.log("✅ TEXT reply sent to Gmail");

//     // ===============================
//     // ATTACHMENT (OPTIONAL)
//     // ===============================
//     if (msg.hasMedia) {
//       const media = await msg.downloadMedia();
//       if (!media || !media.data) return;

//       const saveDir = path.join(__dirname, "incoming_files");
//       fs.mkdirSync(saveDir, { recursive: true });

//       const filePath = path.join(
//         saveDir,
//         Date.now() + "_" + (media.filename || "attachment")
//       );

//       fs.writeFileSync(filePath, Buffer.from(media.data, "base64"));
//       console.log("📎 Attachment saved:", filePath);

//       await axios.post("http://127.0.0.1:5000/reply-attachment", {
//         reply_id: replyId,
//         file_path: filePath
//       });

//       console.log("✅ Attachment forwarded to Gmail");
//     }

//   } catch (err) {
//     console.error("❌ WhatsApp processing error:", err.message);
//   }
// });

// // ===============================
// // API
// // ===============================
// app.get("/ready", (req, res) => {
//   if (isReady) return res.sendStatus(200);
//   res.sendStatus(503);
// });

// app.post("/send", async (req, res) => {
//   try {
//     if (!isReady) {
//       return res.status(503).json({ error: "WhatsApp not ready" });
//     }

//     const { number, message } = req.body;
//     const chatId = number.includes("@c.us")
//       ? number
//       : `${number}@c.us`;

//     await client.sendMessage(chatId, message);
//     res.json({ success: true });
//   } catch (err) {
//     console.error("❌ Send error:", err.message);
//     res.status(500).json({ error: "Send failed" });
//   }
// });

// // ===============================
// app.listen(PORT, () => {
//   console.log(`🚀 WhatsApp Server running on ${PORT}`);
// });

// client.initialize();




require("dotenv").config();

const { Client, LocalAuth } = require("whatsapp-web.js");
const express = require("express");
const qrcode = require("qrcode-terminal");
const axios = require("axios");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(express.json());

const PORT = 3000;
let isReady = false;

// ===============================
// WhatsApp Client
// ===============================
const client = new Client({
  authStrategy: new LocalAuth({
    clientId: "email_whatsapp_bot_v1",
    dataPath: "./.wwebjs_auth"
  }),
  puppeteer: {
    headless: false,
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
      "--disable-gpu",
      "--disable-extensions"
    ]
  }
});

// ===============================
// WhatsApp Events
// ===============================
client.on("qr", qr => {
  console.log("📱 Scan WhatsApp QR:");
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  isReady = true;
  console.log("✅ WhatsApp READY");
});

client.on("disconnected", reason => {
  isReady = false;
  console.log("⚠ WhatsApp disconnected:", reason);
});

// =======================================================
// 🔥 INCOMING WHATSAPP → GMAIL (FINAL & FIXED)
// =======================================================
client.on("message_create", async msg => {
  try {
    const body = (msg.body || "").trim();

    console.log("\n📩 WhatsApp MESSAGE");
    console.log("fromMe:", msg.fromMe);
    console.log("body:", body);
    console.log("hasMedia:", msg.hasMedia);

    // ❌ Ignore bot notification messages
    if (msg.fromMe && body.startsWith("📧")) return;

    // ❌ Ignore random WhatsApp chats
    if (!body.includes("|")) return;

    // -------------------------------
    // TEXT REPLY
    // Format: reply_id | message
    // -------------------------------
    const [rawReplyId, ...rest] = body.split("|");
    const replyId = rawReplyId.trim();
    const messageText = rest.join("|").trim();

    if (!replyId || !messageText) {
      console.log("⚠ Invalid reply format");
      return;
    }

    console.log("🔁 Forwarding reply →", replyId);

    await axios.post("http://127.0.0.1:5000/reply", {
      reply_id: replyId,
      message: messageText
    });

    console.log("✅ Gmail reply triggered");

    // -------------------------------
    // ATTACHMENT (optional)
    // -------------------------------
    if (msg.hasMedia) {
      const media = await msg.downloadMedia();
      if (!media || !media.data) return;

      const saveDir = path.join(__dirname, "incoming_files");
      fs.mkdirSync(saveDir, { recursive: true });

      const filePath = path.join(
        saveDir,
        Date.now() + "_" + (media.filename || "attachment")
      );

      fs.writeFileSync(filePath, Buffer.from(media.data, "base64"));

      console.log("📎 Attachment saved:", filePath);

      await axios.post("http://127.0.0.1:5000/reply-attachment", {
        reply_id: replyId,
        file_path: filePath
      });

      console.log("✅ Attachment forwarded to Gmail");
    }

  } catch (err) {
    console.error("❌ WhatsApp processing error:", err.message);
  }
});

// ===============================
// API (Python → WhatsApp)
// ===============================
app.get("/ready", (req, res) => {
  if (isReady) return res.sendStatus(200);
  res.sendStatus(503);
});

app.post("/send", async (req, res) => {
  try {
    if (!isReady) {
      return res.status(503).json({ error: "WhatsApp not ready" });
    }

    const { number, message } = req.body;

    const chatId = number.includes("@c.us")
      ? number
      : `${number}@c.us`;

    await client.sendMessage(chatId, message);
    res.json({ success: true });

  } catch (err) {
    console.error("❌ Send error:", err.message);
    res.status(500).json({ error: "Send failed" });
  }
});

// ===============================
app.listen(PORT, () => {
  console.log(`🚀 WhatsApp Server running on ${PORT}`);
});

client.initialize();
