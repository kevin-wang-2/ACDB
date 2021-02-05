export function mergeObject(A, B) {
  const result = {};
  for (const id in A) {
    result[id] = A[id];
  }
  for (const id in B) {
    result[id] = B[id];
  }
  return result;
}
export function curryMerge(A) {
  const result = function(B) {
    return curryMerge(mergeObject(A, B));
  };
  result.value = A;
  return result;
}
//# sourceMappingURL=mergeObject.js.map
