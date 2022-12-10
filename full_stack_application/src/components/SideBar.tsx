import {
  Code,
  ColorInput,
  Container,
  Divider,
  Select,
  SelectItem,
  SimpleGrid,
  Space,
  Stack,
  Text,
  Title,
  useMantineTheme,
} from "@mantine/core";
import { useEffect, useState } from "react";

import { Node } from "../types/Node";

interface SideBarProps {
  numNodes: number;
  numLinks: number;
  selectedStrainID: string | null;
  strains: SelectItem[];
  selectedNode: Node | null;
  setSelectedStrainID: React.Dispatch<React.SetStateAction<string | null>>;
}

const SideBar = ({
  numNodes,
  numLinks,
  selectedStrainID,
  strains,
  selectedNode,
  setSelectedStrainID,
}: SideBarProps) => {
  const theme = useMantineTheme();

  const [strainNames, setStrainNames] = useState<string[]>([]);

  // Update strains whenever the node changes
  useEffect(() => {
    if (selectedNode) {
      const nodeStrains = strains.filter((strain) => selectedNode.strains.includes(+strain.value));
      console.log(nodeStrains);
      setStrainNames(nodeStrains.map((strain) => (strain.label ? strain.label : "")));
    }
  }, [selectedNode]);

  return (
    <Stack h="100%">
      <Title order={4}>Graph Information</Title>
      <SimpleGrid bg={theme.colors.dark[6]} cols={2} p="xs">
        <Text align="center">{numNodes.toLocaleString("en-US")} Nodes</Text>
        <Text align="center">{numLinks.toLocaleString("en-US")} Links</Text>
      </SimpleGrid>
      <Select
        label="Strain"
        placeholder="Select or search for a strain"
        data={strains}
        value={selectedStrainID}
        onChange={setSelectedStrainID}
        searchable
      />
      <Stack h="100%">
        <Title order={4}>Node Information</Title>
        <Container bg={theme.colors.dark[6]} h="100%" w="100%">
          {selectedNode ? (
            <>
              <Text>K-mer:</Text>
              <Code block>{selectedNode ? selectedNode.id : ""}</Code>
              <Divider my="md" />
              <Text>Strain(s):</Text>
              <Code block>{selectedNode ? strainNames.join(", ") : ""}</Code>
              <Space h="md" />
              <Divider my="md" />
              <Text>Color: </Text>
              <ColorInput disallowInput value={selectedNode ? selectedNode.color : ""} />
            </>
          ) : (
            <Text>Select a node or link to view its properties</Text>
          )}
        </Container>
      </Stack>
    </Stack>
  );
};

export default SideBar;
