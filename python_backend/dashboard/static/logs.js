function loadLogs() {
  fetch("/api/logs")
    .then(res => res.json())
    .then(logs => {
      const tbody = document.querySelector("#emailTable tbody");
      tbody.innerHTML = "";

      logs.reverse().forEach(log => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${log.from || "-"}</td>
          <td>${log.subject || "-"}</td>
          <td>${log.priority || "-"}</td>
          <td>${log.status || "-"}</td>
          <td>${log.time || "-"}</td>
        `;
        tbody.appendChild(row);
      });
    });
}

loadLogs();
setInterval(loadLogs, 10000);
