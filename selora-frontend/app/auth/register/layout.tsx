import { Fragment, PropsWithChildren } from "react";

import { Metadata } from "next";

import { Header } from "@/components/layouts";

export async function generateMetadata(): Promise<Metadata> {
	return {
		title: "ثبت نام",
		description: "ثبت نام سلورا",
	};
}

function RegisterLayout({ children }: Readonly<PropsWithChildren>) {
	return (
		<Fragment>
			<Header />
			{children}
		</Fragment>
	);
}

export default RegisterLayout;
