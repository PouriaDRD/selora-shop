"use client";

import { useState } from "react";

import { Button } from "@/components/ui";
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

	const isAvailable =
		product.in_stock &&
		!!selectedVariant &&
		selectedVariant.is_active &&
		selectedVariant.stock > 0;

	const buttonText = !product.in_stock
		? "ناموجود"
		: !selectedVariant
			? "ناموجود"
			: selectedVariant.stock <= 0
				? "ناموجود"
				: !selectedVariant.is_active
					? "ناموجود"
					: "افزودن به سبد خرید";

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

			<Button disabled={!isAvailable}>{buttonText}</Button>
		</div>
	);
}

function formatPrice(price: number) {
	return new Intl.NumberFormat("fa-IR").format(price);
}
