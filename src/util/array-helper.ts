type Scalar = number | string;

export function areEqual(array1: Scalar[], array2: Scalar[]): boolean {
  return (
    array1.length === array2.length &&
    array1.every((value, index) => value === array2[index])
  );
}
