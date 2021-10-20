import DATA from './data.js';
import FN from './fn.js';
import { EUROPE, ASIA, AMERICA } from './cells.js';

//main();

export default function(COMS) {
  //const COMS = [...new Array(36).fill(0), ...PCTS];

  const results = Object.entries(DATA)
    .reduce((results, [country, numbers]) => {
      const c = country.replace(/./, c => c.toLowerCase());
      const data = DATA[c];
      results[country] = FN({ data, COMS });
      return results;
    }, {});

  //for (const country of Object.keys(results)) {
  //  const works = results[country] === CONFIRM_RESULTS[country];
  //  if (!works) {
  //    throw new Error(`MISMATCH: ${country} ${results[country]} ${CONFIRM_RESULTS[country]}`);
  //  }
  //}

  //console.log(results);
  //console.log(EUROPE[0]);
  return results;
}
