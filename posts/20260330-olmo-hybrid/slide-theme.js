const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');
const html2pptx = require(path.join(process.env.HOME, '.claude/skills/pptx/scripts/html2pptx'));

const THEME = {
  bg: '#FFFFFF',
  headerBg: '#E41159',
  headerText: '#FFFFFF',
  bodyText: '#110A29',
  accent: '#E41159',
  codeBg: '#F5F3F2',
  codeBorder: '#D9D5D2',
  codeText: '#4421D2',
  cardBg: '#F5F3F2',
  cardBorder: '#D9D5D2',
  logo: 'kungfu-logo.png',
  logoOpacity: 0.6,
  font: 'Arial, sans-serif',
};

function injectTheme(html) {
  return html
    .replace(/%%BG%%/g, THEME.bg)
    .replace(/%%HEADER_BG%%/g, THEME.headerBg)
    .replace(/%%HEADER_TEXT%%/g, THEME.headerText)
    .replace(/%%BODY_TEXT%%/g, THEME.bodyText)
    .replace(/%%ACCENT%%/g, THEME.accent)
    .replace(/%%CODE_BG%%/g, THEME.codeBg)
    .replace(/%%CODE_BORDER%%/g, THEME.codeBorder)
    .replace(/%%CODE_TEXT%%/g, THEME.codeText)
    .replace(/%%CARD_BG%%/g, THEME.cardBg)
    .replace(/%%CARD_BORDER%%/g, THEME.cardBorder)
    .replace(/%%FONT%%/g, THEME.font)
    .replace(/%%LOGO%%/g, THEME.logo)
    .replace(/%%LOGO_OPACITY%%/g, String(THEME.logoOpacity));
}

async function buildDeck({ title, author, slides, slideDir, outputFile }) {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = author || 'KungFu AI';
  pptx.title = title;

  for (const file of slides) {
    console.log(`Processing ${file}...`);
    const srcHtml = fs.readFileSync(path.join(slideDir, file), 'utf8');
    const themed = injectTheme(srcHtml);
    const tmpPath = path.join(slideDir, '.tmp-' + file);
    fs.writeFileSync(tmpPath, themed);
    try { await html2pptx(tmpPath, pptx); } finally { fs.unlinkSync(tmpPath); }
  }

  const outPath = path.join(slideDir, outputFile);
  await pptx.writeFile({ fileName: outPath });
  console.log(`Created: ${outPath}`);
}

module.exports = { THEME, injectTheme, buildDeck };
