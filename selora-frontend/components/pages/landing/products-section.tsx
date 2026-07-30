"use client";

import Image from "next/image";
import Link from "next/link";

import { Skeleton } from "@/components/ui";
import { useGetCategoryDetails } from "@/features/store/mutations";
import type { CategoryDetail } from "@/features/store/types/category.type";
import type { Product } from "@/features/store/types/product.type";

export function ProductsSection() {
	const { data, isLoading } = useGetCategoryDetails();

	if (isLoading) return <ProductsSkeleton />;

	if (!data || !data.status) {
		return (
			<ProductsMessage text="خطا در دریافت محصولات. لطفاً صفحه را رفرش کنید." />
		);
	}

	const categories = data.data as CategoryDetail[];

	if (!categories.length) {
		return <ProductsMessage text="محصولی یافت نشد." />;
	}

	return (
		<section id="products" className="w-full space-y-14">
			{categories.map((category) => (
				<CategoryProducts key={category.id} category={category} />
			))}
		</section>
	);
}

function CategoryProducts({ category }: { category: CategoryDetail }) {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h2 className="text-xl font-bold">{category.name}</h2>

				<span className="text-sm text-muted-foreground">
					{category.products.length} محصول
				</span>
			</div>

			<div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
				{category.products.map((product) => (
					<ProductCard key={product.id} product={product} />
				))}
			</div>
		</div>
	);
}

function ProductCard({ product }: { product: Product }) {
	return (
		<Link href={`/product/${product.slug}`}>
			<article className="group overflow-hidden rounded-xl border bg-card transition hover:shadow-md">
				<div className="relative aspect-square overflow-hidden bg-muted">
					{product.main_image?.image ? (
						<Image
							src={product.main_image.image}
							alt={product.main_image.alt_text || product.name}
							fill
							priority
							unoptimized
							className="object-cover transition duration-300 group-hover:scale-105"
							sizes="(max-width: 768px) 100vw, 33vw"
						/>
					) : (
						<div className="flex h-full items-center justify-center text-sm text-muted-foreground">
							بدون تصویر
						</div>
					)}
				</div>

				<div className="space-y-3 p-4">
					<h3 className="line-clamp-1 font-semibold">
						{product.name}
					</h3>

					<p className="line-clamp-2 text-sm text-muted-foreground">
						{product.description}
					</p>

					<div className="flex items-center justify-between">
						<span className="font-bold">
							{formatPrice(product.base_price)} تومان
						</span>

						<span
							className={
								product.in_stock
									? "text-xs text-green-700"
									: "text-xs text-destructive"
							}>
							{product.in_stock ? "موجود" : "ناموجود"}
						</span>
					</div>
				</div>
			</article>
		</Link>
	);
}

function formatPrice(price: number) {
	return new Intl.NumberFormat("fa-IR").format(price);
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

						<div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
							{Array.from({ length: 4 }).map((_, j) => (
								<Skeleton key={j} className="h-80 rounded-xl" />
							))}
						</div>
					</div>
				))}
			</div>
		</section>
	);
}
