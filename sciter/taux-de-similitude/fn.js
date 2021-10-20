export default function ({ data, COMS }) {
  const otez = 0;
  const midpoint = Math.ceil(COMS.length / 2);
  const COMS_a = COMS.slice(0, midpoint);
  const COMS_b = COMS.slice(midpoint);
  const A = COMS_b
    .map((com_b, i) => {
    const com_a = COMS_a[i];
    return com_b - (com_a * otez / 100);
  })
    .map(n => Math.max(n, 0));
  const B = A.reduce((sum, n) => sum + n, 0);
  const C = A.map(n => (100 / B) * n);
  const D = C.map((n, i) => Math.min(n, data[i]));
  const E = D.reduce((sum, n) => sum + n, 0);
  const F = Math.round(E);
  return F;
}                 