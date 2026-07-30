"use server";

import { cookies } from "next/headers";

export async function storeCartSession(sessionKey: string) {
	try {
		const cookieStore = await cookies();

		cookieStore.set({
			name: "crtss",
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

		return cookieStore.get("crtss")?.value;
	} catch (error) {
		if (process.env.NODE_ENV === "development") {
			console.error("[getCartSession]", error);
		}
		return null;
	}
}
