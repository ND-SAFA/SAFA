export default function nonreactive (obj) {
  Object.keys(obj).forEach(key => {
    Object.defineProperty(obj, key, { configurable: false })
  })
}
