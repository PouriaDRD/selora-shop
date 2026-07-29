import Image from "next/image";

import { cn } from "@/features/shared/utils";

interface Props {
	className?: string;
}

export const AppIcon = (props: Props) => {
	return (
		<Image
			src="/images/icon.svg"
			alt="Selora Logo"
			width={128}
			height={128}
			className={cn("w-8", props.className)}
		/>
	);
};
