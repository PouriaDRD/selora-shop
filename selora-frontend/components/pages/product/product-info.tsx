"use client";

import { useState } from "react";

import type { ProductDetail, ProductVariant } from "@/features/store/types";

import { VariantSelector } from "./variant-selector";

interface Props {
	product: ProductDetail;
}

export function ProductInfo({ product }: Props) {
	const [selectedVariant, setSelectedVariant] = useState<
		ProductVariant | undefined
	>(product.variants[0]);

	const price = selectedVariant?.price ?? product.min_price;

	return (
		<div className="space-y-6">
			<div>
				<h1 className="text-3xl font-bold">{product.name}</h1>

				<p className="mt-4 leading-8 text-muted-foreground">
					{product.description}
				</p>
			</div>

			<div className="text-2xl font-bold">
				{formatPrice(price)}
				{" تومان"}
			</div>

			<VariantSelector
				variants={product.variants}
				onChange={setSelectedVariant}
			/>

			<button
				disabled={!product.in_stock || !selectedVariant}
				className="h-12 w-full rounded-xl bg-primary text-primary-foreground disabled:opacity-50">
				{product.in_stock ? "افزودن به سبد خرید" : "ناموجود"}
			</button>
		</div>
	);
}

function formatPrice(price: number) {
	return new Intl.NumberFormat("fa-IR").format(price);
}
