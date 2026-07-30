"use client";

import Link from "next/link";

import { ShoppingCart } from "lucide-react";

import { ThemeSwitcher } from "@/features/preferences/components";
import { QuickActionsPopover } from "@/features/user/components/popovers";
import { useUser } from "@/features/user/context";

import AppLogo from "../icons/app-logo";
import { Button } from "../ui";

export function Header() {
	const { isAuthenticated } = useUser();

	return (
		<header
			className={`bg-background/95 md:bg-background/95 sticky top-0 z-50 
        	flex items-center justify-between gap-4 container max-w-7xl mx-auto
			backdrop-blur-2xl px-4 py-2.5 overflow-hidden`}>
			<Link href={"/"}>
				<AppLogo />
			</Link>

			<div className="hidden items-center gap-8 md:flex">
				<Link
					href="/#products"
					className="text-sm font-medium text-muted-foreground">
					محصولات
				</Link>

				<Link
					href="#"
					className="text-sm font-medium text-muted-foreground">
					درباره ما
				</Link>

				<Link
					href="#"
					className="text-sm font-medium text-muted-foreground">
					تماس
				</Link>
			</div>

			<div className="flex items-center gap-2">
				<ThemeSwitcher />
				<Button variant={"outline"} size={"icon-sm"}>
					<ShoppingCart />
				</Button>
				{isAuthenticated ? (
					<QuickActionsPopover />
				) : (
					<Button>شروع کنید</Button>
				)}
			</div>
		</header>
	);
}
