"use client";

import Link from "next/link";

import { AppIcon } from "../icons";

export function Footer() {
	const currentDate = new Date();
	const year = currentDate.getFullYear();

	return (
		<footer className="border-t mt-16">
			<div className="container max-w-7xl mx-auto px-4 py-8">
				<div className="flex flex-col items-center justify-between gap-4 md:flex-row">
					<div className="flex items-center gap-2">
						<AppIcon />
						<span
							className="text-sm font-semibold"
							suppressHydrationWarning>
							سلورا
						</span>
					</div>
					<p
						className="text-sm text-muted-foreground"
						suppressHydrationWarning>
						© {year} سلورا شاپ. تمامی حقوق محفوظ است.
					</p>
					<div className="flex gap-6">
						<Link
							href="#"
							className="text-sm text-muted-foreground"
							suppressHydrationWarning>
							حریم خصوصی
						</Link>
						<Link
							href="#"
							className="text-sm text-muted-foreground"
							suppressHydrationWarning>
							شرایط استفاده
						</Link>
					</div>
				</div>
			</div>
		</footer>
	);
}
