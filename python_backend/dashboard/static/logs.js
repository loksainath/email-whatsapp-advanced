// function loadLogs() {
//   fetch("/api/logs")
//     .then(res => res.json())
//     .then(logs => {
//       const tbody = document.querySelector("#emailTable tbody");
//       tbody.innerHTML = "";

//       logs.reverse().forEach(log => {
//         const row = document.createElement("tr");
//         row.innerHTML = `
//           <td>${log.from || "-"}</td>
//           <td>${log.subject || "-"}</td>
//           <td>${log.priority || "-"}</td>
//           <td>${log.status || "-"}</td>
//           <td>${log.time || "-"}</td>
//         `;
//         tbody.appendChild(row);
//       });
//     });
// }

// loadLogs();
// setInterval(loadLogs, 10000);

let lastCount = -1;
let audioUnlocked = false;

const popup = document.getElementById("popup");
const audio = document.getElementById("alertSound");

document.body.addEventListener("click", () => {
    audioUnlocked = true;
});

function showPopup() {
    popup.style.display = "block";
    setTimeout(() => popup.style.display = "none", 4000);
}

function playSound() {
    if (audioUnlocked) {
        audio.play().catch(() => {});
    }
}

async function loadLogs() {
    if (typeof renderStatsChart === "function") {
    renderStatsChart(data);
}

    try {
        const res = await fetch("/api/logs");
        const data = await res.json();

        document.getElementById("received").textContent = data.emails;
        document.getElementById("sent").textContent = data.whatsapp;
        document.getElementById("replied").textContent = data.replies;

        const tbody = document.getElementById("logs");
        tbody.innerHTML = "";

        data.logs.forEach(e => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${e.from}</td>
                <td>${e.subject}</td>
                <td>${e.status}</td>
                <td>${e.time || ""}</td>
            `;
            tbody.appendChild(tr);
        });

        if (data.logs.length > lastCount) {
            showPopup();
            playSound();
            lastCount = data.logs.length;
        }

    } catch (err) {
        console.error("Dashboard error", err);
    }
}

setInterval(loadLogs, 3000);
loadLogs();
