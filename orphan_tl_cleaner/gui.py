import json

import webview

from .api import Cleaner
from .i18n import TRANSLATIONS, LANGUAGES
from .settings import Settings

HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
  --bg: #f0f0f0;
  --surface: #ffffff;
  --text: #333333;
  --text-secondary: #555555;
  --border: #cccccc;
  --input-bg: #ffffff;
  --input-text: #333333;
  --button-bg: #4a90d9;
  --button-hover: #357abd;
  --button-text: #ffffff;
  --success: #27ae60;
  --error: #e74c3c;
  --textarea-bg: #ffffff;
  --textarea-text: #333333;
  --shadow: rgba(0,0,0,0.08);
  --header-bg: #4a90d9;
  --header-text: #ffffff;
}
body.dark {
  --bg: #1e1e1e;
  --surface: #2d2d2d;
  --text: #e0e0e0;
  --text-secondary: #aaaaaa;
  --border: #444444;
  --input-bg: #3c3c3c;
  --input-text: #e0e0e0;
  --button-bg: #5c5c5c;
  --button-hover: #6e6e6e;
  --button-text: #ffffff;
  --success: #2ecc71;
  --error: #e74c3c;
  --textarea-bg: #3c3c3c;
  --textarea-text: #e0e0e0;
  --shadow: rgba(0,0,0,0.2);
  --header-bg: #3d3d3d;
  --header-text: #e0e0e0;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  font-size: 14px;
  line-height: 1.5;
  min-height: 100vh;
}
.header {
  background: var(--header-bg);
  color: var(--header-text);
  padding: 14px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 4px var(--shadow);
}
.header h1 { font-size: 18px; font-weight: 600; }
.header select {
  background: rgba(255,255,255,0.15);
  color: var(--header-text);
  border: 1px solid rgba(255,255,255,0.3);
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}
.header select option { background: #555; color: #fff; }
.container { padding: 16px 20px; max-width: 700px; margin: 0 auto; }
.section { margin-bottom: 14px; }
.checkboxes { display: flex; gap: 18px; margin-bottom: 14px; flex-wrap: wrap; }
.checkboxes label {
  display: flex; align-items: center; gap: 6px;
  cursor: pointer; user-select: none;
}
.checkboxes input[type="checkbox"] {
  width: 16px; height: 16px; cursor: pointer; accent-color: var(--button-bg);
}
.field-label {
  font-size: 13px; color: var(--text-secondary);
  margin-bottom: 4px;
}
.btn-row { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.btn {
  background: var(--button-bg); color: var(--button-text);
  border: none; padding: 8px 18px; border-radius: 4px;
  font-size: 13px; cursor: pointer; white-space: nowrap;
  transition: background 0.15s;
}
.btn:hover { background: var(--button-hover); }
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-primary {
  background: var(--success); font-size: 15px; font-weight: 600;
  padding: 10px 28px;
}
.btn-primary:hover { background: #219a52; }
.path-display {
  font-size: 12px; color: var(--text-secondary);
  word-break: break-all; flex: 1; min-width: 0;
}
input[type="text"] {
  width: 100%; padding: 8px 10px;
  background: var(--input-bg); color: var(--input-text);
  border: 1px solid var(--border); border-radius: 4px;
  font-size: 13px; outline: none;
}
input[type="text"]:focus { border-color: var(--button-bg); }
textarea {
  width: 100%; min-height: 180px; padding: 10px;
  background: var(--textarea-bg); color: var(--textarea-text);
  border: 1px solid var(--border); border-radius: 4px;
  font-size: 12px; font-family: 'Consolas', 'Courier New', monospace;
  resize: vertical; outline: none;
}
.status-msg {
  font-size: 13px; padding: 8px 12px; border-radius: 4px;
  margin-bottom: 10px; display: none;
}
.status-msg.error { display: block; background: rgba(231,76,60,0.1); color: var(--error); border: 1px solid rgba(231,76,60,0.3); }
.status-msg.success { display: block; background: rgba(46,204,113,0.1); color: var(--success); border: 1px solid rgba(46,204,113,0.3); }
.separator { border: none; border-top: 1px solid var(--border); margin: 14px 0; }
</style>
</head>
<body>
<div class="header">
  <h1 id="app-title">Limpiador de TLs Hu\u00e9rfanas</h1>
  <select id="lang-select" onchange="changeLanguage(this.value)"></select>
</div>
<div class="container">
  <div class="checkboxes">
    <label><input type="checkbox" id="dark-mode" onchange="toggleDarkMode(this.checked)"> <span data-i18n="dark_mode">Modo oscuro</span></label>
    <label><input type="checkbox" id="comment-blocks"> <span data-i18n="comment_blocks">Comentar bloques en lugar de borrarlos</span></label>
  </div>

  <div class="section">
    <div class="field-label" data-i18n="dir_label">Seleccione el directorio con los archivos .rpy y .rpym</div>
    <div class="btn-row">
      <button class="btn" onclick="selectDirectory()" data-i18n="dir_button">Seleccionar Directorio</button>
      <span class="path-display" id="dir-path"></span>
    </div>
  </div>

  <div class="section">
    <div class="field-label" data-i18n="lint_label">Seleccione el archivo lint.txt</div>
    <div class="btn-row">
      <button class="btn" onclick="selectLintFile()" data-i18n="lint_button">Seleccionar lint.txt</button>
      <span class="path-display" id="lint-path"></span>
    </div>
  </div>

  <div class="section">
    <div class="field-label" data-i18n="lang_label">Ingrese el idioma a buscar (por ejemplo, 'english')</div>
    <input type="text" id="lang-input" data-i18n-placeholder="lang_placeholder" placeholder="ej: english">
  </div>

  <hr class="separator">

  <div class="section">
    <div id="status-msg" class="status-msg"></div>
    <button class="btn btn-primary" id="run-btn" onclick="runTool()" data-i18n="execute">Ejecutar</button>
  </div>

  <div class="section">
    <textarea id="result-area" readonly></textarea>
  </div>
</div>

<script>
const TRANS = __TRANSLATIONS__;
const LANGS = __LANGUAGES__;
const SETTINGS = __SETTINGS__;
let currentLocale = SETTINGS.locale || 'es_ES';
let selectedDir = null;
let selectedLint = null;

function t(key, params) {
  let val = (TRANS[currentLocale] && TRANS[currentLocale][key]) || (TRANS['es_ES'] && TRANS['es_ES'][key]) || key;
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      val = val.replace('{' + k + '}', v);
    }
  }
  return val;
}

function applyLanguage(locale, save) {
  currentLocale = locale;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
      el.placeholder = t(key);
    } else {
      el.textContent = t(key);
    }
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    el.placeholder = t(key);
  });
  document.getElementById('app-title').textContent = t('app_title');
  if (save !== false && window.__apiReady) {
    window.__apiReady.then(function(api) { api.save_setting('locale', locale); });
  }
}

function changeLanguage(locale) {
  applyLanguage(locale, true);
}

function populateLanguages() {
  const sel = document.getElementById('lang-select');
  sel.innerHTML = '';
  LANGS.forEach(function(item) {
    const opt = document.createElement('option');
    opt.value = item[1];
    opt.textContent = item[0];
    sel.appendChild(opt);
  });
}

async function callApi(method) {
  var args = Array.prototype.slice.call(arguments, 1);
  try {
    if (window.__apiReady) {
      var api = await window.__apiReady;
      return await api[method].apply(api, args);
    }
  } catch(e) {
    throw e;
  }
}

async function selectDirectory() {
  try {
    const path = await callApi('select_directory');
    if (path) {
      selectedDir = path;
      document.getElementById('dir-path').textContent = t('dir_selected', {path: path});
    }
  } catch(e) {
    document.getElementById('dir-path').textContent = 'Error: ' + e;
  }
}

async function selectLintFile() {
  try {
    const path = await callApi('select_lint_file');
    if (path) {
      selectedLint = path;
      document.getElementById('lint-path').textContent = t('lint_selected', {path: path});
    }
  } catch(e) {
    document.getElementById('lint-path').textContent = 'Error: ' + e;
  }
}

function showStatus(msg, type) {
  const el = document.getElementById('status-msg');
  el.textContent = msg;
  el.className = 'status-msg ' + type;
}

async function runTool() {
  if (!selectedDir || !selectedLint) {
    showStatus(t('error_select_first'), 'error');
    return;
  }
  const language = document.getElementById('lang-input').value.trim();
  if (!language) {
    showStatus(t('error_enter_language'), 'error');
    return;
  }
  const commentBlocks = document.getElementById('comment-blocks').checked;
  const runBtn = document.getElementById('run-btn');
  runBtn.disabled = true;
  runBtn.textContent = t('running');
  showStatus('', '');
  try {
    const result = await callApi('run_tool', selectedDir, selectedLint, language, commentBlocks);
    document.getElementById('result-area').value = result;
    showStatus('', '');
  } catch(e) {
    document.getElementById('result-area').value = 'Error: ' + e;
    showStatus(e.toString(), 'error');
  } finally {
    runBtn.disabled = false;
    runBtn.textContent = t('execute');
  }
}

function toggleDarkMode(enabled) {
  document.body.classList.toggle('dark', enabled);
  callApi('save_setting', 'theme', enabled ? 'dark' : 'light');
}

function init() {
  populateLanguages();
  document.getElementById('lang-select').value = currentLocale;
  applyLanguage(currentLocale, false);
  if (SETTINGS.theme === 'dark') {
    document.getElementById('dark-mode').checked = true;
    document.body.classList.add('dark');
  }
  if (SETTINGS.comment_blocks) {
    document.getElementById('comment-blocks').checked = true;
  }
}
init();

window.__apiReady = new Promise(function(resolve) {
  function check() {
    if (typeof pywebview !== 'undefined' && pywebview && pywebview.api) {
      resolve(pywebview.api);
    } else {
      setTimeout(check, 50);
    }
  }
  check();
});

(function() {
    let _native = window.native;
    Object.defineProperty(window, 'native', {
        get: function() { return _native; },
        set: function(val) { _native = val; },
        enumerable: false,
        configurable: true
    });
})();
</script>
</body>
</html>"""


class Api:
    def __init__(self):
        self.window = None
        self.settings = Settings()
        self.cleaner = Cleaner()

    def get_settings(self):
        return self.settings.load()

    def save_setting(self, key, value):
        self.settings.save(key, value)

    def select_directory(self):
        result = self.window.create_file_dialog(webview.FOLDER_DIALOG)
        if result:
            return result[0]
        return None

    def select_lint_file(self):
        result = self.window.create_file_dialog(
            webview.OPEN_DIALOG,
            file_types=('Text Files (*.txt)', 'All Files (*.*)')
        )
        if result:
            return result[0]
        return None

    def run_tool(self, directory, lint_file, language, comment_blocks):
        try:
            settings = self.settings.load()
            locale = settings.get('locale', 'es_ES')
            return self.cleaner.run_tool(directory, lint_file, language, comment_blocks, locale)
        except Exception as e:
            return f"Error: {str(e)}"


def build_html():
    trans_json = json.dumps(TRANSLATIONS, ensure_ascii=False)
    langs_json = json.dumps(LANGUAGES, ensure_ascii=False)
    settings = Settings().load()
    settings_json = json.dumps(settings, ensure_ascii=False)
    html = HTML.replace('__TRANSLATIONS__', trans_json)
    html = html.replace('__LANGUAGES__', langs_json)
    html = html.replace('__SETTINGS__', settings_json)
    return html
