"use client";

import { useParams } from "next/navigation";

import { ProductGallery, ProductInfo } from "@/components/pages/product";
import { Skeleton } from "@/components/ui";
import { useGetProductDetails } from "@/features/store/mutations";

export default function ProductDetailPage() {
	const params = useParams();

	const slug = params.slug as string;

	const { data, isLoading, isError } = useGetProductDetails(slug);

	if (isLoading) {
		return <ProductDetailSkeleton />;
	}

	if (isError || !data?.status) {
		return (
			<div className="py-20 text-center text-sm text-muted-foreground">
				خطا در دریافت اطلاعات محصول
			</div>
		);
	}

	const product = data.data;

	return (
		<section className="space-y-10">
			<div className="grid gap-8 lg:grid-cols-2">
				<ProductInfo product={product} />

				<ProductGallery images={product.images} name={product.name} />
			</div>
		</section>
	);
}

function ProductDetailSkeleton() {
	return (
		<div className="grid gap-8 lg:grid-cols-2">
			<div className="space-y-5">
				<Skeleton className="h-10 w-3/4" />
				<Skeleton className="h-5 w-full" />
				<Skeleton className="h-5 w-full" />
				<Skeleton className="h-12 w-40" />
			</div>
			<Skeleton className="aspect-square rounded-xl" />
		</div>
	);
}
