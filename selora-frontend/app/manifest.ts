import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
	return {
		name: "Selora Shop",
		short_name: "Selora",
		description: "Selora Shop",
		start_url: "/",
		display: "standalone",
		background_color: "#f9f9f9",
		theme_color: "#1447e6",
		icons: [
			{
				src: "/images/web-app-manifest-192x192.png",
				sizes: "192x192",
				type: "image/png",
			},
			{
				src: "/images/web-app-manifest-512x512.png",
				sizes: "512x512",
				type: "image/png",
			},
		],
	};
}
