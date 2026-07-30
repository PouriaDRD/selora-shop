"use client";

import Link from "next/link";

import { AppIcon } from "../icons";

const footerLinks = [
	{
		label: "حریم خصوصی",
		href: "/",
	},
	{
		label: "شرایط استفاده",
		href: "/",
	},
	{
		label: "تماس با ما",
		href: "/",
	},
];

export function Footer() {
	const year = new Date().getFullYear();

	return (
		<footer className="mt-20 border-t bg-background" dir="rtl">
			<div className="container mx-auto max-w-7xl px-4 py-10">
				<div
					className={`
						flex flex-col gap-8
						md:flex-row md:items-center md:justify-between`}>
					{/* Brand */}
					<Link
						href="/"
						className={`
							group flex items-center gap-3
							transition-opacity
							hover:opacity-80
						`}>
						<div
							className={`
								flex h-11 w-11 items-center justify-center
								rounded-xl bg-primary/10
								transition-colors
								group-hover:bg-primary/20
							`}>
							<AppIcon className="h-6 w-6 text-primary" />
						</div>

						<div className="flex flex-col">
							<span
								className="text-base font-bold"
								suppressHydrationWarning>
								سلورا
							</span>

							<span
								className="text-xs text-muted-foreground"
								suppressHydrationWarning>
								خریدی ساده، انتخابی بهتر
							</span>
						</div>
					</Link>

					{/* Navigation */}
					<nav className="flex flex-wrap justify-center gap-x-6 gap-y-3">
						{footerLinks.map((item, idx) => (
							<Link
								suppressHydrationWarning
								key={idx}
								href={item.href as "/"}
								className={`
									text-sm text-muted-foreground
									transition-colors
									hover:text-foreground
								`}>
								{item.label}
							</Link>
						))}
					</nav>

					{/* Copyright */}
					<p
						suppressHydrationWarning
						className={`
							text-center text-sm
							text-muted-foreground
							md:text-right
						`}>
						© {year} سلورا شاپ
						<br className="md:hidden" /> تمامی حقوق محفوظ است.
					</p>
				</div>
			</div>
		</footer>
	);
}
