import type { NextConfig } from "next";

import path from "path";

const backendURL = new URL(
	process.env.NEXT_PUBLIC_BASE_API_URL || "http://127.0.0.1:8000/api/",
);

const nextConfig: NextConfig = {
	output: "standalone",

	typedRoutes: true,

	reactCompiler: true,

	reactStrictMode: process.env.NODE_ENV === "development",

	images: {
		remotePatterns: [
			{
				protocol: backendURL.protocol.replace(":", "") as
					| "http"
					| "https",
				hostname: backendURL.hostname,
				port: backendURL.port,
				pathname: "/media/**",
			},
			{
				protocol: "http",
				hostname: "127.0.0.1",
				port: "8000",
				pathname: "/media/**",
			},
			{
				protocol: "http",
				hostname: "127.0.0.1",
				port: "8000",
				pathname: "/media/**",
			},
			{
				protocol: "http",
				hostname: "localhost",
				port: "8000",
				pathname: "/media/**",
			},
		],
	},

	turbopack: {
		root: path.join(__dirname, ".."),
	},

	headers: async () => [
		{
			source: "/(.*)",
			headers: [
				{
					key: "X-Content-Type-Options",
					value: "nosniff",
				},
				{
					key: "X-Frame-Options",
					value: "DENY",
				},
				{
					key: "Referrer-Policy",
					value: "strict-origin-when-cross-origin",
				},
			],
		},
		{
			source: "/sw.js",
			headers: [
				{
					key: "Content-Type",
					value: "application/javascript; charset=utf-8",
				},
				{
					key: "Cache-Control",
					value: "no-cache, no-store, must-revalidate",
				},
				{
					key: "Content-Security-Policy",
					value: "default-src 'self'; script-src 'self'",
				},
			],
		},
	],
};

export default nextConfig;
