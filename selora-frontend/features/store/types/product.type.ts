import { ProductVariant } from "./variant.type";

export type ProductImage = {
	id: string;
	image: string;
	alt_text: string;
	is_main: boolean;
};

export type Product = {
	id: string;
	name: string;
	slug: string;
	description: string;
	base_price: number;
	in_stock: boolean;
	main_image?: ProductImage | null;
	created_at: Date;
};

export type ProductDetail = Omit<Product, "main_image"> & {
	variants: ProductVariant[];
	min_price: number;
	max_price: number;
	images?: ProductImage[] | null;
};
