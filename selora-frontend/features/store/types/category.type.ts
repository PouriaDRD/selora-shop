import { Product } from "./product.type";

export type Category = {
	id: string;
	name: string;
	slug: string;
};

export type CategoryDetail = Category & {
	products: Product[];
};
