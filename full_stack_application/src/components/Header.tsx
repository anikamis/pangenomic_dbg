import { Header as MantineHeader, Title } from "@mantine/core";

const Header = () => (
  <MantineHeader height={{ base: 100, md: 70 }} p="md">
    <div style={{ display: "flex", alignItems: "center", height: "100%" }}>
      <Title order={1}>Colored De Bruijn Graph Visualizer</Title>
    </div>
  </MantineHeader>
);

export default Header;
