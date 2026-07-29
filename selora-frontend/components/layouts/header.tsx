"use client";

import Link from "next/link";

import { ShoppingCart } from "lucide-react";

import { ThemeSwitcher } from "@/features/preferences/components";
import { QuickActionsPopover } from "@/features/user/components/popovers";

import AppLogo from "../icons/app-logo";
import { Button } from "../ui";

export function Header() {
	return (
		<header
			className={`bg-background/80 md:bg-background/80 sticky top-0 z-50 
        	flex items-center justify-between gap-4
			border-b backdrop-blur-2xl px-4 py-2.5`}>
			<div className="flex items-center gap-2">
				<QuickActionsPopover />
				<ThemeSwitcher />
				<Button variant={"outline"} size={"icon-sm"}>
					<ShoppingCart />
				</Button>
			</div>
			<Link href={"/"}>
				<AppLogo />
			</Link>
		</header>
	);
}
