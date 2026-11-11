// usage: node shots.js <docs/index.html> <outdir> [hash ...]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [file, outdir, ...hashes] = process.argv.slice(2);
  // wrap like the publishing skeleton does (doctype + viewport meta) so phone layouts are realistic
  const fs = require('fs');
  const test = path.join(path.dirname(path.resolve(file)), '_test.html');
  fs.writeFileSync(test, '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>' + fs.readFileSync(file, 'utf8') + '</body></html>');
  const url = 'file://' + test;
  const browser = await chromium.launch();
  const runs = [
    { name: 'desk', viewport: { width: 1440, height: 900 }, scheme: 'light' },
    { name: 'deskdark', viewport: { width: 1440, height: 900 }, scheme: 'dark' },
    { name: 'phone', viewport: { width: 390, height: 844 }, scheme: 'light', mobile: true },
  ];
  for (const run of runs) {
    const ctx = await browser.newContext({ viewport: run.viewport, colorScheme: run.scheme, isMobile: !!run.mobile, hasTouch: !!run.mobile });
    const page = await ctx.newPage();
    const errs = [];
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    page.on('pageerror', e => errs.push(String(e)));
    for (const h of hashes) {
      await page.goto(url + '#' + h);
      await page.waitForTimeout(500);
      await page.evaluate(async () => { for (const img of document.querySelectorAll('#doc img')) { img.loading = 'eager'; } });
      await page.waitForTimeout(600);
      const info = await page.evaluate(() => ({
        title: document.title,
        overflow: document.documentElement.scrollWidth - window.innerWidth,
        broken: [...document.querySelectorAll('#doc img')].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src')?.slice(0, 60)).slice(0, 5),
        imgs: document.querySelectorAll('#doc img').length,
      }));
      console.log(run.name, h, JSON.stringify(info));
      await page.screenshot({ path: `${outdir}/${run.name}-${h}.png`, fullPage: false });
    }
    if (errs.length) console.log(run.name, 'errors:', errs.slice(0, 5));
    await ctx.close();
  }
  await browser.close();
})();
