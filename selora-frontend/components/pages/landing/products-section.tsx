"use client";

import { Skeleton } from "@/components/ui";
import { useGetCategoryDetails } from "@/features/store/mutations";

export function ProductsSection() {
	const { data, isLoading } = useGetCategoryDetails();

	if (isLoading) return <ProductsSkeleton />;

	if (!data || !data.status) {
		return (
			<ProductsMessage text="خطا در دریافت محصولات. لطفاً صفحه را رفرش کنید." />
		);
	}

	const categories = data.data;

	if (categories.length === 0) {
		return <ProductsMessage text="محصولی یافت نشد." />;
	}

	return (
		<section id="products" className="w-full">
			<ProductsSkeleton />
		</section>
	);
}

function ProductsMessage({ text }: { text: string }) {
	return (
		<section id="products" className="w-full">
			<p className="text-center text-sm text-muted-foreground">{text}</p>
		</section>
	);
}

function ProductsSkeleton() {
	return (
		<section id="products" className="w-full">
			<Skeleton className="mb-4 h-4 w-24" />
			<Skeleton className="mb-12 h-8 w-72" />
			<div className="space-y-14">
				{Array.from({ length: 2 }).map((_, i) => (
					<div key={i} className="space-y-6">
						<Skeleton className="h-6 w-32" />
						<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
							{Array.from({ length: 3 }).map((_, j) => (
								<Skeleton key={j} className="h-64 rounded-xl" />
							))}
						</div>
					</div>
				))}
			</div>
		</section>
	);
}
