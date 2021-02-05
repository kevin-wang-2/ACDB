export type MergeType<T1, T2> = T1 & T2;

export function mergeObject<T1, T2>(A: T1, B: T2): MergeType<T1, T2> {
  const result: MergeType<T1, T2> = {} as MergeType<T1, T2>;

  for (const id in A) {
    (result as T1)[id] = A[id];
  }

  for (const id in B) {
    (result as T2)[id] = B[id];
  }

  return result;
}

type CurryMergeFunctor<T> = <R>(B: R) => CurryMergeResult<MergeType<T, R>>;

export interface CurryMergeResult<T> extends CurryMergeFunctor<T> {
  value?: T;
}

export function curryMerge<T>(A: T) {
  const result: CurryMergeResult<T> = function<R>(B: R) {
    return curryMerge(mergeObject(A, B));
  };
  result.value = A;

  return result;
}

export type MergeOptional<T1, T2> = T1 | (T1 & T2);
