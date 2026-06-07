import os
import re
import sys
import json
import webview

TRANSLATIONS = {
    "es_ES": {
        "app_title": "Limpiador de TLs Hu\u00e9rfanas",
        "dark_mode": "Modo oscuro",
        "comment_blocks": "Comentar bloques en lugar de borrarlos",
        "dir_label": "Seleccione el directorio con los archivos .rpy y .rpym",
        "dir_button": "Seleccionar Directorio",
        "dir_selected": "Directorio seleccionado: {path}",
        "lint_label": "Seleccione el archivo lint.txt",
        "lint_button": "Seleccionar lint.txt",
        "lint_selected": "lint.txt seleccionado: {path}",
        "lang_label": "Ingrese el idioma a buscar (por ejemplo, 'english')",
        "lang_placeholder": "ej: english",
        "execute": "Ejecutar",
        "running": "Procesando...",
        "error_select_first": "Seleccione el directorio y el archivo lint.txt primero.",
        "error_enter_language": "Por favor, ingrese un idioma.",
        "error_no_identifiers": "No se encontraron identificadores en lint.txt.",
        "processed_header": "Archivos procesados:\n{files}",
        "no_files_processed": "No se encontraron archivos para procesar.",
        "select_dir_dialog": "Seleccione Directorio",
        "select_lint_dialog": "Seleccione lint.txt",
    },
    "en_US": {
        "app_title": "Orphan TL Cleaner",
        "dark_mode": "Dark mode",
        "comment_blocks": "Comment out blocks instead of deleting them",
        "dir_label": "Please select the directory containing the .rpy and .rpym files",
        "dir_button": "Select Directory",
        "dir_selected": "Selected directory: {path}",
        "lint_label": "Please select the lint.txt file",
        "lint_button": "Select lint.txt",
        "lint_selected": "lint.txt selected: {path}",
        "lang_label": "Please enter the language to search for (e.g., 'english')",
        "lang_placeholder": "e.g.: english",
        "execute": "Execute",
        "running": "Processing...",
        "error_select_first": "Please select the directory and lint.txt file first.",
        "error_enter_language": "Please enter a language.",
        "error_no_identifiers": "No identifiers were found in lint.txt.",
        "processed_header": "Processed files:\n{files}",
        "no_files_processed": "No files were found to process.",
        "select_dir_dialog": "Select Directory",
        "select_lint_dialog": "Select lint.txt",
    },
    "fr_FR": {
        "app_title": "Nettoyeur de TL orphelines",
        "dark_mode": "Mode sombre",
        "comment_blocks": "Commenter les blocs au lieu de les supprimer",
        "dir_label": "Veuillez s\u00e9lectionner le r\u00e9pertoire contenant les fichiers .rpy et .rpym",
        "dir_button": "S\u00e9lectionner le R\u00e9pertoire",
        "dir_selected": "R\u00e9pertoire s\u00e9lectionn\u00e9 : {path}",
        "lint_label": "Veuillez s\u00e9lectionner le fichier lint.txt",
        "lint_button": "S\u00e9lectionner lint.txt",
        "lint_selected": "lint.txt s\u00e9lectionn\u00e9 : {path}",
        "lang_label": "Veuillez entrer la langue \u00e0 rechercher (par exemple, 'anglais')",
        "lang_placeholder": "ex.: anglais",
        "execute": "Ex\u00e9cuter",
        "running": "Traitement...",
        "error_select_first": "Veuillez d'abord s\u00e9lectionner le r\u00e9pertoire et le fichier lint.txt.",
        "error_enter_language": "Veuillez entrer une langue.",
        "error_no_identifiers": "Aucun identifiant trouv\u00e9 dans lint.txt.",
        "processed_header": "Fichiers trait\u00e9s :\n{files}",
        "no_files_processed": "Aucun fichier trouv\u00e9 \u00e0 traiter.",
        "select_dir_dialog": "S\u00e9lectionner le R\u00e9pertoire",
        "select_lint_dialog": "S\u00e9lectionner lint.txt",
    },
    "pt_BR": {
        "app_title": "Limpiador de TLs \u00f3rf\u00e3s",
        "dark_mode": "Modo escuro",
        "comment_blocks": "Comentar blocos em vez de exclu\u00ed-los",
        "dir_label": "Selecione o diret\u00f3rio com os arquivos .rpy e .rpym",
        "dir_button": "Selecionar Diret\u00f3rio",
        "dir_selected": "Diret\u00f3rio selecionado: {path}",
        "lint_label": "Selecione o arquivo lint.txt",
        "lint_button": "Selecionar lint.txt",
        "lint_selected": "lint.txt selecionado: {path}",
        "lang_label": "Digite o idioma a ser procurado (por exemplo, 'english')",
        "lang_placeholder": "ex.: english",
        "execute": "Executar",
        "running": "Processando...",
        "error_select_first": "Por favor, selecione primeiro o diret\u00f3rio e o arquivo lint.txt.",
        "error_enter_language": "Por favor, digite um idioma.",
        "error_no_identifiers": "N\u00e3o foram encontrados identificadores em lint.txt.",
        "processed_header": "Arquivos processados:\n{files}",
        "no_files_processed": "Nenhum arquivo encontrado para processar.",
        "select_dir_dialog": "Selecionar Diret\u00f3rio",
        "select_lint_dialog": "Selecionar lint.txt",
    },
    "ja_JP": {
        "app_title": "\u5b64\u7acb TL \u30af\u30ea\u30fc\u30ca\u30fc",
        "dark_mode": "\u30c0\u30fc\u30af\u30e2\u30fc\u30c9",
        "comment_blocks": "\u30d6\u30ed\u30c3\u30af\u3092\u524a\u9664\u3059\u308b\u4ee3\u308f\u308a\u306b\u30b3\u30e1\u30f3\u30c8\u30a2\u30a6\u30c8\u3059\u308b",
        "dir_label": ".rpy\u30d5\u30a1\u30a4\u30eb\u3068.rpym\u30d5\u30a1\u30a4\u30eb\u304c\u542b\u307e\u308c\u3066\u3044\u308b\u30c7\u30a3\u30ec\u30af\u30c8\u30ea\u3092\u9078\u629e\u3057\u3066\u304f\u3060\u3055\u3044",
        "dir_button": "\u30c7\u30a3\u30ec\u30af\u30c8\u30ea\u3092\u9078\u629e",
        "dir_selected": "\u9078\u629e\u3055\u308c\u305f\u30c7\u30a3\u30ec\u30af\u30c8\u30ea: {path}",
        "lint_label": "lint.txt\u30d5\u30a1\u30a4\u30eb\u3092\u9078\u629e\u3057\u3066\u304f\u3060\u3055\u3044",
        "lint_button": "lint.txt\u3092\u9078\u629e",
        "lint_selected": "\u9078\u629e\u3055\u308c\u305flin.txt: {path}",
        "lang_label": "\u691c\u7d22\u3059\u308b\u8a00\u8a9e\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\uff08\u4f8b\uff1a\u300cenglish\u300d\uff09",
        "lang_placeholder": "\u4f8b: english",
        "execute": "\u5b9f\u884c",
        "running": "\u51e6\u7406\u4e2d...",
        "error_select_first": "\u6700\u521d\u306b\u30c7\u30a3\u30ec\u30af\u30c8\u30ea\u3068lint.txt\u30d5\u30a1\u30a4\u30eb\u3092\u9078\u629e\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
        "error_enter_language": "\u8a00\u8a9e\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
        "error_no_identifiers": "lint.txt\u306b\u8b58\u5225\u5b50\u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093\u3067\u3057\u305f\u3002",
        "processed_header": "\u51e6\u7406\u3055\u308c\u305f\u30d5\u30a1\u30a4\u30eb:\n{files}",
        "no_files_processed": "\u51e6\u7406\u3059\u308b\u30d5\u30a1\u30a4\u30eb\u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093\u3067\u3057\u305f\u3002",
        "select_dir_dialog": "\u30c7\u30a3\u30ec\u30af\u30c8\u30ea\u3092\u9078\u629e",
        "select_lint_dialog": "lint.txt\u3092\u9078\u629e",
    },
    "ru_RU": {
        "app_title": "\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u0435\u043b\u044c \u0441\u0438\u0440\u043e\u0442\u0441\u043a\u0438\u0445 TL",
        "dark_mode": "\u0422\u0451\u043c\u043d\u044b\u0439 \u0440\u0435\u0436\u0438\u043c",
        "comment_blocks": "\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0431\u043b\u043e\u043a\u0438 \u0432\u043c\u0435\u0441\u0442\u043e \u0438\u0445 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f",
        "dir_label": "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043a\u0430\u0442\u0430\u043b\u043e\u0433 \u0441 \u0444\u0430\u0439\u043b\u0430\u043c\u0438 .rpy \u0438 .rpym",
        "dir_button": "\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u043a\u0430\u0442\u0430\u043b\u043e\u0433",
        "dir_selected": "\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u043a\u0430\u0442\u0430\u043b\u043e\u0433: {path}",
        "lint_label": "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0444\u0430\u0439\u043b lint.txt",
        "lint_button": "\u0412\u044b\u0431\u0440\u0430\u0442\u044c lint.txt",
        "lint_selected": "\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 lint.txt: {path}",
        "lang_label": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u044f\u0437\u044b\u043a \u0434\u043b\u044f \u043f\u043e\u0438\u0441\u043a\u0430 (\u043d\u0430\u043f\u0440\u0438\u043c\u0435\u0440, \u00aborphan\u00bb)",
        "lang_placeholder": "\u043d\u0430\u043f\u0440.: english",
        "execute": "\u0412\u044b\u043f\u043e\u043b\u043d\u0438\u0442\u044c",
        "running": "\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430...",
        "error_select_first": "\u0421\u043d\u0430\u0447\u0430\u043b\u0430 \u0432\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043a\u0430\u0442\u0430\u043b\u043e\u0433 \u0438 \u0444\u0430\u0439\u043b lint.txt.",
        "error_enter_language": "\u041f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430, \u0432\u0432\u0435\u0434\u0438\u0442\u0435 \u044f\u0437\u044b\u043a.",
        "error_no_identifiers": "\u0412 lint.txt \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u043e \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440\u043e\u0432.",
        "processed_header": "\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u0430\u043d\u043d\u044b\u0435 \u0444\u0430\u0439\u043b\u044b:\n{files}",
        "no_files_processed": "\u041d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u043e \u0444\u0430\u0439\u043b\u043e\u0432 \u0434\u043b\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438.",
        "select_dir_dialog": "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043a\u0430\u0442\u0430\u043b\u043e\u0433",
        "select_lint_dialog": "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 lint.txt",
    },
    "zh_TW": {
        "app_title": "\u5b64\u7acb TL \u6e05\u7406\u5de5\u5177",
        "dark_mode": "\u6697\u9ed1\u6a21\u5f0f",
        "comment_blocks": "\u8a3b\u89e3\u5340\u584a\u800c\u4e0d\u662f\u522a\u9664\u5b83\u5011",
        "dir_label": "\u8acb\u9078\u64c7\u5305\u542b .rpy \u548c .rpym \u6587\u4ef6\u7684\u76ee\u9304",
        "dir_button": "\u9078\u64c7\u76ee\u9304",
        "dir_selected": "\u9078\u5b9a\u7684\u76ee\u9304: {path}",
        "lint_label": "\u8acb\u9078\u64c7 lint.txt \u6587\u4ef6",
        "lint_button": "\u9078\u64c7 lint.txt",
        "lint_selected": "\u9078\u5b9a\u7684 lint.txt: {path}",
        "lang_label": "\u8acb\u8f38\u5165\u8981\u67e5\u627e\u7684\u8a9e\u8a00\uff08\u4f8b\u5982\uff0c\u2018english\u2019\uff09",
        "lang_placeholder": "\u4f8b: english",
        "execute": "\u57f7\u884c",
        "running": "\u8655\u7406\u4e2d...",
        "error_select_first": "\u8acb\u9996\u5148\u9078\u64c7\u76ee\u9304\u548c lint.txt \u6587\u4ef6\u3002",
        "error_enter_language": "\u8acb\u63d0\u4f9b\u4e00\u500b\u8a9e\u8a00\u3002",
        "error_no_identifiers": "\u5728 lint.txt \u4e2d\u672a\u627e\u5230\u6a19\u8b58\u7b26\u3002",
        "processed_header": "\u5df2\u8655\u7406\u7684\u6587\u4ef6\uff1a\n{files}",
        "no_files_processed": "\u627e\u4e0d\u5230\u8981\u8655\u7406\u7684\u6587\u4ef6\u3002",
        "select_dir_dialog": "\u9078\u64c7\u76ee\u9304",
        "select_lint_dialog": "\u9078\u64c7 lint.txt",
    },
}

LANGUAGES = [
    ("Espa\u00f1ol", "es_ES"),
    ("English", "en_US"),
    ("Fran\u00e7ais", "fr_FR"),
    ("Portugu\u00eas (Brasil)", "pt_BR"),
    ("\u65e5\u672c\u8a9e", "ja_JP"),
    ("\u0420\u0443\u0441\u0441\u043a\u0438\u0439", "ru_RU"),
    ("\u4e2d\u6587\uff08\u7e41\u9ad4\uff09", "zh_TW"),
]

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

// Prevenir que herramientas de inspección automática escaneen el objeto nativo de .NET
    (function() {
        let _native = window.native;
        Object.defineProperty(window, 'native', {
            get: function() { return _native; },
            set: function(val) { _native = val; },
            enumerable: false,   // <- Esto evita que bucles como for...in o Object.keys() lo vean
            configurable: true
        });
    })();
</script>
</body>
</html>"""


class Api:
    def __init__(self):
        self.window = None
        self.settings_path = self._get_settings_path()

    def _get_settings_path(self):
        if hasattr(sys, '_MEIPASS'):
            base = sys._MEIPASS
        else:
            base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, 'settings.json')

    def _load_settings(self):
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"locale": "es_ES", "theme": "light", "comment_blocks": False}

    def _save_settings(self, settings):
        with open(self.settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)

    def get_settings(self):
        return self._load_settings()

    def save_setting(self, key, value):
        settings = self._load_settings()
        settings[key] = value
        self._save_settings(settings)

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
            identifiers = self._load_identifiers(lint_file)
            if not identifiers:
                locale = self._load_settings().get('locale', 'es_ES')
                return TRANSLATIONS.get(locale, TRANSLATIONS['es_ES']).get('error_no_identifiers', 'No identifiers found.')

            files_processed = []
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.rpy') or file.endswith('.rpym'):
                        filepath = os.path.join(root, file)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()

                        updated_content = self._process_file(content, identifiers, language, comment_blocks)

                        if updated_content != content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(updated_content)
                            files_processed.append(filepath)

            locale = self._load_settings().get('locale', 'es_ES')
            t = TRANSLATIONS.get(locale, TRANSLATIONS['es_ES'])

            if files_processed:
                return t.get('processed_header', 'Processed files:\n{files}').format(files="\n".join(files_processed))
            else:
                return t.get('no_files_processed', 'No files were found to process.')

        except Exception as e:
            return f"Error: {str(e)}"

    def _load_identifiers(self, lint_file):
        with open(lint_file, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = r'\(id (\w+)\)'
        return re.findall(pattern, content)

    def _process_file(self, content, identifiers, language, comment_blocks):
        for identifier in identifiers:
            pattern = rf'(?m)^translate\s+{re.escape(language)}\s+{re.escape(identifier)}:(.*?)^(?=\S|\Z)'
            compiled_pattern = re.compile(pattern, re.DOTALL)
            bloque_match = compiled_pattern.search(content)
            if bloque_match:
                bloque_completo = bloque_match.group(0)
                if comment_blocks:
                    lineas_bloque = bloque_completo.strip().split("\n")
                    lineas_modificadas = ["# " + linea if linea.strip() else "" for linea in lineas_bloque]
                    bloque_modificado = "\n".join(lineas_modificadas) + "\n\n"
                else:
                    bloque_modificado = ""

                content = content.replace(bloque_completo, bloque_modificado)

        return content


def _build_html():
    trans_json = json.dumps(TRANSLATIONS, ensure_ascii=False)
    langs_json = json.dumps(LANGUAGES, ensure_ascii=False)
    settings = Api()._load_settings()
    settings_json = json.dumps(settings, ensure_ascii=False)
    html = HTML.replace('__TRANSLATIONS__', trans_json)
    html = html.replace('__LANGUAGES__', langs_json)
    html = html.replace('__SETTINGS__', settings_json)
    return html


if __name__ == '__main__':
    api = Api()
    html = _build_html()

    window = webview.create_window(
        TRANSLATIONS['es_ES']['app_title'],
        html=html,
        js_api=api,
        width=1000,
        height=700,
        resizable=True
    )

    api.window = window
    webview.start(gui='qt')
