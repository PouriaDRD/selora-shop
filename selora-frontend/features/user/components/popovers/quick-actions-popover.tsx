"use client";

import { useState } from "react";

import Link from "next/link";

import {
	Avatar,
	AvatarFallback,
	AvatarImage,
	Button,
	Popover,
	PopoverContent,
	PopoverDescription,
	PopoverHeader,
	PopoverTitle,
	PopoverTrigger,
	Separator,
	Spinner,
} from "@/components/ui";
import { LogoutDialog } from "@/features/auth/components/dialogs";

import { useUser } from "../../context";
export function QuickActionsPopover() {
	const [open, setOpen] = useState(false);

	const { user, isLoading } = useUser();

	if (isLoading)
		return (
			<Button variant="outline" size={"icon-sm"}>
				<Spinner />
			</Button>
		);

	if (!user) return null;

	const initials = user.username.slice(0, 2).toUpperCase();

	return (
		<Popover open={open} onOpenChange={setOpen}>
			<PopoverTrigger
				render={
					<Button variant="ghost" className="px-0">
						<Avatar size="default">
							<AvatarImage
								src="/images/avatar-fallback.png"
								className="bg-muted p-2"
							/>

							<AvatarFallback>{initials}</AvatarFallback>
						</Avatar>
					</Button>
				}
			/>
			<PopoverContent>
				<PopoverHeader className="gap-0">
					<PopoverTitle>{user.username}</PopoverTitle>
					<PopoverDescription>{user.full_name}</PopoverDescription>
				</PopoverHeader>

				<Separator />

				<div className="flex flex-col gap-2 w-full">
					<Link href="/panel/dashboard">
						<Button
							className="w-full"
							variant="outline"
							size={"icon-sm"}
							onClick={() => setOpen(false)}>
							داشبورد
						</Button>
					</Link>

					<LogoutDialog
						collapsed={false}
						className="w-full"
						variant={"secondary"}
						size={"icon-sm"}
					/>
				</div>
			</PopoverContent>
		</Popover>
	);
}
