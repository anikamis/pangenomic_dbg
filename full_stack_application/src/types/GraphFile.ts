import { z } from "zod";

import { Link } from "./Link";
import { Node } from "./Node";
import { Strain } from "./Strain";

export const GraphFile = z.object({
  nodes: z.array(Node),
  links: z.array(Link),
  strains: z.array(Strain),
});
