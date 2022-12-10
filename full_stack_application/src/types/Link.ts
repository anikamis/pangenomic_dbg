import { z } from "zod";

export const Link = z.object({
  source: z.string(),
  target: z.string(),
});

export type Link = z.infer<typeof Link>;
