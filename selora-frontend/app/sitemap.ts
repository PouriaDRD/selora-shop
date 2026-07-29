import type { MetadataRoute } from "next";

function siteMap(): MetadataRoute.Sitemap {
	return [
		{
			url: "https://selora.pouria-drd.ir",
			lastModified: "07/30/2026",
			changeFrequency: "monthly",
			priority: 1,
		},
	];
}
export default siteMap;
