"use client";

import { useState } from "react";

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
					<button
						key={variant.id}
						onClick={() => setSelected(variant.id)}
						className={`
							rounded-lg border px-4 py-2 text-sm
							${
								selected === variant.id
									? "border-primary bg-primary text-primary-foreground"
									: "bg-background"
							}
						`}>
						{variant.label}
					</button>
				))}
			</div>
		</div>
	);
}
