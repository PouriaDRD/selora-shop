import { Fragment, PropsWithChildren } from "react";

import { Metadata } from "next";

import { Header } from "@/components/layouts";

export async function generateMetadata(): Promise<Metadata> {
	return {
		title: "ورود",
		description: "ورود سلورا",
	};
}

function LoginLayout({ children }: Readonly<PropsWithChildren>) {
	return (
		<Fragment>
			<Header />
			{children}
		</Fragment>
	);
}

export default LoginLayout;
