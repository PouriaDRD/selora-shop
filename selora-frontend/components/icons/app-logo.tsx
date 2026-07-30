"use client";

import { Activity } from "react";

import { cn } from "@/features/shared/utils";

import { AppIcon } from "./app-icon";

interface Props {
	text?: string;
	className?: string;
	hideLogoText?: boolean;
	hideLogoTextOnMobile?: boolean;
}

export default function AppLogo(props: Props) {
	const { className, hideLogoText, hideLogoTextOnMobile = true } = props;
	return (
		<div
			className={cn(
				"flex items-center justify-center text-center gap-1",
				className,
			)}>
			<div className="size-8">
				<AppIcon className="size-full" />
			</div>
			<Activity mode={hideLogoText ? "hidden" : "visible"}>
				<span
					suppressHydrationWarning
					className={cn(
						"font-bold text-xl md:text-2xl text-center",
						`${hideLogoTextOnMobile && "hidden md:block"}`,
					)}>
					سلورا
				</span>
			</Activity>
		</div>
	);
}
