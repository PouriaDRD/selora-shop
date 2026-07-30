"use client";

import { motion } from "framer-motion";
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
		icon: ShoppingBag,
		title: "کلکسیون‌های منتخب",
		desc: "محصولات برگزیده برای هر سلیقه و موقعیت.",
	},
	{
		icon: ShieldCheck,
		title: "تضمین کیفیت",
		desc: "مواد اولیه مرغوب و صنایع‌دستی قابل اعتماد.",
	},
	{
		icon: Truck,
		title: "ارسال رایگان",
		desc: "ارسال رایگان برای تمام سفارش‌ها در سراسر جهان.",
	},
	{
		icon: Headphones,
		title: "پشتیبانی ۲۴/۷",
		desc: "تیم ما همیشه و همه‌جا آماده کمک به شماست.",
	},
];

export function FeaturesSection() {
	return (
		<section className="w-full">
			<div className="mb-12 text-center">
				<h2 className="text-3xl font-bold" suppressHydrationWarning>
					چرا سلورا را انتخاب کنید؟
				</h2>
				<p
					className="mt-4 text-muted-foreground"
					suppressHydrationWarning>
					تجربه خریدی متفاوت با خدمات برتر ما.
				</p>
			</div>
			<div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
				{features.map((feature, idx) => (
					<Feature
						key={idx}
						idx={idx}
						Icon={feature.icon}
						title={feature.title}
						desc={feature.desc}
					/>
				))}
			</div>
		</section>
	);
}

interface FeatureProps {
	idx: number;
	Icon: LucideIcon;
	title: string;
	desc: string;
}

function Feature({ idx, Icon, title, desc }: FeatureProps) {
	return (
		<motion.div
			initial={{ opacity: 0, y: 20 }}
			whileInView={{ opacity: 1, y: 0 }}
			transition={{ duration: 0.4, delay: idx * 0.1 }}
			viewport={{ once: true }}>
			<Card className="h-full border-0 shadow-lg backdrop-blur-sm transition hover:scale-105 hover:shadow-xl">
				<CardHeader>
					<Icon className="h-12 w-12 text-primary" />
					<CardTitle suppressHydrationWarning>{title}</CardTitle>
				</CardHeader>
				<CardContent>
					<CardDescription
						className="text-muted-foreground"
						suppressHydrationWarning>
						{desc}
					</CardDescription>
				</CardContent>
			</Card>
		</motion.div>
	);
}
