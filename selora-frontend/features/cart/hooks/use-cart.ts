"use client";

import { useEffect, useMemo } from "react";

import { storeCartSession } from "../actions";
import { useMyCart } from "../mutations";
import { useCartStore } from "../stores";

export function useGetMyCart() {
	const { data, isLoading } = useMyCart();

	const setCart = useCartStore((state) => state.setCart);

	const cart = data?.status ? data.data : null;
	const cartItems = useMemo(() => cart?.items ?? [], [cart?.items]);

	useEffect(() => {
		const handleCart = async () => {
			if (!cart) return;
			setCart(cart);
			await storeCartSession(cart.session_key);
		};

		handleCart();
	}, [cart, cartItems, setCart]);

	return {
		cart,
		cartItems,
		isLoading,
	};
}
