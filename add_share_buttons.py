#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Idempotent: insert a Pinterest Pin + X/Twitter share bar into
  - index.html  (before </body>, shares the home page)
  - guides/*-build-en.html  (before </article>, shares each guide)
Pinterest media prefilled: 3 characters with their pin image, others use promo_cover.
Inline-style only (no <style> edits, no external JS) -> clean & ad-blocker safe.
"""
import os, re, glob
from urllib.parse import urlencode

BASE = "https://genshin-guide-one-five.vercel.app"
ROOT = os.path.dirname(os.path.abspath(__file__))

PIN = {
    "albedo-build-en.html":   f"{BASE}/assets/promo_pinterest/pin_albedo.png",
    "xiao-build-en.html":     f"{BASE}/assets/promo_pinterest/pin_xiao.png",
    "yae-miko-build-en.html": f"{BASE}/assets/promo_pinterest/pin_yaemiko.png",
}
COVER = f"{BASE}/assets/promo_longtail/promo_cover.png"

# Inline-style share bar. {pin} and {tw} are the fully-built share endpoints.
SHARE_TMPL = """<section class="share-block" style="margin:48px 0 8px;padding-top:26px;border-top:1px solid rgba(255,255,255,.09);text-align:center">
  <div style="max-width:920px;margin:0 auto;padding:0 20px">
    <p style="color:#9aa6b8;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin:0 0 14px">{title}</p>
    <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
      <a href="{pin}" target="_blank" rel="noopener" aria-label="Share on Pinterest" style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;border-radius:999px;font-weight:600;font-size:14px;color:#fff;text-decoration:none;background:#E60023">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 0C5.373 0 0 5.372 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738a.36.36 0 0 1 .083.345c-.091.378-.293 1.194-.333 1.361-.052.22-.174.266-.401.16-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.632-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12 24c6.627 0 12-5.373 12-12C24 5.372 18.627 0 12 0z"/></svg>
        Pinterest
      </a>
      <a href="{tw}" target="_blank" rel="noopener" aria-label="Share on X" style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;border-radius:999px;font-weight:600;font-size:14px;color:#fff;text-decoration:none;background:#1d9bf0">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24h-6.66l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
        X / Twitter
      </a>
    </div>
  </div>
</section>
"""

def build_endpoints(page_url, media_url, text):
    pin = "https://www.pinterest.com/pin/create/button/?" + urlencode({
        "url": page_url, "media": media_url, "description": text})
    tw = "https://twitter.com/intent/tweet?" + urlencode({
        "url": page_url, "text": text})
    return pin, tw

def insert(path, title, page_url, media_url, text):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    if "share-block" in c:
        print(f"  skip (exists): {os.path.relpath(path, ROOT)}")
        return False
    pin, tw = build_endpoints(page_url, media_url, text)
    block = SHARE_TMPL.format(title=title, pin=pin, tw=tw)
    if path.endswith("index.html"):
        c = c.replace("</body>", block + "\n</body>", 1)
    else:
        c = c.replace("</article>", block + "\n</article>", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"  inserted: {os.path.relpath(path, ROOT)}")
    return True

# 1) Home page
print("Home page:")
insert(os.path.join(ROOT, "index.html"),
       "Share this site",
       BASE + "/",
       COVER,
       "Teyvat Starter Guide — Genshin Impact Beginner to Mid Guide + Interactive Tools")

# 2) All English build pages
print("Build pages:")
for fp in sorted(glob.glob(os.path.join(ROOT, "guides", "*-build-en.html"))):
    fn = os.path.basename(fp)
    name = fn.replace("-build-en.html", "").replace("-", " ").title()
    media = PIN.get(fn, COVER)
    page = f"{BASE}/guides/{fn}"
    text = f"{name} Build Guide — Genshin Impact 2026 | Teyvat Starter Guide"
    insert(fp, "Share this guide", page, media, text)

print("DONE")
