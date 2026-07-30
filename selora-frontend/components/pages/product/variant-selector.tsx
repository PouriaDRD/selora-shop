"use client";

import { useMemo, useState } from "react";

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

	const defaultSelection = useMemo(() => {
		const selected: Record<string, string> = {};

		variants[0]?.attributes.forEach((attribute) => {
			selected[attribute.attribute] = attribute.value;
		});

		return selected;
	}, [variants]);

	const [selectedAttributes, setSelectedAttributes] =
		useState<Record<string, string>>(defaultSelection);

	const selectedVariant = useMemo(() => {
		return variants.find((variant) =>
			variant.attributes.every(
				(attribute) =>
					selectedAttributes[attribute.attribute] === attribute.value,
			),
		);
	}, [variants, selectedAttributes]);

	useMemo(() => {
		onChange?.(selectedVariant);
	}, [selectedVariant, onChange]);

	if (!variants.length) {
		return null;
	}

	return (
		<div className="space-y-6">
			{[...attributes.entries()].map(([attribute, values]) => (
				<div key={attribute} className="space-y-3">
					<h3 className="font-medium">{attribute}</h3>

					<div className="flex flex-wrap gap-2">
						{values.map((value) => (
							<Button
								key={value}
								type="button"
								variant={
									selectedAttributes[attribute] === value
										? "default"
										: "outline"
								}
								onClick={() =>
									setSelectedAttributes((prev) => ({
										...prev,
										[attribute]: value,
									}))
								}>
								{value}
							</Button>
						))}
					</div>
				</div>
			))}
		</div>
	);
}
