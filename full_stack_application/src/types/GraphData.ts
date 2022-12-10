import { Link } from "./Link";
import { Node } from "./Node";

export default interface GraphData {
  nodes: Node[];
  links: Link[];
}
