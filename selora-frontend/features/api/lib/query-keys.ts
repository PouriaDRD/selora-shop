export const queryKeys = {
	auth: {
		history: ["auth", "history"],
	},

	accounts: {
		profile: ["accounts", "profile"],
	},

	store: {
		categories: ["store", "categories"],
		categoryDetails: ["store", "categories", "details"],
		products: ["store", "products"],
		productDetails: (slug: string) => [
			"store",
			"products",
			"details",
			slug,
		],
	},

	cart: {
		cart: ["cart", "cart"],
	},
};
