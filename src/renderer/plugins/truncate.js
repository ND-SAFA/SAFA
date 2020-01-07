export default function (str, max = 60) {
  if (str.length > max) {
    return str.substr(0, max) + '...'
  }
  return str
}
