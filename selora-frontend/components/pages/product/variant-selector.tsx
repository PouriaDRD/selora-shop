"use client";

import { useState } from "react";

import { Button } from "@/components/ui";
import type { ProductVariant } from "@/features/store/types";

interface Props {
	variants: ProductVariant[];
}

export function VariantSelector({ variants }: Props) {
	const [selected, setSelected] = useState(variants[0]?.id);

	if (!variants.length) {
		return null;
	}

	return (
		<div className="space-y-3">
			<h3 className="font-semibold">انتخاب مدل</h3>

			<div className="flex flex-wrap gap-3">
				{variants.map((variant) => (
					<Button
						key={variant.id}
						onClick={() => setSelected(variant.id)}
						variant={selected ? "default" : "secondary"}>
						{variant.label}
					</Button>
				))}
			</div>
		</div>
	);
}
