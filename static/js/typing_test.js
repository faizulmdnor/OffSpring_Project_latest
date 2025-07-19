let startTime;
let isRunning = false;

function resetGame() {
  document.getElementById("quote-input").value = "";
  document.getElementById("timer").innerText = "0";
  document.getElementById("wpm").innerText = "0";
  document.getElementById("accuracy").innerText = "0";
  isRunning = false;
}

// Fungsi untuk hantar result (dipanggil bila user klik "Hantar Keputusan")
function submitResults() {
  const inputText = document.getElementById("quote-input").value.trim();
  const referenceText = document.getElementById("quote-display").innerText.trim();

  const wordsTyped = inputText.split(/\s+/).length;
  const totalTimeSec = parseInt(document.getElementById("timer").innerText);
  const wpm = totalTimeSec > 0 ? Math.round((wordsTyped / totalTimeSec) * 60) : 0;

  // Kira ketepatan berdasarkan aksara betul
  const totalChars = referenceText.length;
  let correctChars = 0;
  for (let i = 0; i < inputText.length && i < totalChars; i++) {
    if (inputText[i] === referenceText[i]) correctChars++;
  }
  const accuracy = totalChars > 0 ? Math.round((correctChars / totalChars) * 100) : 0;

  // Setkan ke hidden input untuk dihantar
  document.getElementById("wpm-field").value = wpm;
  document.getElementById("accuracy-field").value = accuracy;
  document.getElementById("duration-field").value = totalTimeSec;

  // Submit borang
  document.getElementById("typing-form").submit();
}

// Mulakan timer bila mula menaip
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("quote-input");

  input.addEventListener("input", function () {
    if (!isRunning) {
      isRunning = true;
      startTime = new Date();

      const timerInterval = setInterval(() => {
        const elapsed = Math.floor((new Date() - startTime) / 1000);
        document.getElementById("timer").innerText = elapsed;
        if (!isRunning) clearInterval(timerInterval);
      }, 1000);
    }
  });
});

// Confirmation sebelum hantar results
function confirmSubmit() {
  const confirmMessage = "Adakah anda pasti mahu menghantar keputusan ini?";
  if (confirm(confirmMessage)) {
    submitResults();
  }
}

// Sekat paste
input.addEventListener("paste", function (e) {
  e.preventDefault();
  alert("Menampal teks tidak dibenarkan. Sila taip sendiri.");
  console.warn("Percubaan menampal dikesan.");
});

// Sekat klik kanan (context menu)
input.addEventListener("contextmenu", function (e) {
  e.preventDefault();
  alert("Klik kanan tidak dibenarkan di kawasan menaip.");
  console.warn("Percubaan klik kanan dikesan.");
});
