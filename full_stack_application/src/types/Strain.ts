import { z } from "zod";

export const Strain = z.object({
  id: z.number(),
  name: z.string(),
  colors: z.array(z.string()),
});

export type Strain = z.infer<typeof Strain>;
