export function generateSuccess(data) {
  return {
    success: true,
    error: 0,
    data: data || null
  };
}
export function generateError(error) {
  return {
    success: false,
    error: error || -1,
    data: null
  };
}
//# sourceMappingURL=result.js.map
