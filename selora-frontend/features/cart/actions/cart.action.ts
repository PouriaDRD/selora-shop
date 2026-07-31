"use server";

import { cookies } from "next/headers";

const CART_SESSION_COOKIE_NAME = "crtss";

export async function storeCartSession(sessionKey: string) {
	try {
		const cookieStore = await cookies();

		cookieStore.set({
			name: CART_SESSION_COOKIE_NAME,
			value: sessionKey,
			httpOnly: true,
			secure: true,
			sameSite: "lax",
			path: "/",
		});
	} catch (error) {
		if (process.env.NODE_ENV === "development") {
			console.error("[storeCartSession]", error);
		}
	}
}

export async function getCartSession() {
	try {
		const cookieStore = await cookies();

		return cookieStore.get(CART_SESSION_COOKIE_NAME)?.value;
	} catch (error) {
		if (process.env.NODE_ENV === "development") {
			console.error("[getCartSession]", error);
		}
		return null;
	}
}
