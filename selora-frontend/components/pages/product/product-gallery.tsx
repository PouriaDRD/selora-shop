"use client";

import { useMemo, useState } from "react";

import Image from "next/image";

import type {
	ProductDetail,
	ProductImage,
	ProductVariantImage,
} from "@/features/store/types";

interface Props {
	product: ProductDetail;
}

type GalleryImage = ProductImage | ProductVariantImage;

export function ProductGallery({ product }: Props) {
	const images = useMemo<GalleryImage[]>(() => {
		const map = new Map<string, GalleryImage>();

		product.images?.forEach((image) => {
			map.set(image.id, image);
		});

		product.variants.forEach((variant) => {
			variant.images?.forEach((image) => {
				map.set(image.id, image);
			});
		});

		return [...map.values()];
	}, [product]);

	const defaultImage =
		images.find((image) => image.is_main) ?? images[0] ?? null;

	const [selectedImage, setSelectedImage] = useState<GalleryImage | null>(
		defaultImage,
	);

	return (
		<div className="space-y-4">
			<div className="relative aspect-square overflow-hidden rounded-xl border bg-muted">
				<Image
					src={selectedImage?.image ?? "/images/product-fallback.png"}
					alt={selectedImage?.alt_text || product.name}
					fill
					priority
					unoptimized
					className="object-cover"
					sizes="(max-width:1024px)100vw,50vw"
				/>
			</div>

			<div className="grid grid-cols-4 gap-3">
				{images.map((image) => (
					<button
						key={image.id}
						type="button"
						onClick={() => setSelectedImage(image)}
						className={`relative aspect-square overflow-hidden rounded-lg border transition
							${
								selectedImage?.id === image.id
									? "border-primary ring-2 ring-primary"
									: "border-border hover:border-primary/50"
							}`}>
						<Image
							src={image.image ?? "/images/product-fallback.png"}
							alt={image.alt_text}
							fill
							unoptimized
							className="object-cover"
							sizes="120px"
						/>
					</button>
				))}
			</div>
		</div>
	);
}
