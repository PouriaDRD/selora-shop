export type ProductVariantImage = {
	id: string;
	image: string;
	alt_text: string;
	is_main: boolean;
};

export type ProductVariant = {
	id: string;
	sku: string;
	label: string;
	price: number;
	stock: number;
	is_active: boolean;
	images?: ProductVariantImage[] | null;
};
