"use client";

import { Minus, Plus } from "lucide-react";

import { Button } from "@/components/ui";
import { useCartActions } from "@/features/cart/hooks";
import type { ProductDetail, ProductVariant } from "@/features/store/types";

interface Props {
	product: ProductDetail;
	variant?: ProductVariant;
}

export function ProductCartAction({ product, variant }: Props) {
	const {
		addItem,
		increaseQuantity,
		decreaseQuantity,
		isUpdatingItem,
		cartStore,
		isAddingItem,
	} = useCartActions();

	if (!variant) {
		return (
			<Button disabled className="w-full">
				ناموجود
			</Button>
		);
	}

	const cartItem = cartStore.getItemByVariantId(variant.id);

	const isAvailable =
		product.in_stock && variant.is_active && variant.stock > 0;

	if (!isAvailable) {
		return (
			<Button disabled className="w-full">
				ناموجود
			</Button>
		);
	}

	if (cartItem) {
		return (
			<div className="flex h-12 items-center overflow-hidden rounded-xl border">
				<Button
					variant="ghost"
					className="h-full w-14 rounded-none"
					disabled={isUpdatingItem}
					onClick={() => decreaseQuantity(cartItem.id)}>
					<Minus className="size-4" />
				</Button>

				<div className="flex-1 text-center font-semibold">
					{cartItem.quantity}
				</div>

				<Button
					variant="ghost"
					className="h-full w-14 rounded-none"
					disabled={isUpdatingItem}
					onClick={() => increaseQuantity(cartItem.id)}>
					<Plus className="size-4" />
				</Button>
			</div>
		);
	}

	return (
		<Button
			className="w-full"
			disabled={isAddingItem}
			onClick={() =>
				addItem({
					id: variant.id,
					variant_id: variant.id,
					price: variant.price,
					quantity: 1,
					product_name: product.name,
					subtotal: variant.price,
					variant_label: variant.label,
				})
			}>
			{isAddingItem ? "در حال افزودن..." : "افزودن به سبد خرید"}
		</Button>
	);
}
