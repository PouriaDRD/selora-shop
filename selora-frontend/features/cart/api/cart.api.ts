/**
 * Cart API layer
 * All HTTP calls for CART feature
 */

import { apiClient, endpoints } from "@/features/api/lib";

import { getCartSession } from "../actions";
import { Cart, CartItem } from "../types";

export const cartApi = {
	getCart: async () => {
		const cartSession = await getCartSession();

		return apiClient.get<Cart>(endpoints.cart.cart, {
			session_key: cartSession ?? undefined,
		});
	},

	addItem: (variant_id: string, quantity: number, cartSession: string) => {
		return apiClient.post<CartItem>(endpoints.cart.addItem, {
			cart_session_key: cartSession ?? "",
			variant_id,
			quantity,
		});
	},

	updateItem: (item_id: string, quantity: number) => {
		return apiClient.patch<CartItem>(endpoints.cart.updateItem(item_id), {
			quantity,
		});
	},

	removeItem: (item_id: string) => {
		return apiClient.delete(endpoints.cart.deleteItem(item_id));
	},
};
