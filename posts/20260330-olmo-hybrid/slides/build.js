const { buildDeck, injectTheme } = require('../slide-theme');
const { chromium } = require('playwright');
const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');
const html2pptx = require(path.join(process.env.HOME, '.claude/skills/pptx/scripts/html2pptx'));

// Slides that use KaTeX math — render as full-slide screenshots
const MATH_SLIDES = new Set([
  '03-the-paper.html',
  '06-delta-rule.html',
  '07-matrix-memory.html',
  '07b-linear-attention.html',
  '07c-mamba.html',
  '08-deltanet.html',
  '09-gated-deltanet.html',
  '09b-neg-eigenvalue-deep.html',
  '12-inference-state.html',
  '13-pretraining.html',
  '14-scaling-laws.html',
  '15-expressivity.html',
  '16b-chunk-parallel.html',
  '16d-chunk-pseudocode.html',
  '17-open-questions.html',
]);

const ALL_SLIDES = [
  '01-title.html',
  '02-outline.html',
  '03-the-paper.html',
  '04-architecture.html',
  '05-flashback-intro.html',
  '06-delta-rule.html',
  '07-matrix-memory.html',
  '07b-linear-attention.html',
  '07c-mamba.html',
  '08-deltanet.html',
  '09-gated-deltanet.html',
  '09b-neg-eigenvalue-deep.html',
  '11-landscape.html',
  '12-inference-state.html',
  '13-pretraining.html',
  '14-scaling-laws.html',
  '15-expressivity.html',
  '16-training-recipe.html',
  '16c-fla.html',
  '16b-chunk-parallel.html',
  '16d-chunk-pseudocode.html',
  '17-open-questions.html',
];

async function renderMathSlide(browser, htmlFile, pptx) {
  const srcHtml = fs.readFileSync(path.join(__dirname, htmlFile), 'utf8');
  const themed = injectTheme(srcHtml);
  const tmpHtml = path.join(__dirname, '.tmp-' + htmlFile);
  const tmpPng = path.join(__dirname, '.tmp-' + htmlFile.replace('.html', '.png'));
  fs.writeFileSync(tmpHtml, themed);

  const page = await browser.newPage();
  await page.setViewportSize({ width: 960, height: 540 });
  await page.goto('file://' + tmpHtml, { waitUntil: 'networkidle' });
  // Wait for KaTeX to render
  await page.waitForTimeout(1500);
  await page.screenshot({ path: tmpPng, type: 'png' });
  await page.close();

  // Read image as base64 data so pptxgenjs doesn't need the file at writeFile time
  const imgData = fs.readFileSync(tmpPng).toString('base64');
  const slide = pptx.addSlide();
  slide.addImage({
    data: 'image/png;base64,' + imgData,
    x: 0, y: 0,
    w: '100%', h: '100%',
  });

  if (fs.existsSync(tmpHtml)) fs.unlinkSync(tmpHtml);
  if (fs.existsSync(tmpPng)) fs.unlinkSync(tmpPng);
}

async function main() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'KungFu AI';
  pptx.title = 'OLMo Hybrid: Mixing Attention and Recurrence in LLMs';

  const browser = await chromium.launch();

  for (const file of ALL_SLIDES) {
    console.log(`Processing ${file}...`);
    if (MATH_SLIDES.has(file)) {
      await renderMathSlide(browser, file, pptx);
    } else {
      const srcHtml = fs.readFileSync(path.join(__dirname, file), 'utf8');
      const themed = injectTheme(srcHtml);
      const tmpPath = path.join(__dirname, '.tmp-' + file);
      fs.writeFileSync(tmpPath, themed);
      try {
        await html2pptx(tmpPath, pptx);
      } finally {
        if (fs.existsSync(tmpPath)) fs.unlinkSync(tmpPath);
      }
    }
  }

  await browser.close();

  const outPath = path.join(__dirname, 'olmo-hybrid-deck.pptx');
  await pptx.writeFile({ fileName: outPath });
  console.log(`Created: ${outPath}`);
}

main().catch(console.error);
