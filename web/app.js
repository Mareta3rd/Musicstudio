
const $ = (id) => document.getElementById(id);

const promptBox = $("prompt");
const lyricsBox = $("lyrics");
const durationBox = $("duration");
const bpmBox = $("bpm");
const keyBox = $("key");
const languageBox = $("language");
const generateBtn = $("generate");
const errorBox = $("error");
const emptyState = $("emptyState");
const trackState = $("trackState");
const resultTitle = $("resultTitle");
const resultStatus = $("resultStatus");
const trackTitle = $("trackTitle");
const trackMeta = $("trackMeta");
const audio = $("audio");
const labNote = $("labNote");
const historyList = $("historyList");

let history = [];

const guideStart = $("guideStart");
const guideBody = $("guideBody");
const guideQuestion = $("guideQuestion");
const guidePurpose = $("guidePurpose");
const guideAnswer = $("guideAnswer");
const guideNext = $("guideNext");
const guideBrief = $("guideBrief");

let guideSessionId = null;
let guideQuestionId = null;

async function startGuide() {
  const res = await fetch("/api/guide/start", {method: "POST"});
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Guide could not start");
  guideSessionId = data.session_id;
  guideQuestionId = data.question_id;
  guideQuestion.textContent = data.question || "Ready.";
  guidePurpose.textContent = data.purpose ? "Focus: " + data.purpose : "";
  guideBody.hidden = false;
  guideAnswer.value = "";
  guideBrief.hidden = true;
  guideNext.textContent = "Continue ↗";
  guideAnswer.focus();
}

async function answerGuide() {
  if (!guideSessionId || !guideQuestionId) return;
  const answer = guideAnswer.value.trim();
  if (!answer) return;
  guideNext.disabled = true;
  try {
    const res = await fetch("/api/guide/answer", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        session_id: guideSessionId,
        question_id: guideQuestionId,
        answer
      })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Guide answer failed");
    guideAnswer.value = "";
    if (data.complete) {
      guideQuestion.textContent = "The creative brief is ready.";
      guidePurpose.textContent = "Pass it to the Producer or edit it in the main brief.";
      guideBrief.textContent = data.brief || "";
      guideBrief.hidden = false;
      guideNext.disabled = true;
      return;
    }
    guideQuestionId = data.question_id;
    guideQuestion.textContent = data.question || "";
    guidePurpose.textContent = data.purpose ? "Focus: " + data.purpose : "";
    guideAnswer.focus();
  } catch (err) {
    showError(err.message || "Guide error");
  } finally {
    if (!guideNext.disabled || !guideBrief.hidden) guideNext.disabled = false;
  }
}

guideStart.addEventListener("click", () => {
  startGuide().catch((err) => showError(err.message));
});
guideNext.addEventListener("click", () => {
  answerGuide().catch((err) => showError(err.message));
});
guideAnswer.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    answerGuide();
  }
});


async function loadProvider() {
  try {
    const res = await fetch("/api/providers");
    const providers = await res.json();
    const p = providers[0];
    if (p) $("providerLabel").textContent = p.label;
  } catch (_) {}
}

document.querySelectorAll(".chip").forEach((button) => {
  button.addEventListener("click", () => {
    const value = button.dataset.add;
    const current = promptBox.value.trim();
    promptBox.value = current ? current + ", " + value : value;
    promptBox.focus();
  });
});

function resetError() {
  errorBox.hidden = true;
  errorBox.textContent = "";
}

function showError(message) {
  errorBox.hidden = false;
  errorBox.textContent = message;
}

function makeWave() {
  const wave = $("wave");
  wave.innerHTML = "";
  for (let i = 0; i < 130; i++) {
    const bar = document.createElement("span");
    bar.className = "bar";
    const center = Math.abs(i - 65) / 65;
    const height = 20 + (1 - center) * 120 * (0.35 + Math.random() * 0.65);
    bar.style.height = height + "px";
    bar.style.animationDelay = Math.random() * 1.6 + "s";
    wave.appendChild(bar);
  }
}

function renderHistory() {
  if (!history.length) {
    historyList.innerHTML = '<div class="history-empty">Versions will collect here.</div>';
    return;
  }
  historyList.innerHTML = history.map((job, index) => {
    return '<div class="history-item">' +
      '<div class="history-title">v' + (history.length - index) + ' · ' +
      escapeHtml(job.title) + '</div>' +
      '<div class="history-meta">' + job.status.toUpperCase() + ' · ' + job.provider + '</div>' +
      '</div>';
  }).join("");
}

function escapeHtml(text) {
  return String(text).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}

function pushHistory(job) {
  if (history.some((item) => item.id === job.id)) return;
  history.unshift(job);
  renderHistory();
}

function renderJob(job) {
  resultStatus.textContent = job.status.toUpperCase();

  if (job.status === "queued" || job.status === "running") {
    emptyState.hidden = true;
    trackState.hidden = false;
    resultTitle.textContent = "Generating…";
    trackTitle.textContent = job.title || "Building your track";
    trackMeta.textContent = "The provider is working on this version.";
    labNote.hidden = true;
    audio.hidden = true;
    makeWave();
    return;
  }

  if (job.status === "failed") {
    emptyState.hidden = true;
    trackState.hidden = false;
    resultTitle.textContent = "Generation stopped";
    trackTitle.textContent = "Something needs attention";
    trackMeta.textContent = job.error || "Unknown error";
    labNote.hidden = true;
    return;
  }

  emptyState.hidden = true;
  trackState.hidden = false;
  resultTitle.textContent = "Your track";
  trackTitle.textContent = job.title || "Untitled generation";

  const meta = job.metadata || {};
  const bits = [];
  if (meta.duration) bits.push(meta.duration + "s");
  if (meta.bpm) bits.push(meta.bpm + " BPM");
  if (meta.key_scale) bits.push(meta.key_scale);
  trackMeta.textContent = bits.join(" · ") || "Generation complete";

  labNote.hidden = !!job.audio_url;

  if (job.audio_url) {
    audio.src = job.audio_url;
    audio.hidden = false;
  } else {
    audio.removeAttribute("src");
    audio.hidden = true;
  }

  makeWave();
  pushHistory(job);
}

async function poll(jobId) {
  const res = await fetch("/api/jobs/" + jobId);
  if (!res.ok) throw new Error(await res.text());
  const job = await res.json();
  renderJob(job);

  if (job.status === "queued" || job.status === "running") {
    setTimeout(() => poll(jobId).catch((err) => showError(err.message)), 1300);
  } else {
    generateBtn.disabled = false;
    generateBtn.querySelector("span").textContent = "Generate";
  }
}

generateBtn.addEventListener("click", async () => {
  resetError();
  const prompt = promptBox.value.trim();
  if (!prompt) {
    showError("Describe the music first.");
    promptBox.focus();
    return;
  }

  const payload = {
    prompt: prompt,
    lyrics: lyricsBox.value,
    duration: Number(durationBox.value),
    bpm: bpmBox.value ? Number(bpmBox.value) : null,
    key_scale: keyBox.value.trim(),
    vocal_language: languageBox.value,
    batch_size: 1,
    seed: null
  };

  generateBtn.disabled = true;
  generateBtn.querySelector("span").textContent = "Working…";
  resultStatus.textContent = "QUEUED";

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Generation failed");
    await poll(data.id);
  } catch (err) {
    generateBtn.disabled = false;
    generateBtn.querySelector("span").textContent = "Generate";
    showError(err.message || "Unexpected error");
  }
});

$("newVersion").addEventListener("click", () => promptBox.focus());

loadProvider();
