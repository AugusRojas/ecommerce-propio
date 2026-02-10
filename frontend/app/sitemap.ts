import { MetadataRoute } from 'next'
export default function sitemap(): MetadataRoute.Sitemap {
  return ['','/productos','/carrito','/checkout'].map((route) => ({ url: `http://localhost:3000${route}`, lastModified: new Date() }))
}
