export default function (object) {
  if (typeof (object) !== 'object') {
    return true
  }
  return (Object.entries(object).length === 0)
}
