// Get the base URL for assets
export function getAssetUrl(path: string): string {
  const base = import.meta.env.BASE_URL
  // Remove leading slash from path if base already ends with /
  const cleanPath = path.startsWith('/') ? path.slice(1) : path
  return `${base}${cleanPath}`
}
