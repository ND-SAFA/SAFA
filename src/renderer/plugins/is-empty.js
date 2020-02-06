export default function (object) {
  if (typeof (object) !== 'object' || object === null) {
    return true
  }
  if (object instanceof Array) {
    return object.length === 0
  }
  return (Object.entries(object).length === 0)
}
