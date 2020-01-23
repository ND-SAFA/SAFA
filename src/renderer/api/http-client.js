import CONFIG from 'config'

export default async function httpClient (relativeUrl) {
  const baseURL = CONFIG.get('services.api.url')
  return fetch(`${baseURL}/${relativeUrl}`, {
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    }
  })
}
