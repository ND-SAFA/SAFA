import CONFIG from 'config'

export default function eventSource (url) {
  return new EventSource(`${CONFIG.get('services.api.url')}/${url}`)
}
