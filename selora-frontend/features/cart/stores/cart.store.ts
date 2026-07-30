import { create } from "zustand";
import { persist } from "zustand/middleware";

import { Cart, CartItem, CartStore } from "../types";

export const useCartStore = create<CartStore>()(
	persist(
		(set, get) => ({
			items: [],

			setCart: (cart: Cart) => {
				set({
					...cart,
				});
			},

			addItem: (item) => {
				const exists = get().items.find((i) => i.id === item.id);

				if (exists) {
					set({
						items: get().items.map((i) =>
							i.id === item.id
								? {
										...i,
										quantity: i.quantity + item.quantity,
									}
								: i,
						),
					});

					return;
				}

				set({
					items: [...get().items, item],
				});
			},

			setItems: (items: CartItem[]) =>
				set(() => ({
					items,
				})),

			updateItemData: (item_id, data) =>
				set({
					items: get().items.map((i) =>
						i.id === item_id
							? {
									...i,
									...data,
								}
							: i,
					),
				}),

			removeItem: (item_id) =>
				set({
					items: get().items.filter((i) => i.id !== item_id),
				}),

			updateQuantity: (item_id, quantity) => {
				if (quantity <= 0) {
					get().removeItem(item_id);
					return;
				}

				set({
					items: get().items.map((i) =>
						i.id === item_id
							? {
									...i,
									quantity,
								}
							: i,
					),
				});
			},

			increaseQuantity: (item_id) => {
				const item = get().items.find((i) => i.id === item_id);
				if (!item) return;
				set({
					items: get().items.map((i) =>
						i.id === item_id
							? {
									...i,
									quantity: i.quantity + 1,
								}
							: i,
					),
				});
			},

			decreaseQuantity: (item_id) => {
				const item = get().items.find((i) => i.id === item_id);
				if (!item) return;
				set({
					items: get().items.map((i) =>
						i.id === item_id
							? {
									...i,
									quantity: i.quantity - 1,
								}
							: i,
					),
				});
			},

			clear: () =>
				set({
					items: [],
				}),

			getItemByVariantId: (variant_id) =>
				get().items.find((i) => i.variant_id === variant_id),

			hasItem: (item_id) => get().items.some((i) => i.id === item_id),

			getItem: (item_id) => get().items.find((i) => i.id === item_id),

			totalItems: () =>
				get().items.reduce((sum, item) => sum + item.quantity, 0),

			totalPrice: () =>
				get().items.reduce(
					(sum, item) => sum + item.subtotal * item.quantity,
					0,
				),
		}),
		{
			name: "shopping-cart",
		},
	),
);
