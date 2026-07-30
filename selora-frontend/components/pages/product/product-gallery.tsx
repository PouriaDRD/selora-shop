"use client";

import Image from "next/image";

import type { ProductImage } from "@/features/store/types";

interface Props {
	images?: ProductImage[] | null;
	name: string;
}

export function ProductGallery({ images, name }: Props) {
	const mainImage = images?.find((image) => image.is_main) ?? images?.[0];

	return (
		<div className="space-y-4">
			<div className="relative aspect-square overflow-hidden rounded-xl border bg-muted">
				{mainImage ? (
					<Image
						src={mainImage.image || "/images/product-fallback.png"}
						alt={mainImage.alt_text || name}
						fill
						priority
						unoptimized
						className="object-cover"
						sizes="(max-width:1024px)100vw,50vw"
					/>
				) : (
					<Image
						src={"/images/product-fallback.png"}
						alt={name}
						fill
						priority
						unoptimized
						className="object-cover"
						sizes="(max-width:1024px)100vw,50vw"
					/>
				)}
			</div>

			<div className="grid grid-cols-5 gap-3">
				{images?.map((image) => (
					<div
						key={image.id}
						className="relative aspect-square overflow-hidden rounded-lg border">
						<Image
							src={image.image || "/images/product-fallback.png"}
							alt={image.alt_text}
							fill
							unoptimized
							className="object-cover"
							sizes="100px"
						/>
					</div>
				))}
			</div>
		</div>
	);
}
