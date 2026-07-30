"use client";

import Link from "next/link";

import { motion } from "framer-motion";

import { Button } from "@/components/ui";

export function HeroSection() {
	return (
		<section className="w-full">
			<div className="flex items-center justify-center w-full">
				<motion.div
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.5 }}
					className="flex flex-col items-center justify-center w-full gap-6">
					<h1 className=" text-center text-4xl font-bold leading-tight text-primary md:text-5xl">
						سلورا
						<br />
						<span className="text-foreground">
							بگرد، ببین و خرید کن
						</span>
					</h1>

					<div className="flex flex-row-reverse gap-4">
						<Link href="/#products">
							<Button size={"lg"} variant={"default"}>
								مشاهده محصولات
							</Button>
						</Link>

						<Link href="/">
							<Button size={"lg"} variant={"secondary"}>
								بیشتر بدانید
							</Button>
						</Link>
					</div>
				</motion.div>
			</div>
		</section>
	);
}
