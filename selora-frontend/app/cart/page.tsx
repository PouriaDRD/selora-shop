"use client";

import { Fragment } from "react/jsx-runtime";

import { Footer, Header } from "@/components/layouts";

export default function CartPage() {
	return (
		<Fragment>
			<Header />
			<main className="mx-auto container max-w-7xl px-4 space-y-16 pt-12 flex-1">
				cart page
			</main>
			<Footer />
		</Fragment>
	);
}
