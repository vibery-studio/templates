---
name: chrome-devtools
description: Browser automation, debugging, and performance analysis using Puppeteer CLI scripts. Use for automating browsers, taking screenshots, analyzing performance, monitoring network traffic, web scraping, form automation, and JavaScript debugging.
license: MIT
---

# Chrome DevTools Automation

Browser automation, debugging, and performance analysis using Puppeteer CLI scripts.

## When to Use

- Automating browser interactions
- Taking screenshots of web pages
- Analyzing page performance
- Monitoring network traffic
- Web scraping
- Form automation
- JavaScript debugging

## Installation

```bash
# System Dependencies (Linux/WSL)
./install-deps.sh

# Node Dependencies
npm install puppeteer
```

## Core Scripts

### Navigation & Screenshots
```javascript
const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.goto('https://example.com');
await page.screenshot({ path: 'screenshot.png' });
await browser.close();
```

### Element Interaction
```javascript
await page.click('#submit-button');
await page.type('#input-field', 'text');
await page.select('#dropdown', 'option-value');
```

### JavaScript Evaluation
```javascript
const result = await page.evaluate(() => {
  return document.title;
});
```

### Network Monitoring
```javascript
page.on('request', request => {
  console.log(request.url());
});
page.on('response', response => {
  console.log(response.status());
});
```

### Performance Analysis
```javascript
const metrics = await page.metrics();
const performance = await page.evaluate(() => {
  return JSON.stringify(performance.timing);
});
```

## Critical Execution Protocol

1. **Always check `pwd` before running scripts**
2. Validate output files after operations complete
3. Images auto-compress if exceeding 5MB (requires ImageMagick)

## Output Format

All scripts return JSON to stdout:
- Success/failure status
- Operation results
- Errors route to stderr

Parse with `jq` for structured processing.

## Common Workflows

- Web scraping with data extraction
- Performance testing and benchmarking
- Form automation and testing
- Error monitoring and alerting
- Browser session maintenance

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
