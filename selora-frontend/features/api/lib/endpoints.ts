export const endpoints = {
	auth: {
		login: "authentication/login/",
		register: "authentication/register/",
		refresh: "authentication/login/refresh/",
		history: "authentication/login/history/",
	},

	account: {
		profile: "accounts/profile/",
	},

	store: {
		categories: "store/categories/",
		categoryDetails: "store/categories-detail/",
		products: "store/products/",
		productDetails: (slug: string) => `store/products/${slug}/`,
	},

	cart: {
		cart: "cart/",

		addItem: "cart/items/add/",

		updateItem: (item_id: string) => `cart/items/${item_id}/update/`,

		deleteItem: (item_id: string) => `cart/items/${item_id}/delete/`,
	},
};
