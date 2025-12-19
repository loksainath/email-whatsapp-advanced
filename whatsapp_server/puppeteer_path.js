const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: true });
    console.log(browser.process().spawnfile);
    await browser.close();
})();
