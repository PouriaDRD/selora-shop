import Link from "next/link";

import { VariantProps } from "class-variance-authority";
import { ShoppingCart } from "lucide-react";

import { Badge, Button, buttonVariants } from "@/components/ui";
import { cn } from "@/features/shared/utils";

import { useGetMyCart } from "../hooks";

interface BaseSwitcherProps {
	className?: string;
	align?: "start" | "center" | "end";
	size?: VariantProps<typeof buttonVariants>["size"];
	variant?: VariantProps<typeof buttonVariants>["variant"];
}

export function ShoppingCartAction(props: BaseSwitcherProps) {
	const { cart, isLoading } = useGetMyCart();

	const count = cart?.items_count ?? 0;

	return (
		<Link href="/cart">
			<Button
				size={props.size ?? "icon-sm"}
				variant={props.variant ?? "outline"}
				className={cn("relative", props.className)}
				disabled={isLoading}>
				<ShoppingCart className="size-4" />

				{count > 0 && (
					<Badge
						className={`absolute -right-1 -top-1 flex h-5 min-w-5
						items-center justify-center rounded-full px-1 text-[10px]`}
						variant="default">
						{count.toLocaleString("fa-IR")}
					</Badge>
				)}
			</Button>
		</Link>
	);
}
