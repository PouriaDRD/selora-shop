"use client";

import { Fragment } from "react/jsx-runtime";

import { Footer, Header } from "@/components/layouts";
import { FeaturesSection, HeroSection } from "@/components/pages/landing";
import CtaSection from "@/components/pages/landing/cta-section";

export default function LandingPage() {
	return (
		<Fragment>
			<Header />
			<main className="mx-auto container max-w-7xl px-4 space-y-16 pt-12">
				<HeroSection />

				<FeaturesSection />

				<CtaSection />
			</main>
			<Footer />
		</Fragment>
	);
}
