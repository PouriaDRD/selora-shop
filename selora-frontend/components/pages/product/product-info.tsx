"use client";

import { useState } from "react";

import { ProductCartAction } from "@/features/store/components";
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

			<div className="text-2xl font-bold">{formatPrice(price)} تومان</div>

			<VariantSelector
				variants={product.variants}
				onChange={setSelectedVariant}
			/>

			<ProductCartAction product={product} variant={selectedVariant} />
		</div>
	);
}

function formatPrice(price: number) {
	return new Intl.NumberFormat("fa-IR").format(price);
}
