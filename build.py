"""src/page.html 과 data/*.json 을 합쳐 GitHub Pages 용 index.html 을 만든다."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
IDS = ['area_monthly', 'area_yearly', 'ingredient_quarterly', 'ingredient_yearly', 'region_yearly']
data = {k: json.loads((ROOT / 'data' / f'{k}.json').read_text()) for k in IDS}
page = (ROOT / 'src' / 'page.html').read_text()

HEAD = r'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>만성질환 처방시장</title>
<meta name="description" content="고혈압, 이상지질혈증, 당뇨 8개 성분의 2024~2025년 처방시장 규모와 추이 (교육용 가상 청구자료)">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@400&display=swap">
<style>
:root {
  --font-anthropic-sans: "Noto Sans KR", system-ui, -apple-system, "Apple SD Gothic Neo", sans-serif;
  --font-anthropic-serif: "Noto Serif KR", "AppleMyungjo", Georgia, serif;
  --color-bg: #f6f6f3; --color-panel: #fcfcfb; --color-fg: #0b0b0b; --color-fg-muted: #6b6a66;
  --color-border-line: #e1e0d9; --color-ok: #006300; --color-bad: #c62f2f;
  --cds-gap-xs: 4px; --cds-gap-sm: 8px; --cds-gap-md: 16px; --cds-gap-lg: 24px;
  --cds-pad-xs: 4px; --cds-pad-sm: 8px; --cds-pad-lg: 20px; --cds-radius: 8px;
  --cds-font-size-caption: 12px; --cds-font-size-body: 14px; --cds-font-size-heading: 15px; --cds-font-size-title: 28px;
  --cds-font-weight-medium: 500; --cds-dur-slow: .3s;
  --cds-chart-grid: #e1e0d9; --cds-chart-axis: #c3c2b7; --cds-chart-muted: #c9c8c1; --cds-chart-reference: #898781;
  --cds-surface-popover: #ffffff; --cds-border: rgba(11,11,11,.12); --cds-shadow-popover: 0 4px 16px rgba(0,0,0,.10); --cds-text-secondary: #52514e;
  --s1: #2a78d6; --s2: #eb6834; --s3: #1baf7a; --s4: #eda100; --s5: #e87ba4; --s6: #008300; --s7: #6250d6; --s8: #e34948;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) { :root {
  --color-bg: #0d0d0d; --color-panel: #1a1a19; --color-fg: #f0efec; --color-fg-muted: #a3a29b;
  --color-border-line: #2c2c2a; --color-ok: #2fbf2f; --color-bad: #e66767;
  --cds-chart-grid: #2c2c2a; --cds-chart-axis: #383835; --cds-chart-muted: #4a4a46; --cds-chart-reference: #898781;
  --cds-surface-popover: #232322; --cds-border: rgba(255,255,255,.12); --cds-shadow-popover: 0 4px 16px rgba(0,0,0,.5); --cds-text-secondary: #c3c2b7;
  --s1: #3987e5; --s2: #d95926; --s3: #199e70; --s4: #c98500; --s5: #d55181; --s6: #008300; --s7: #9085e9; --s8: #e66767;
  color-scheme: dark;
} }
html, body { margin: 0; background: var(--color-bg); color: var(--color-fg); font-family: var(--font-anthropic-sans); font-size: 14px; }
#dash-root { max-width: 1200px; margin-inline: auto; padding-block: 32px 48px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
#dash-root .dash-skeleton { color: transparent; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>
// 대시보드 런타임(dash)을 대신하는 작은 shim: 데이터는 이 파일에 들어 있다.
window.dash = (() => {
  const DATA = __DATA__;
  const DEFAULTS = { area: '전체', metric: 'amount' };
  const calcs = {};
  const fns = [];
  let params = { ...DEFAULTS };
  const run = () => fns.forEach((f) => f());
  const css = getComputedStyle(document.documentElement);
  const api = {
    data: (id) => id in DATA ? { status: 'ok', data: DATA[id] } : id in calcs ? { status: 'ok', data: calcs[id] } : { status: 'missing', data: [] },
    calc: (id, o) => { calcs[id] = o.fn(...o.inputs.map((i) => api.data(i).data)); },
    onData: (fn) => { fns.push(fn); fn(); },
    params: () => ({ ...params }),
    setParams: (p) => { params = { ...params, ...p }; run(); },
    resetParams: () => { params = { ...DEFAULTS }; run(); },
    get colors() { return [1, 2, 3, 4, 5, 6, 7, 8].map((i) => css.getPropertyValue('--s' + i).trim()); },
    setLink: () => {},
  };
  let t;
  window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(run, 120); });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', run);
  return api;
})();
</script>
</head>
<body>
<div id="dash-root">
'''

out = HEAD.replace('__DATA__', json.dumps(data, ensure_ascii=False)) + page + '\n</div>\n</body>\n</html>\n'
(ROOT / 'index.html').write_text(out)
print('index.html', len(out.encode()), 'bytes')
