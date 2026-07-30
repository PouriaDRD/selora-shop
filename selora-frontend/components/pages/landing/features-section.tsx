"use client";

import { motion, type Variants } from "framer-motion";
import {
	Headphones,
	LucideIcon,
	ShieldCheck,
	ShoppingBag,
	Truck,
} from "lucide-react";

import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "@/components/ui";

const features = [
	{
		id: "collection",
		icon: ShoppingBag,
		title: "کلکسیون‌های منتخب",
		desc: "محصولات برگزیده و خاص برای هر سلیقه و سبک زندگی.",
	},
	{
		id: "quality",
		icon: ShieldCheck,
		title: "تضمین کیفیت",
		desc: "انتخاب دقیق محصولات با تمرکز روی کیفیت و دوام.",
	},
	{
		id: "shipping",
		icon: Truck,
		title: "ارسال سریع",
		desc: "ارسال مطمئن سفارش‌ها با تجربه‌ای ساده و سریع.",
	},
	{
		id: "support",
		icon: Headphones,
		title: "پشتیبانی همیشه همراه",
		desc: "تیم پشتیبانی ما برای پاسخ‌گویی در کنار شماست.",
	},
];

const containerVariants: Variants = {
	hidden: {},
	visible: {
		transition: {
			staggerChildren: 0.12,
		},
	},
};

const itemVariants: Variants = {
	hidden: {
		opacity: 0,
		y: 25,
	},
	visible: {
		opacity: 1,
		y: 0,
		transition: {
			duration: 0.5,
			ease: "easeOut",
		},
	},
};

export function FeaturesSection() {
	return (
		<section className="w-full py-20" dir="rtl">
			<div className="mx-auto mb-14 max-w-2xl text-center">
				<motion.h2
					suppressHydrationWarning
					initial={{ opacity: 0, y: 15 }}
					whileInView={{ opacity: 1, y: 0 }}
					viewport={{ once: true }}
					transition={{
						duration: 0.5,
						ease: "easeOut",
					}}
					className="text-3xl font-bold tracking-tight sm:text-4xl">
					چرا سلورا را انتخاب کنید؟
				</motion.h2>

				<motion.p
					suppressHydrationWarning
					initial={{ opacity: 0, y: 15 }}
					whileInView={{ opacity: 1, y: 0 }}
					viewport={{ once: true }}
					transition={{
						duration: 0.5,
						delay: 0.1,
						ease: "easeOut",
					}}
					className="mt-4 text-base leading-8 text-muted-foreground sm:text-lg">
					تجربه‌ای متفاوت از خرید آنلاین با کیفیت، اعتماد و خدمات
					حرفه‌ای.
				</motion.p>
			</div>

			<motion.div
				variants={containerVariants}
				initial="hidden"
				whileInView="visible"
				viewport={{
					once: true,
					margin: "-100px",
				}}
				className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
				{features.map((feature) => (
					<Feature
						key={feature.id}
						Icon={feature.icon}
						title={feature.title}
						desc={feature.desc}
					/>
				))}
			</motion.div>
		</section>
	);
}

interface FeatureProps {
	Icon: LucideIcon;
	title: string;
	desc: string;
}

function Feature({ Icon, title, desc }: FeatureProps) {
	return (
		<motion.div variants={itemVariants}>
			<Card
				className="
					group relative h-full overflow-hidden
					border bg-card/60
					transition-all duration-300
					hover:-translate-y-2
					hover:shadow-xl
				">
				<CardHeader className="space-y-5">
					<div
						className={`
							flex h-14 w-14 items-center justify-center
							rounded-2xl bg-primary/10
							transition-colors duration-300
							group-hover:bg-primary/20`}>
						<Icon className="h-7 w-7 text-primary" />
					</div>

					<CardTitle className="text-xl" suppressHydrationWarning>
						{title}
					</CardTitle>
				</CardHeader>

				<CardContent>
					<CardDescription
						className="leading-7"
						suppressHydrationWarning>
						{desc}
					</CardDescription>
				</CardContent>
			</Card>
		</motion.div>
	);
}
