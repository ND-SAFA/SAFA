import CONFIG from 'config'

export default async function httpClient (relativeUrl, options) {
  options = options || {}
  options.headers = {
    'Content-Type': 'application/json'
  }
  const baseURL = CONFIG.get('services.api.url')
  return fetch(`${baseURL}/${relativeUrl}`, options)
}
