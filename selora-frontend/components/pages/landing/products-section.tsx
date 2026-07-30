"use client";

import Image from "next/image";
import Link from "next/link";

import { motion } from "framer-motion";

import { Skeleton } from "@/components/ui";
import { useGetCategoryDetails } from "@/features/store/mutations";
import type { CategoryDetail } from "@/features/store/types/category.type";
import type { Product } from "@/features/store/types/product.type";

const fallbackImage = "/images/product-fallback.png";

export function ProductsSection() {
	const { data, isLoading } = useGetCategoryDetails();

	if (isLoading) {
		return <ProductsSkeleton />;
	}

	if (!data?.status) {
		return (
			<ProductsMessage text="خطا در دریافت محصولات. لطفاً صفحه را رفرش کنید." />
		);
	}

	const categories = data.data as CategoryDetail[];

	if (!categories.length) {
		return <ProductsMessage text="محصولی یافت نشد." />;
	}

	return (
		<section id="products" className={`w-full space-y-16 py-20`} dir="rtl">
			{categories.map((category) => (
				<CategoryProducts key={category.id} category={category} />
			))}
		</section>
	);
}

function CategoryProducts({ category }: { category: CategoryDetail }) {
	return (
		<section className={`space-y-6`}>
			<div className={`flex items-center justify-between`}>
				<h2 className={`text-2xl font-bold tracking-tight`}>
					{category.name}
				</h2>

				<span
					className={`rounded-full bg-muted px-3 py-1 text-xs text-muted-foreground`}>
					{category.products.length} محصول
				</span>
			</div>

			<div
				className={`grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4`}>
				{category.products.map((product) => (
					<ProductCard key={product.id} product={product} />
				))}
			</div>
		</section>
	);
}

function ProductCard({ product }: { product: Product }) {
	const image = product.main_image?.image ?? fallbackImage;

	return (
		<motion.div
			initial={{
				opacity: 0,
				y: 20,
			}}
			whileInView={{
				opacity: 1,
				y: 0,
			}}
			viewport={{
				once: true,
			}}
			transition={{
				duration: 0.4,
			}}>
			<Link href={`/products/${product.slug}`}>
				<article
					className={`
						group overflow-hidden rounded-2xl border bg-card
						transition-all duration-300
						hover:-translate-y-1
						hover:shadow-xl
					`}>
					<div
						className={`
							relative aspect-square overflow-hidden
							bg-muted
						`}>
						<Image
							src={image}
							alt={product.main_image?.alt_text ?? product.name}
							fill
							priority={false}
							unoptimized
							className={`
								object-cover
								transition-transform duration-500
								group-hover:scale-105
							`}
							sizes={`(max-width: 640px) 100vw,
								(max-width: 1024px) 50vw,
								25vw`}
						/>

						<div
							className={`
								absolute inset-x-0 bottom-0
								h-24 bg-linear-to-t
								from-black/20 to-transparent
							`}
						/>
					</div>

					<div
						className={`
							space-y-4 p-5
						`}>
						<h3
							className={`
								line-clamp-1
								text-lg font-semibold
							`}>
							{product.name}
						</h3>

						<p
							className={`
								line-clamp-2 min-h-12
								text-sm leading-6
								text-muted-foreground
							`}>
							{product.description}
						</p>

						<div
							className={`
								flex items-center justify-between
								border-t pt-4
							`}>
							<span className={`font-bold`}>
								{formatPrice(product.base_price)} تومان
							</span>

							<span
								className={`
									text-xs font-medium
									${product.in_stock ? "text-green-600" : "text-destructive"}
								`}>
								{product.in_stock ? "موجود" : "ناموجود"}
							</span>
						</div>
					</div>
				</article>
			</Link>
		</motion.div>
	);
}

function formatPrice(price: number) {
	return new Intl.NumberFormat("fa-IR").format(price);
}

function ProductsMessage({ text }: { text: string }) {
	return (
		<section
			id="products"
			className={`flex w-full justify-center py-20`}
			dir="rtl">
			<p
				className={`
					text-sm text-muted-foreground
				`}>
				{text}
			</p>
		</section>
	);
}

function ProductsSkeleton() {
	return (
		<section id="products" className={`w-full space-y-14 py-20`}>
			{Array.from({
				length: 2,
			}).map((_, i) => (
				<div key={i} className={`space-y-6`}>
					<div
						className={`
							flex items-center justify-between
						`}>
						<Skeleton className={`h-7 w-40`} />

						<Skeleton className={`h-6 w-20 rounded-full`} />
					</div>

					<div
						className={`
							grid grid-cols-1 gap-6
							sm:grid-cols-2
							lg:grid-cols-4
						`}>
						{Array.from({
							length: 4,
						}).map((_, j) => (
							<Skeleton
								key={j}
								className={`
									h-96 rounded-2xl
								`}
							/>
						))}
					</div>
				</div>
			))}
		</section>
	);
}
