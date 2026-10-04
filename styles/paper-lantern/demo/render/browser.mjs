// Headless Chrome: PLAYWRIGHT_CHROME env var first, else the headless shell in the local playwright cache
// GPU flags route WebGL through ANGLE/GL (~6x faster than default SwiftShader on Apple Silicon Macs)
import fs from 'fs'; import path from 'path';
function findExe() {
  if (process.env.PLAYWRIGHT_CHROME) return process.env.PLAYWRIGHT_CHROME;
  const base = path.join(process.env.HOME, 'Library/Caches/ms-playwright');
  const dirs = fs.existsSync(base) ? fs.readdirSync(base).filter(d => d.startsWith('chromium_headless_shell')).sort().reverse() : [];
  for (const d of dirs) {
    const p = path.join(base, d, 'chrome-headless-shell-mac-arm64/chrome-headless-shell');
    if (fs.existsSync(p)) return p;
  }
  return undefined;   // let playwright find it
}
export const EXE = findExe();
export const ARGS = ['--use-angle=gl', '--enable-gpu', '--ignore-gpu-blocklist', '--font-render-hinting=none', '--force-color-profile=srgb'];
