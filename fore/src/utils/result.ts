export interface Result<T> {
  success: boolean;
  error: number;
  data: T | null;
}

export function generateSuccess<T>(data?: T): Result<T> {
  return {
    success: true,
    error: 0,
    data: data || null
  };
}

export function generateError<T>(error?: number): Result<T> {
  return {
    success: false,
    error: error || -1,
    data: null
  };
}

export default Result;
