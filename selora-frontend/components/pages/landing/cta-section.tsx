"use client";

import Link from "next/link";

import { motion } from "framer-motion";

import { Button } from "@/components/ui";

export function CtaSection() {
	return (
		<section className="w-full py-20" dir="rtl">
			<motion.div
				initial={{
					opacity: 0,
					y: 30,
				}}
				whileInView={{
					opacity: 1,
					y: 0,
				}}
				viewport={{
					once: true,
					margin: "-100px",
				}}
				transition={{
					duration: 0.6,
					ease: "easeOut",
				}}
				className={`
					relative overflow-hidden
					rounded-3xl
					border
					bg-primary
					p-8
					text-center
					text-primary-foreground
					shadow-xl
					md:p-14`}>
				<div className="relative z-10 mx-auto max-w-3xl">
					<h2
						suppressHydrationWarning
						className="text-3xl font-extrabold tracking-tight sm:text-4xl">
						آماده‌اید سبک خود را ارتقا دهید؟
					</h2>

					<p
						suppressHydrationWarning
						className={`
							mx-auto mt-5 max-w-2xl
							text-sm leading-8
							text-primary-foreground/80
							sm:text-base`}>
						به هزاران مشتری خوشحال بپیوندید و مجموعه‌ای از محصولات
						خاص و باکیفیت را برای خود انتخاب کنید.
					</p>

					<div className="mt-8 flex justify-center">
						<Link href="/#products">
							<Button
								suppressHydrationWarning
								size="lg"
								variant="secondary"
								className={`
									min-w-40
									rounded-full
									font-semibold
									shadow-md
									transition-transform
									hover:-translate-y-1`}>
								شروع خرید
							</Button>
						</Link>
					</div>
				</div>

				{/* Decorative elements */}
				<div
					className={`
						pointer-events-none
						absolute -left-20 -top-20
						h-60 w-60
						rounded-full
						bg-white/10
						blur-3xl`}
				/>

				<div
					className={`
						pointer-events-none
						absolute -bottom-24 -right-20
						h-72 w-72
						rounded-full
						bg-white/10
						blur-3xl`}
				/>
			</motion.div>
		</section>
	);
}
