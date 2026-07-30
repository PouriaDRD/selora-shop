"use client";

import { useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

import { queryKeys } from "@/features/api/lib";

import { getCartSession } from "../actions";
import { useAddItem, useRemoveItem, useUpdateItem } from "../mutations";
import { useCartStore } from "../stores";
import type { CartItem } from "../types";

export function useCartActions() {
	const queryClient = useQueryClient();

	const cartStore = useCartStore();

	const addItemMutation = useAddItem();
	const updateItemMutation = useUpdateItem();
	const removeItemMutation = useRemoveItem();

	async function addItem(item: CartItem) {
		const cartSession = await getCartSession();

		if (!cartSession) {
			return;
		}
		cartStore.addItem(item);

		addItemMutation.mutate(
			{
				variant_id: item.variant_id,
				quantity: item.quantity,
				cartSession: cartSession,
			},
			{
				onSuccess: async (data) => {
					if (!data.status) {
						toast.error("خطا در اضافه کردن محصول", {
							description: data.message,
						});
						cartStore.removeItem(item.id);
					} else {
						cartStore.updateItemData(item.id, data.data);
					}
					await Promise.all([
						queryClient.invalidateQueries({
							queryKey: queryKeys.cart.cart,
						}),
					]);
				},

				onError: async () => {
					toast.error("خطا در اضافه کردن محصول");
					cartStore.removeItem(item.id);
					await Promise.all([
						queryClient.invalidateQueries({
							queryKey: queryKeys.cart.cart,
						}),
					]);
				},
			},
		);
	}

	function increaseQuantity(item_id: string) {
		const item = cartStore.getItem(item_id);
		if (!item) return;

		const new_quantity = item.quantity + 1;
		cartStore.increaseQuantity(item_id);

		updateItemMutation.mutate(
			{ item_id: item.id, new_quantity: new_quantity },
			{
				onSuccess: async (data) => {
					if (!data.status) {
						toast.error("خطا در اضافه کردن محصول");
						cartStore.decreaseQuantity(item_id);
					} else {
						cartStore.updateItemData(item_id, data.data);
					}
					await Promise.all([
						queryClient.invalidateQueries({
							queryKey: queryKeys.cart.cart,
						}),
					]);
				},
				onError: async () => {
					toast.error("خطا در اضافه کردن محصول");
					cartStore.decreaseQuantity(item_id);
					await Promise.all([
						queryClient.invalidateQueries({
							queryKey: queryKeys.cart.cart,
						}),
					]);
				},
			},
		);
	}

	function decreaseQuantity(item_id: string) {
		const item = cartStore.getItem(item_id);
		if (!item) return;

		const new_quantity = item.quantity - 1;
		cartStore.decreaseQuantity(item_id);

		if (new_quantity <= 0) {
			removeItemMutation.mutate(item.id!, {
				onSuccess: async (data) => {
					if (!data.status) {
						toast.error("خطا در حذف کردن محصول");
						cartStore.addItem(item);
					} else {
						cartStore.removeItem(item_id);
					}
					await Promise.all([
						queryClient.invalidateQueries({
							queryKey: queryKeys.cart.cart,
						}),
					]);
				},
				onError: async () => {
					toast.error("خطا در حذف کردن محصول");
					cartStore.addItem(item);
					await Promise.all([
						queryClient.invalidateQueries({
							queryKey: queryKeys.cart.cart,
						}),
					]);
				},
			});
		} else {
			updateItemMutation.mutate(
				{ item_id: item.id, new_quantity: new_quantity },
				{
					onSuccess: async (data) => {
						if (!data.status) {
							toast.error("خطا در حذف کردن محصول");
							cartStore.increaseQuantity(item_id);
						} else {
							cartStore.updateItemData(item_id, data.data);
						}
						await Promise.all([
							queryClient.invalidateQueries({
								queryKey: queryKeys.cart.cart,
							}),
						]);
					},
					onError: async () => {
						toast.error("خطا در حذف کردن محصول");
						cartStore.increaseQuantity(item_id);
						await Promise.all([
							queryClient.invalidateQueries({
								queryKey: queryKeys.cart.cart,
							}),
						]);
					},
				},
			);
		}
	}

	function removeItem(item_id: string) {
		const item = cartStore.getItem(item_id);
		if (!item) return;

		cartStore.removeItem(item_id);

		removeItemMutation.mutate(item.id!, {
			onSuccess: async (data) => {
				if (!data.status) {
					toast.error("خطا در حذف کردن محصول");
					cartStore.addItem(item);
				}
				await Promise.all([
					queryClient.invalidateQueries({
						queryKey: queryKeys.cart.cart,
					}),
				]);
			},
			onError: async () => {
				toast.error("خطا در حذف کردن محصول");
				cartStore.addItem(item);
				await Promise.all([
					queryClient.invalidateQueries({
						queryKey: queryKeys.cart.cart,
					}),
				]);
			},
		});
	}

	return {
		addItem,
		isAddingItem: addItemMutation.isPending,

		increaseQuantity,
		isIncreasingQuantity: updateItemMutation.isPending,

		decreaseQuantity,
		isDecreasingQuantity: updateItemMutation.isPending,

		removeItem,
		isRemovingItem: removeItemMutation.isPending,

		cartStore: cartStore,
	};
}
