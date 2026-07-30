/**
 * Store API layer
 * All HTTP calls for STORE feature
 */

import { apiClient, endpoints } from "@/features/api/lib";

import { Category, CategoryDetail, Product, ProductDetail } from "../types";

export const storeApi = {
	categories: () => {
		return apiClient.get<Category[]>(endpoints.store.categories);
	},

	categoryDetails: () => {
		return apiClient.get<CategoryDetail[]>(endpoints.store.categoryDetails);
	},

	products: () => {
		return apiClient.get<Product[]>(endpoints.store.products);
	},

	productDetails: (slug: string) => {
		return apiClient.get<ProductDetail>(
			endpoints.store.productDetails(slug),
		);
	},
};
