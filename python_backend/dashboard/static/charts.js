function loadAnalytics() {
  fetch("/api/analytics")
    .then(res => res.json())
    .then(data => {

      document.getElementById("emails").innerHTML =
        `<h3>📧 Emails</h3><p>${data.total_emails}</p>`;

      document.getElementById("whatsapp").innerHTML =
        `<h3>📲 Queued</h3><p>${data.queued_messages}</p>`;

      document.getElementById("replies").innerHTML =
        `<h3>↩ Replies</h3><p>${data.replies}</p>`;

      document.getElementById("spam").innerHTML =
        `<h3>🚫 Low Priority</h3><p>${data.priority.LOW}</p>`;

      if (window.emailChartInstance) {
        window.emailChartInstance.destroy();
      }

      const ctx = document.getElementById("emailChart").getContext("2d");

      window.emailChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
          labels: ["HIGH", "MEDIUM", "LOW"],
          datasets: [{
            label: "Email Priority",
            data: [
              data.priority.HIGH,
              data.priority.MEDIUM,
              data.priority.LOW
            ]
          }]
        }
      });
    });
}

loadAnalytics();
setInterval(loadAnalytics, 10000);
