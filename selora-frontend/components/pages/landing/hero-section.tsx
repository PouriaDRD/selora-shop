"use client";

import Link from "next/link";

import { motion } from "framer-motion";
import { ArrowLeft, Info, ShoppingBag } from "lucide-react";

import { Button } from "@/components/ui";

export function HeroSection() {
	return (
		<section
			className="relative flex w-full items-center justify-center overflow-hidden px-4 py-20"
			suppressHydrationWarning>
			<motion.div
				suppressHydrationWarning
				initial="hidden"
				animate="visible"
				variants={{
					hidden: {
						opacity: 0,
						y: 24,
					},
					visible: {
						opacity: 1,
						y: 0,
						transition: {
							duration: 0.6,
							ease: "easeOut",
							staggerChildren: 0.12,
						},
					},
				}}
				className="flex w-full max-w-4xl flex-col items-center justify-center gap-8 text-center">
				<motion.h1
					suppressHydrationWarning
					variants={{
						hidden: { opacity: 0, y: 15 },
						visible: { opacity: 1, y: 0 },
					}}
					className="text-5xl font-extrabold leading-[1.2] tracking-tight text-primary sm:text-6xl md:text-7xl">
					سلورا
					<span
						className="mt-3 block text-foreground"
						suppressHydrationWarning>
						بگرد، ببین و خرید کن
					</span>
				</motion.h1>

				<motion.p
					suppressHydrationWarning
					variants={{
						hidden: { opacity: 0, y: 15 },
						visible: { opacity: 1, y: 0 },
					}}
					className="max-w-xl text-base leading-8 text-muted-foreground sm:text-lg">
					تجربه‌ای متفاوت از خرید آنلاین با محصولات متنوع، کیفیت بالا
					و انتخابی ساده‌تر.
				</motion.p>

				<motion.div
					suppressHydrationWarning
					variants={{
						hidden: { opacity: 0, y: 15 },
						visible: { opacity: 1, y: 0 },
					}}
					className="flex flex-col gap-3 sm:flex-row">
					<Link href="/#products" prefetch>
						<Button
							size="lg"
							variant="default"
							className="group gap-2 min-w-40">
							<ShoppingBag className="h-5 w-5 transition-transform group-hover:scale-110" />
							<span suppressHydrationWarning>مشاهده محصولات</span>
							<ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-1" />
						</Button>
					</Link>

					<Link href="/" prefetch>
						<Button
							size="lg"
							variant="outline"
							className="group gap-2 min-w-40">
							<Info className="h-5 w-5 transition-transform group-hover:scale-110" />
							<span suppressHydrationWarning>بیشتر بدانید</span>
						</Button>
					</Link>
				</motion.div>
			</motion.div>
		</section>
	);
}
