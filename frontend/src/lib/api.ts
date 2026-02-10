/**
 * API client helpers.
 *
 * - Public (read-only) endpoints: use axios with apiBaseUrl from @/config/site (no auth).
 * - Protected (create/update/delete) endpoints: use createAuthApiClient(username, password)
 *   so requests send HTTP Basic auth. Use this when building admin UI (e.g. login form).
 *
 * Backend Swagger UI: open /admin/414 and click "Authorize" to enter username/password
 * for testing protected endpoints.
 */
import axios from 'axios'
import type { AxiosInstance } from 'axios'
import { apiBaseUrl } from '@/config/site'

/**
 * Creates an axios instance that sends HTTP Basic auth on every request.
 * Use for admin-only API calls (POST/PATCH/DELETE blog, projects, etc.).
 *
 * @example
 * const api = createAuthApiClient(username, password)
 * await api.post('/api/v1/blog/', postData)
 * await api.patch(`/api/v1/blog/${id}`, patchData)
 * await api.delete(`/api/v1/blog/${id}`)
 */
export function createAuthApiClient(username: string, password: string): AxiosInstance {
  return axios.create({
    baseURL: apiBaseUrl,
    auth: { username, password },
  })
}
