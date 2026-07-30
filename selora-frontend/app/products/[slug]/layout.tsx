import { Fragment, type ReactNode } from "react";

import type { Metadata } from "next";

import { Footer, Header } from "@/components/layouts";

interface ProductLayoutProps {
	children: ReactNode;
	params: Promise<{
		slug: string;
	}>;
}

export async function generateMetadata({
	params,
}: ProductLayoutProps): Promise<Metadata> {
	const { slug } = await params;

	return {
		title: `محصول ${slug}`,
		description: "مشاهده جزئیات محصول",
	};
}

export default async function ProductLayout({ children }: ProductLayoutProps) {
	return (
		<Fragment>
			<Header />
			<main className="mx-auto container max-w-7xl px-4 space-y-16 pt-12">
				{children}
			</main>
			<Footer />
		</Fragment>
	);
}
