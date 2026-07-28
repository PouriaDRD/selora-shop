import { AppIcon } from "@/components/icons";
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "@/components/ui";
import { ThemeSwitcher } from "@/features/preferences/components";
import { GridShape } from "@/features/shared/components";

export default function LandingPage() {
	return (
		<main
			className={`relative flex min-h-dvh flex-col items-center 
			justify-center px-6 pb-16 pt-12 text-center`}
			dir="rtl">
			<GridShape />

			<Card className="w-full max-w-xs">
				<CardHeader className="flex flex-col items-center justify-center gap-2">
					<AppIcon />
					<CardTitle suppressHydrationWarning>Selora Shop</CardTitle>

					<CardDescription suppressHydrationWarning>
						به سلورا شاپ خوش آمدید!
					</CardDescription>
				</CardHeader>

				<CardContent>
					<ThemeSwitcher />
				</CardContent>
			</Card>
		</main>
	);
}
