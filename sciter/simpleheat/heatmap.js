import { $ } from '@sciter';
import * as env from "@env";
import * as sys from "@sys";

import { EUROPE, ASIA, AMERICA } from '../taux-de-similitude/cells.js';
//import TEST_DATA from '../taux-de-similitude/confirm-results.js';
/*
const _ = [...EUROPE, ...ASIA, ...AMERICA];
const MISSING = Object.entries(TEST_DATA).map(([country]) => {
  return _.find(({ region }) => region === country + 1) ? null : country;
}).filter(Boolean);

console.log(JSON.stringify(MISSING));
*/

export default async function heatmap(TEST_DATA, TEMP_FOLDER) {
  console.log("heatmap.js > heatmap()");
  console.log(TEMP_FOLDER);
  const EUROPE_DATA = Object.entries(TEST_DATA).map(([country, percent]) => {
    const entry = EUROPE.find(({ region }) => region === country + 1);
    if (!entry) {
      return [0, 0, 0];
    }
    const { x, y } = entry;
    return [x, y, percent / 3];
  });

  const ASIA_DATA = Object.entries(TEST_DATA).map(([country, percent]) => {
    const entry = ASIA.find(({ region }) => region === country + 1);
    if (!entry) {
      return [0, 0, 0];
    }
    const { x, y } = entry;
    return [x, y, percent / 3];
  });

  const AMERICA_DATA = Object.entries(TEST_DATA).map(([country, percent]) => {
    const entry = AMERICA.find(({ region }) => region === country + 1);
    if (!entry) {
      return [0, 0, 0];
    }
    const { x, y } = entry;
    return [x, y, percent / 3];
  });

  const DATA = {
    EUROPE_DATA,
    ASIA_DATA,
    AMERICA_DATA,
  };

  Object.values(DATA).forEach(data => {
    data.forEach(a => {
      a.x += 25 / 2;
      a.y += 18 / 2;
    });
  });

  for (const continent of ['europe', 'asia', 'america']) {
    const canvas = $(`#${continent}`);
    const image = new Graphics.Image(canvas.width, canvas.height, function (gfx) {
      return painter(gfx, DATA[`${continent.toUpperCase()}_DATA`], this);
    });
    console.log(`${TEMP_FOLDER}/${continent}.png`);
    const europe = await Graphics.Image.load(`${TEMP_FOLDER}/sciter/${continent}.png`);
    canvas.paintContent = function (gfx) { gfx.draw(image); }
    const snapshot = new Graphics.Image(canvas.width, canvas.height, canvas);
    const png = snapshot.toBytes('jpeg')
    const file = await sys.fs.open(`${TEMP_FOLDER}/output.jpeg`, 'w+', 0o666);
    await file.write(png);
    file.close();
    console.log(Window.this.xcall('bob', continent));
    /*const heatmap = await Graphics.Image.load('heatmap.jpeg');
    canvas.paintContent = function (gfx) {
      gfx.draw(heatmap);
      gfx.draw(europe);
    }
    canvas.requestPaint();*/
    //canvas.remove();

    const HEATMAP = await Graphics.Image.load(`${TEMP_FOLDER}/${continent}.jpeg`);
    $(`img[name="${continent}"]`).paintContent = function (gfx) {
      gfx.draw(HEATMAP); 
      gfx.draw(europe);
    }
  }
}

function painter(ctx, data, self) {
  data.forEach(([x, y, r]) => {
    ctx.fillStyle = 'white';
    ctx.beginPath();
    ctx.strokeStyle = 'white';
    ctx.ellipse(x, y, r, r, Math.PI / 4, 0, 2 * Math.PI);
    ctx.closePath();
    ctx.fill();
  });
  self.requestPaint();
}