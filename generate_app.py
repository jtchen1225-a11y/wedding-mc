# -*- coding: utf-8 -*-
"""
Generate complete index.html for Wedding MC Web App
"""
import json

with open('sections_data.json', 'r', encoding='utf-8') as f:
    sections = json.load(f)

# Flatten cue cards for Card Mode
all_cards = []
for sec_idx, sec in enumerate(sections):
    if sec.get('type') == 'summary':
        continue
    if sec.get('type') == 'tips':
        all_cards.append({
            "secId": sec['id'],
            "secTitle": sec['title'],
            "secTime": sec.get('time', ''),
            "speaker": "cue",
            "roleName": "舞台備忘",
            "text": "• " + "\n• ".join(sec['tips'])
        })
        continue
    for c_idx, c in enumerate(sec.get('cards', [])):
        card_copy = dict(c)
        card_copy['secId'] = sec['id']
        card_copy['secTitle'] = sec['title']
        card_copy['secTime'] = sec.get('time', '')
        card_copy['cardIndex'] = len(all_cards)
        all_cards.append(card_copy)

html_content = '''<!DOCTYPE html>
<html lang="zh-HK">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">
  <title>啟殷 × 芷蕎 婚禮完整司儀手卡</title>
  <meta name="theme-color" content="#0d1117">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="婚禮司儀稿">
  <link rel="icon" type="image/svg+xml" href="icon.svg">
  <link rel="manifest" href="manifest.json">
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: #151b28;
      --card-border: #232c3d;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --accent-gold: #fbbf24;
      --accent-rose: #f43f5e;
      --accent-blue: #38bdf8;
      --cue-bg: rgba(245, 158, 11, 0.12);
      --cue-border: #f59e0b;
      --cue-text: #fef3c7;
      --sister-color: #fda4af;
      --sister-bg: rgba(244, 63, 94, 0.12);
      --sister-border: #f43f5e;
      --brother-color: #7dd3fc;
      --brother-bg: rgba(56, 189, 248, 0.12);
      --brother-border: #38bdf8;
      --both-color: #fde047;
      --both-bg: rgba(250, 204, 21, 0.12);
      --both-border: #eab308;
      --header-bg: rgba(11, 15, 25, 0.92);
      --base-font-size: 20px;
      --font-scale: 1;
    }

    [data-theme="light"] {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --card-border: #e2e8f0;
      --text: #0f172a;
      --text-muted: #64748b;
      --header-bg: rgba(248, 250, 252, 0.94);
      --cue-bg: #fef3c7;
      --cue-border: #d97706;
      --cue-text: #78350f;
      --sister-color: #be123c;
      --sister-bg: #ffe4e6;
      --sister-border: #f43f5e;
      --brother-color: #0369a1;
      --brother-bg: #e0f2fe;
      --brother-border: #0284c7;
      --both-color: #854d0e;
      --both-bg: #fef9c3;
      --both-border: #ca8a04;
    }

    [data-theme="contrast"] {
      --bg: #000000;
      --card-bg: #111111;
      --card-border: #444444;
      --text: #ffffff;
      --text-muted: #cccccc;
      --header-bg: #000000;
      --accent-gold: #ffff00;
      --cue-bg: #221c00;
      --cue-border: #ffff00;
      --cue-text: #ffffaa;
      --sister-color: #ff99bb;
      --sister-bg: #330015;
      --sister-border: #ff3377;
      --brother-color: #99ddff;
      --brother-bg: #002233;
      --brother-border: #00aaff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans HK", sans-serif;
      font-size: calc(var(--base-font-size) * var(--font-scale));
      line-height: 1.68;
      overflow-x: hidden;
      transition: background-color 0.2s, color 0.2s;
      padding-bottom: 90px;
    }

    /* Fixed Stage Top Bar */
    header.stage-header {
      position: sticky;
      top: 0;
      z-index: 100;
      background: var(--header-bg);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--card-border);
      padding: 8px 12px;
    }

    .top-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
    }

    .wedding-title {
      font-size: 0.95rem;
      font-weight: 700;
      letter-spacing: 0.5px;
      color: var(--accent-gold);
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
    }

    .stage-clock {
      font-family: "SF Mono", "Courier New", monospace;
      font-size: 1.05rem;
      font-weight: 800;
      background: rgba(255, 255, 255, 0.08);
      padding: 3px 8px;
      border-radius: 6px;
      color: var(--text);
      letter-spacing: 1px;
    }

    .header-actions {
      display: flex;
      gap: 6px;
      align-items: center;
    }

    .btn-icon {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--card-border);
      color: var(--text);
      padding: 5px 9px;
      border-radius: 8px;
      font-size: 0.85rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      font-weight: 600;
    }

    .btn-icon.active {
      background: #10b981;
      color: #fff;
      border-color: #059669;
    }

    /* Stage Control Quick Strip */
    .controls-strip {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 6px;
      margin-top: 8px;
      padding-top: 6px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      overflow-x: auto;
      scrollbar-width: none;
    }
    .controls-strip::-webkit-scrollbar { display: none; }

    .role-pills {
      display: flex;
      gap: 4px;
      background: rgba(0, 0, 0, 0.25);
      padding: 3px;
      border-radius: 20px;
    }

    .role-pill {
      border: none;
      background: transparent;
      color: var(--text-muted);
      padding: 4px 10px;
      border-radius: 16px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }

    .role-pill.active {
      background: var(--text);
      color: var(--bg);
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }

    .font-pills {
      display: flex;
      gap: 3px;
    }

    .font-btn {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--card-border);
      color: var(--text);
      width: 32px;
      height: 28px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.85rem;
      cursor: pointer;
    }

    /* Horizontal Section Navigation */
    .section-nav-scroll {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding: 6px 0 2px;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
    }
    .section-nav-scroll::-webkit-scrollbar { display: none; }

    .nav-chip {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      padding: 4px 10px;
      border-radius: 14px;
      font-size: 0.78rem;
      font-weight: 600;
      white-space: nowrap;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s;
    }

    .nav-chip.active {
      border-color: var(--accent-gold);
      color: var(--accent-gold);
      background: rgba(251, 191, 36, 0.1);
    }

    /* Container */
    .container {
      max-width: 760px;
      margin: 0 auto;
      padding: 12px 14px;
    }

    /* Summary Table Card */
    .summary-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 14px;
      margin-bottom: 16px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    .summary-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
    }

    .summary-table th, .summary-table td {
      padding: 8px 6px;
      text-align: left;
      border-bottom: 1px solid var(--card-border);
    }

    .summary-table th {
      color: var(--accent-gold);
      font-weight: 700;
      border-bottom: 2px solid var(--accent-gold);
    }

    .summary-table td.time-col {
      font-family: monospace;
      font-weight: 700;
      color: var(--accent-blue);
      white-space: nowrap;
      width: 65px;
    }

    .summary-table td.phase-col {
      font-weight: 700;
      white-space: nowrap;
      width: 90px;
    }

    /* Section Header */
    .section-anchor {
      margin-top: 24px;
      margin-bottom: 12px;
      padding-top: 10px;
    }

    .section-header-box {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: linear-gradient(90deg, rgba(251, 191, 36, 0.15), transparent);
      border-left: 4px solid var(--accent-gold);
      padding: 8px 12px;
      border-radius: 0 8px 8px 0;
    }

    .section-title {
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--text);
    }

    .section-time-badge {
      background: var(--accent-gold);
      color: #000;
      font-size: 0.78rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 12px;
      font-family: monospace;
    }

    .section-subtitle {
      font-size: 0.84rem;
      color: var(--text-muted);
      margin: 4px 0 10px 4px;
    }

    /* Speech & Cue Cards */
    .speech-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 14px 16px;
      margin-bottom: 12px;
      position: relative;
      transition: all 0.2s ease;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    /* Dimming in filtered view */
    body[data-role="sister"] .speech-card.role-brother {
      opacity: 0.38;
      border-style: dashed;
      transform: scale(0.985);
    }

    body[data-role="sister"] .speech-card.role-sister {
      border-left: 5px solid var(--sister-border);
      background: linear-gradient(90deg, var(--sister-bg), var(--card-bg));
      box-shadow: 0 4px 14px rgba(244, 63, 94, 0.2);
    }

    body[data-role="brother"] .speech-card.role-sister {
      opacity: 0.38;
      border-style: dashed;
      transform: scale(0.985);
    }

    body[data-role="brother"] .speech-card.role-brother {
      border-left: 5px solid var(--brother-border);
      background: linear-gradient(90deg, var(--brother-bg), var(--card-bg));
      box-shadow: 0 4px 14px rgba(56, 189, 248, 0.2);
    }

    .card-header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }

    .speaker-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.88rem;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 16px;
      letter-spacing: 0.5px;
    }

    .role-sister .speaker-badge {
      background: var(--sister-bg);
      color: var(--sister-color);
      border: 1px solid var(--sister-border);
    }

    .role-brother .speaker-badge {
      background: var(--brother-bg);
      color: var(--brother-color);
      border: 1px solid var(--brother-border);
    }

    .role-both .speaker-badge {
      background: var(--both-bg);
      color: var(--both-color);
      border: 1px solid var(--both-border);
    }

    .speech-body {
      white-space: pre-wrap;
      word-break: break-word;
      font-size: 1.05rem;
      font-weight: 500;
      letter-spacing: 0.3px;
    }

    /* Stage Action Cue Card */
    .cue-card {
      background: var(--cue-bg);
      border: 2px dashed var(--cue-border);
      color: var(--cue-text);
      border-radius: 12px;
      padding: 12px 14px;
      margin: 10px 0 14px;
      font-size: 0.95rem;
      font-weight: 700;
      box-shadow: 0 2px 8px rgba(245, 158, 11, 0.15);
    }

    .cue-header {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--accent-gold);
      margin-bottom: 4px;
    }

    .cue-text {
      white-space: pre-wrap;
      line-height: 1.5;
    }

    .pause-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(239, 68, 68, 0.2);
      border: 1px solid #ef4444;
      color: #fca5a5;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.88rem;
      font-weight: 800;
      animation: pulseGlow 2s infinite;
    }

    @keyframes pulseGlow {
      0%, 100% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.03); opacity: 0.85; }
    }

    /* Stage Cue Card Mode (Teleprompter view) */
    #card-view-mode {
      display: none;
      position: fixed;
      inset: 0;
      background: var(--bg);
      z-index: 200;
      flex-direction: column;
      padding: env(safe-area-inset-top, 10px) 16px env(safe-area-inset-bottom, 16px);
    }

    .card-view-active #card-view-mode {
      display: flex;
    }
    .card-view-active #scroll-view-mode {
      display: none;
    }

    .card-view-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 0;
      border-bottom: 1px solid var(--card-border);
    }

    .card-progress {
      font-family: monospace;
      font-size: 1rem;
      font-weight: 800;
      color: var(--accent-gold);
    }

    .card-view-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 20px 8px;
      overflow-y: auto;
    }

    .teleprompter-card {
      background: var(--card-bg);
      border: 2px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .teleprompter-speaker {
      font-size: 1.25rem;
      font-weight: 800;
      margin-bottom: 14px;
    }

    .teleprompter-text {
      font-size: 1.5rem;
      font-weight: 600;
      line-height: 1.7;
      white-space: pre-wrap;
    }

    .card-view-bottom {
      display: flex;
      gap: 12px;
      padding-top: 12px;
    }

    .card-nav-btn {
      flex: 1;
      padding: 16px;
      border-radius: 12px;
      font-size: 1.15rem;
      font-weight: 800;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }

    .card-btn-prev {
      background: rgba(255, 255, 255, 0.1);
      color: var(--text);
    }

    .card-btn-next {
      background: var(--accent-gold);
      color: #000;
    }

    /* Bottom Quick Action Float Bar */
    .bottom-bar {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--header-bg);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-top: 1px solid var(--card-border);
      display: flex;
      justify-content: space-around;
      align-items: center;
      padding: 8px 12px calc(8px + env(safe-area-inset-bottom, 0px));
      z-index: 90;
    }

    .bottom-nav-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 3px;
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
    }

    .bottom-nav-btn.active {
      color: var(--accent-gold);
    }

    .bottom-nav-btn svg {
      width: 22px;
      height: 22px;
    }

    /* Drawer / Table of contents modal */
    .drawer-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.7);
      backdrop-filter: blur(4px);
      z-index: 300;
      display: none;
    }

    .drawer-overlay.open {
      display: block;
    }

    .drawer-panel {
      position: fixed;
      top: 0;
      bottom: 0;
      left: 0;
      width: 82%;
      max-width: 340px;
      background: var(--bg);
      border-right: 1px solid var(--card-border);
      z-index: 310;
      padding: 16px;
      overflow-y: auto;
      transform: translateX(-100%);
      transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .drawer-overlay.open .drawer-panel {
      transform: translateX(0);
    }

    .drawer-title {
      font-size: 1.1rem;
      font-weight: 800;
      color: var(--accent-gold);
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .drawer-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 8px;
      border-bottom: 1px solid var(--card-border);
      color: var(--text);
      text-decoration: none;
      font-size: 0.92rem;
      font-weight: 600;
      border-radius: 6px;
    }

    .drawer-item:active {
      background: rgba(255, 255, 255, 0.08);
    }

    .drawer-item-time {
      font-size: 0.8rem;
      color: var(--accent-blue);
      font-family: monospace;
    }

    /* Screen Wake Lock banner */
    .wake-banner {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid #10b981;
      color: #6ee7b7;
      border-radius: 8px;
      padding: 6px 10px;
      font-size: 0.8rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 10px;
    }

    /* Countdown Utility Modal */
    .countdown-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.85);
      z-index: 400;
      display: none;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .countdown-overlay.open { display: flex; }
    .countdown-num {
      font-size: 6rem;
      font-weight: 900;
      color: var(--accent-gold);
      margin: 20px 0;
      animation: popIn 0.8s ease;
    }
    @keyframes popIn {
      0% { transform: scale(0.5); opacity: 0; }
      50% { transform: scale(1.2); }
      100% { transform: scale(1); opacity: 1; }
    }
  </style>
</head>
<body>

  <!-- Top Sticky Stage Bar -->
  <header class="stage-header">
    <div class="top-row">
      <div class="wedding-title">
        <span>💍 啟殷 × 芷蕎</span>
      </div>
      <div class="stage-clock" id="live-clock">16:00:00</div>
      <div class="header-actions">
        <button class="btn-icon" id="btn-wake" title="保持螢幕長亮">
          <span>💡</span><span id="wake-status-text">長亮</span>
        </button>
        <button class="btn-icon" id="btn-theme" title="切換背景">
          <span>🌙</span>
        </button>
        <button class="btn-icon" id="btn-drawer" title="目錄">
          <span>☰</span>
        </button>
      </div>
    </div>

    <!-- Quick Role Filter and Font Size Adjustment -->
    <div class="controls-strip">
      <div class="role-pills">
        <button class="role-pill active" data-role="all">👥 雙人對稿</button>
        <button class="role-pill" data-role="sister">👩‍💼 表姐（主講）</button>
        <button class="role-pill" data-role="brother">👨‍💼 表姐夫（配合）</button>
      </div>
      <div class="font-pills">
        <button class="font-btn" id="btn-font-dec" title="字體縮小">A-</button>
        <button class="font-btn" id="btn-font-inc" title="字體放大">A+</button>
      </div>
    </div>

    <!-- Horizontal Fast Nav Pills -->
    <nav class="section-nav-scroll" id="quick-nav-pills">
      <a href="#sec-timeline" class="nav-chip">📋 流程速覽</a>
      <a href="#sec-tips" class="nav-chip">⚠️ 現場重點</a>
      <a href="#sec-1" class="nav-chip">16:00 證婚</a>
      <a href="#sec-2" class="nav-chip">20:00 開場白</a>
      <a href="#sec-3" class="nav-chip">新人進場</a>
      <a href="#sec-4" class="nav-chip">切蛋糕</a>
      <a href="#sec-5" class="nav-chip">合巹交杯</a>
      <a href="#sec-6" class="nav-chip">祝酒</a>
      <a href="#sec-7" class="nav-chip">新人互吻</a>
      <a href="#sec-8" class="nav-chip">致謝送花</a>
      <a href="#sec-9" class="nav-chip">上乳豬</a>
      <a href="#sec-10" class="nav-chip">早拍晚播</a>
      <a href="#sec-11" class="nav-chip">姊妹唱歌</a>
      <a href="#sec-12" class="nav-chip">二舅父獻唱</a>
      <a href="#sec-13" class="nav-chip">敬酒</a>
      <a href="#sec-14" class="nav-chip">第二輪拍照</a>
      <a href="#sec-15" class="nav-chip">完場感謝</a>
    </nav>
  </header>

  <!-- SCROLL VIEW MODE -->
  <main id="scroll-view-mode" class="container">
    <div id="wake-prompt-banner" class="wake-banner">
      <span>💡 已啟用防休眠功能，螢幕將保持恆亮，請安心主持。</span>
      <span style="cursor:pointer;" onclick="this.parentElement.style.display='none'">✕</span>
    </div>

'''

# Build HTML for sections
for sec in sections:
    sec_id = sec['id']
    sec_time = sec.get('time', '')
    sec_title = sec['title']
    sec_subtitle = sec.get('subtitle', '')
    
    html_content += f'''
    <section id="{sec_id}" class="section-anchor">
      <div class="section-header-box">
        <h2 class="section-title">{sec_title}</h2>
        <span class="section-time-badge">{sec_time}</span>
      </div>
      {f'<p class="section-subtitle">{sec_subtitle}</p>' if sec_subtitle else ''}
'''
    if sec.get('type') == 'summary':
        html_content += '''
      <div class="summary-card">
        <table class="summary-table">
          <thead>
            <tr>
              <th>時間</th>
              <th>環節</th>
              <th>現場 Cue / 安排</th>
            </tr>
          </thead>
          <tbody>
'''
        for it in sec['items']:
            html_content += f'''
            <tr>
              <td class="time-col">{it['time']}</td>
              <td class="phase-col">{it['phase']}</td>
              <td>{it['cue']}</td>
            </tr>
'''
        html_content += '''
          </tbody>
        </table>
      </div>
'''
    elif sec.get('type') == 'tips':
        html_content += '''
      <div class="cue-card" style="border-style: solid; border-color: var(--accent-gold);">
        <div class="cue-header">
          <span>⚠️ 司儀現場控制 6 大關鍵</span>
        </div>
        <ul style="padding-left: 18px; line-height: 1.8;">
'''
        for tip in sec['tips']:
            html_content += f'          <li>{tip}</li>\n'
        html_content += '''        </ul>
      </div>
'''
    else:
        # Regular cards
        for card in sec.get('cards', []):
            spk = card.get('speaker', '')
            text = card.get('text', '')
            role_name = card.get('roleName', '')
            
            if spk == 'cue':
                is_pause = card.get('type') == 'pause' or '停' in text or 'PAUSE' in text
                badge_html = '<span class="pause-badge">⏱️ 停頓等反應</span>' if is_pause else '<span>⚠️ 舞台動作（切勿讀出）</span>'
                html_content += f'''
      <div class="cue-card">
        <div class="cue-header">
          {badge_html}
        </div>
        <div class="cue-text">{text}</div>
      </div>
'''
            else:
                role_class = "role-sister" if spk == "sister" else ("role-brother" if spk == "brother" else "role-both")
                icon = "👩‍💼" if spk == "sister" else ("👨‍💼" if spk == "brother" else "👥")
                html_content += f'''
      <div class="speech-card {role_class}">
        <div class="card-header-bar">
          <span class="speaker-badge">
            <span>{icon}</span>
            <span>{role_name}</span>
          </span>
        </div>
        <div class="speech-body">{text}</div>
      </div>
'''

    html_content += '''    </section>\n'''

html_content += '''  </main>

  <!-- TELEPROMPTER / CUE CARD VIEW MODE -->
  <div id="card-view-mode">
    <div class="card-view-top">
      <div id="card-sec-badge" style="font-weight:700; color:var(--text-muted); font-size:0.9rem;">環節名稱</div>
      <div class="card-progress" id="card-progress-indicator">1 / 45</div>
      <button class="btn-icon" id="btn-exit-card" style="padding:4px 8px;">✕ 退出手卡</button>
    </div>
    <div class="card-view-content" id="teleprompter-touch-area">
      <div class="teleprompter-card" id="teleprompter-card-box">
        <div class="teleprompter-speaker" id="card-speaker-label">表姐</div>
        <div class="teleprompter-text" id="card-text-body">台詞內容</div>
      </div>
    </div>
    <div class="card-view-bottom">
      <button class="card-nav-btn card-btn-prev" id="btn-card-prev">◀ 上一張</button>
      <button class="card-nav-btn card-btn-next" id="btn-card-next">下一張 ▶</button>
    </div>
  </div>

  <!-- Bottom Navigation Float Bar -->
  <nav class="bottom-bar">
    <button class="bottom-nav-btn active" id="btn-nav-scroll">
      <svg fill="currentColor" viewBox="0 0 24 24"><path d="M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z"/></svg>
      <span>劇本捲動</span>
    </button>
    <button class="bottom-nav-btn" id="btn-nav-cards">
      <svg fill="currentColor" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10H7v-2h10v2z"/></svg>
      <span>逐張手卡</span>
    </button>
    <button class="bottom-nav-btn" id="btn-nav-countdown">
      <svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 14h-2v-2h2zm0-4h-2V7h2z"/></svg>
      <span>倒數幫手</span>
    </button>
    <button class="bottom-nav-btn" id="btn-nav-top">
      <svg fill="currentColor" viewBox="0 0 24 24"><path d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z"/></svg>
      <span>回頂部</span>
    </button>
  </nav>

  <!-- Side Table of Contents Drawer -->
  <div class="drawer-overlay" id="drawer-overlay">
    <div class="drawer-panel" id="drawer-panel">
      <div class="drawer-title">
        <span>📑 婚禮流程總目錄</span>
        <span style="cursor:pointer;" id="btn-close-drawer">✕</span>
      </div>
      <div style="margin-bottom:12px;">
        <input type="text" id="drawer-search" placeholder="🔍 搜尋台詞或環節..." style="width:100%; padding:8px 10px; border-radius:8px; border:1px solid var(--card-border); background:var(--card-bg); color:var(--text); font-size:0.9rem;">
      </div>
      <div id="drawer-list">
'''

for sec in sections:
    html_content += f'''
        <a href="#{sec['id']}" class="drawer-item" data-secid="{sec['id']}">
          <span>{sec['title']}</span>
          <span class="drawer-item-time">{sec.get('time', '')}</span>
        </a>
'''

html_content += '''      </div>
    </div>
  </div>

  <!-- Countdown Helper Modal -->
  <div class="countdown-overlay" id="countdown-modal">
    <h3 style="color:var(--text); font-size:1.4rem;">台上倒數小幫手</h3>
    <div class="countdown-num" id="countdown-display">3</div>
    <div style="display:flex; gap:12px; margin-top:16px;">
      <button class="btn-icon" style="padding:10px 18px; font-size:1rem;" onclick="startCountdown(3)">切蛋糕 3-2-1</button>
      <button class="btn-icon" style="padding:10px 18px; font-size:1rem;" onclick="startCountdown(1, true)">乾杯 1-2-3</button>
    </div>
    <button class="btn-icon" style="margin-top:20px; background:rgba(255,255,255,0.15);" onclick="document.getElementById('countdown-modal').classList.remove('open')">關閉</button>
  </div>

  <!-- Embedded Card Data for Card Mode -->
  <script>
    const allCardsData = ''' + json.dumps(all_cards, ensure_ascii=False) + ''';

    // Live Stage Clock
    function updateClock() {
      const now = new Date();
      const h = String(now.getHours()).padStart(2, '0');
      const m = String(now.getMinutes()).padStart(2, '0');
      const s = String(now.getSeconds()).padStart(2, '0');
      document.getElementById('live-clock').textContent = `${h}:${m}:${s}`;
    }
    setInterval(updateClock, 1000);
    updateClock();

    // Screen Wake Lock API
    let wakeLock = null;
    const btnWake = document.getElementById('btn-wake');
    const wakeStatusText = document.getElementById('wake-status-text');

    async function requestWakeLock() {
      try {
        if ('wakeLock' in navigator) {
          wakeLock = await navigator.wakeLock.request('screen');
          btnWake.classList.add('active');
          wakeStatusText.textContent = '常亮中';
          wakeLock.addEventListener('release', () => {
            btnWake.classList.remove('active');
            wakeStatusText.textContent = '已停用';
          });
        } else {
          btnWake.classList.add('active');
          wakeStatusText.textContent = '已常亮';
        }
      } catch (err) {
        console.log('Wake Lock Error:', err);
      }
    }

    btnWake.addEventListener('click', async () => {
      if (wakeLock) {
        await wakeLock.release();
        wakeLock = null;
        btnWake.classList.remove('active');
        wakeStatusText.textContent = '已暫停';
      } else {
        requestWakeLock();
      }
    });

    // Auto-request Wake Lock on first interaction
    document.addEventListener('click', () => {
      if (!wakeLock) requestWakeLock();
    }, { once: true });
    requestWakeLock();

    // Role Filter Handler
    const rolePills = document.querySelectorAll('.role-pill');
    rolePills.forEach(pill => {
      pill.addEventListener('click', () => {
        rolePills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        const role = pill.dataset.role;
        document.body.setAttribute('data-role', role);
        localStorage.setItem('wedding_mc_role', role);
      });
    });

    const savedRole = localStorage.getItem('wedding_mc_role');
    if (savedRole) {
      const matchPill = document.querySelector(`.role-pill[data-role="${savedRole}"]`);
      if (matchPill) matchPill.click();
    }

    // Font Size Scaler
    let fontScale = parseFloat(localStorage.getItem('wedding_mc_font_scale') || '1.0');
    function applyFontScale(scale) {
      fontScale = Math.min(Math.max(scale, 0.85), 1.6);
      document.documentElement.style.setProperty('--font-scale', fontScale);
      localStorage.setItem('wedding_mc_font_scale', fontScale);
    }
    applyFontScale(fontScale);

    document.getElementById('btn-font-inc').addEventListener('click', () => applyFontScale(fontScale + 0.1));
    document.getElementById('btn-font-dec').addEventListener('click', () => applyFontScale(fontScale - 0.1));

    // Theme Switcher (Dark -> Contrast -> Light)
    const themes = ['dark', 'contrast', 'light'];
    let currentThemeIdx = 0;
    const btnTheme = document.getElementById('btn-theme');

    function applyTheme(theme) {
      document.body.setAttribute('data-theme', theme);
      if (theme === 'dark') {
        btnTheme.innerHTML = '<span>🌙</span>';
      } else if (theme === 'contrast') {
        btnTheme.innerHTML = '<span>⚡</span>';
      } else {
        btnTheme.innerHTML = '<span>☀️</span>';
      }
      localStorage.setItem('wedding_mc_theme', theme);
    }

    btnTheme.addEventListener('click', () => {
      currentThemeIdx = (currentThemeIdx + 1) % themes.length;
      applyTheme(themes[currentThemeIdx]);
    });

    const savedTheme = localStorage.getItem('wedding_mc_theme') || 'dark';
    currentThemeIdx = themes.indexOf(savedTheme);
    applyTheme(savedTheme);

    // Drawer / Table of contents
    const drawerOverlay = document.getElementById('drawer-overlay');
    const btnDrawer = document.getElementById('btn-drawer');
    const btnCloseDrawer = document.getElementById('btn-close-drawer');
    const drawerSearch = document.getElementById('drawer-search');

    btnDrawer.addEventListener('click', () => drawerOverlay.classList.add('open'));
    btnCloseDrawer.addEventListener('click', () => drawerOverlay.classList.remove('open'));
    drawerOverlay.addEventListener('click', (e) => {
      if (e.target === drawerOverlay) drawerOverlay.classList.remove('open');
    });

    document.querySelectorAll('.drawer-item').forEach(item => {
      item.addEventListener('click', () => {
        drawerOverlay.classList.remove('open');
      });
    });

    drawerSearch.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      document.querySelectorAll('.drawer-item').forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(q) ? 'flex' : 'none';
      });
    });

    // Cue Card Mode Logic
    let currentCardIdx = 0;
    const btnNavScroll = document.getElementById('btn-nav-scroll');
    const btnNavCards = document.getElementById('btn-nav-cards');
    const btnExitCard = document.getElementById('btn-exit-card');
    const cardProgressIndicator = document.getElementById('card-progress-indicator');
    const cardSecBadge = document.getElementById('card-sec-badge');
    const cardSpeakerLabel = document.getElementById('card-speaker-label');
    const cardTextBody = document.getElementById('card-text-body');
    const teleprompterCardBox = document.getElementById('teleprompter-card-box');

    function renderCard(idx) {
      if (idx < 0) idx = 0;
      if (idx >= allCardsData.length) idx = allCardsData.length - 1;
      currentCardIdx = idx;

      const card = allCardsData[idx];
      cardProgressIndicator.textContent = `${idx + 1} / ${allCardsData.length}`;
      cardSecBadge.textContent = `${card.secTime} · ${card.secTitle}`;
      
      if (card.speaker === 'cue') {
        cardSpeakerLabel.innerHTML = '⚠️ 舞台動作（切勿讀出）';
        cardSpeakerLabel.style.color = 'var(--accent-gold)';
        teleprompterCardBox.style.border = '2px dashed var(--cue-border)';
        teleprompterCardBox.style.background = 'var(--cue-bg)';
      } else {
        const isSister = card.speaker === 'sister';
        const isBoth = card.speaker === 'both';
        cardSpeakerLabel.innerHTML = (isSister ? '👩‍💼 ' : (isBoth ? '👥 ' : '👨‍💼 ')) + (card.roleName || '');
        cardSpeakerLabel.style.color = isSister ? 'var(--sister-color)' : (isBoth ? 'var(--both-color)' : 'var(--brother-color)');
        teleprompterCardBox.style.border = '2px solid var(--card-border)';
        teleprompterCardBox.style.background = 'var(--card-bg)';
      }
      cardTextBody.textContent = card.text;
    }

    btnNavCards.addEventListener('click', () => {
      document.body.classList.add('card-view-active');
      btnNavCards.classList.add('active');
      btnNavScroll.classList.remove('active');
      renderCard(currentCardIdx);
    });

    function exitCardMode() {
      document.body.classList.remove('card-view-active');
      btnNavScroll.classList.add('active');
      btnNavCards.classList.remove('active');
    }

    btnExitCard.addEventListener('click', exitCardMode);
    btnNavScroll.addEventListener('click', exitCardMode);

    document.getElementById('btn-card-prev').addEventListener('click', () => renderCard(currentCardIdx - 1));
    document.getElementById('btn-card-next').addEventListener('click', () => renderCard(currentCardIdx + 1));

    // Touch swipe left/right for Card Mode
    let touchStartX = 0;
    const touchArea = document.getElementById('teleprompter-touch-area');
    touchArea.addEventListener('touchstart', e => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    touchArea.addEventListener('touchend', e => {
      const touchEndX = e.changedTouches[0].screenX;
      if (touchStartX - touchEndX > 50) {
        renderCard(currentCardIdx + 1); // Swipe left = next
      } else if (touchEndX - touchStartX > 50) {
        renderCard(currentCardIdx - 1); // Swipe right = prev
      }
    }, { passive: true });

    // Scroll back to top button
    document.getElementById('btn-nav-top').addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Countdown Helper
    const countdownModal = document.getElementById('countdown-modal');
    const countdownDisplay = document.getElementById('countdown-display');
    document.getElementById('btn-nav-countdown').addEventListener('click', () => {
      countdownModal.classList.add('open');
    });

    let countdownTimer = null;
    function startCountdown(startNum, forward = false) {
      if (countdownTimer) clearInterval(countdownTimer);
      let cur = startNum;
      countdownDisplay.textContent = cur;
      countdownTimer = setInterval(() => {
        if (!forward) {
          cur--;
          if (cur < 1) {
            clearInterval(countdownTimer);
            countdownDisplay.textContent = '🎉 切蛋糕！';
            return;
          }
        } else {
          cur++;
          if (cur > 3) {
            clearInterval(countdownTimer);
            countdownDisplay.textContent = '🥂 乾杯！';
            return;
          }
        }
        countdownDisplay.textContent = cur;
      }, 1000);
    }
  </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated index.html successfully with {len(all_cards)} cue cards.")
