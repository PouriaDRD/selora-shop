import { type NextRequest, NextResponse } from "next/server";

import { getSession } from "./features/auth/actions";

export async function proxy(request: NextRequest) {
	try {
		const session = await getSession();

		if (!session) {
			return redirectToLogin(request);
		}

		return NextResponse.next();
	} catch (error) {
		if (process.env.NODE_ENV === "development") {
			console.error("Proxy error:", error);
		}

		return redirectToLogin(request);
	}
}

function redirectToLogin(request: NextRequest) {
	const redirectUrl = request.nextUrl.clone();

	redirectUrl.pathname = "/auth/login";
	redirectUrl.search = "";

	const next =
		request.nextUrl.pathname +
		request.nextUrl.search +
		request.nextUrl.hash;

	redirectUrl.searchParams.set("next", next);

	return NextResponse.redirect(redirectUrl, {
		status: 303,
	});
}

export const config = {
	matcher: ["/panel/:path*"],
};
