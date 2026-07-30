"use client";

import { useEffect, useMemo, useState } from "react";

import { Button } from "@/components/ui";
import type { ProductVariant } from "@/features/store/types";

interface Props {
	variants: ProductVariant[];
	onChange?: (variant: ProductVariant | undefined) => void;
}

export function VariantSelector({ variants, onChange }: Props) {
	const attributes = useMemo(() => {
		const map = new Map<string, string[]>();

		for (const variant of variants) {
			for (const attribute of variant.attributes) {
				const values = map.get(attribute.attribute) ?? [];

				if (!values.includes(attribute.value)) {
					values.push(attribute.value);
				}

				map.set(attribute.attribute, values);
			}
		}

		return map;
	}, [variants]);

	const [selectedAttributes, setSelectedAttributes] = useState<
		Record<string, string>
	>(() => {
		const selected: Record<string, string> = {};

		variants[0]?.attributes.forEach((attribute) => {
			selected[attribute.attribute] = attribute.value;
		});

		return selected;
	});

	const selectedVariant = useMemo(() => {
		return variants.find((variant) =>
			variant.attributes.every(
				(attribute) =>
					selectedAttributes[attribute.attribute] === attribute.value,
			),
		);
	}, [variants, selectedAttributes]);

	useEffect(() => {
		onChange?.(selectedVariant);
	}, [selectedVariant, onChange]);

	const isOptionAvailable = (attributeName: string, value: string) => {
		const nextSelection = {
			...selectedAttributes,
			[attributeName]: value,
		};

		return variants.some((variant) =>
			variant.attributes.every((attribute) => {
				const selectedValue = nextSelection[attribute.attribute];

				return !selectedValue || selectedValue === attribute.value;
			}),
		);
	};

	if (!variants.length) {
		return null;
	}

	return (
		<div className="space-y-6">
			{[...attributes.entries()].map(([attribute, values]) => (
				<div key={attribute} className="space-y-3">
					<h3 className="font-medium">{attribute}</h3>

					<div className="flex flex-wrap gap-2">
						{values.map((value) => {
							const active =
								selectedAttributes[attribute] === value;

							const available = isOptionAvailable(
								attribute,
								value,
							);

							return (
								<Button
									key={value}
									type="button"
									disabled={!available}
									variant={active ? "default" : "outline"}
									onClick={() =>
										setSelectedAttributes((prev) => ({
											...prev,
											[attribute]: value,
										}))
									}>
									{value}
								</Button>
							);
						})}
					</div>
				</div>
			))}
		</div>
	);
}
