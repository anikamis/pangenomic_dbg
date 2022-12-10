import { z } from "zod";

export const Node = z.object({
  id: z.string(),
  color: z.string(),
  strains: z.array(z.number()),
  val: z.number(),
});

export type Node = z.infer<typeof Node>;
