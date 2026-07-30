"use client";

import { Fragment } from "react/jsx-runtime";

import { Footer, Header } from "@/components/layouts";
import {
	CtaSection,
	FeaturesSection,
	HeroSection,
	ProductsSection,
} from "@/components/pages/landing";

export default function LandingPage() {
	return (
		<Fragment>
			<Header />
			<main className="mx-auto container max-w-7xl px-4 space-y-12 pt-12">
				<HeroSection />

				<ProductsSection />

				<FeaturesSection />

				<CtaSection />
			</main>
			<Footer />
		</Fragment>
	);
}
