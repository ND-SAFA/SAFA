const baseURL = process.env.ELECTRON_WEBPACK_APP_BASE_URL

export default async function httpClient (relativeUrl) {
  return fetch(`${baseURL}/${relativeUrl}`, {
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    }
  })
}
