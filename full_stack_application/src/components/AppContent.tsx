import { Button, Flex, Grid, LoadingOverlay, SelectItem, Tooltip } from "@mantine/core";
import { IconLoader, IconPlayerPause, IconPlayerPlay, IconRefresh } from "@tabler/icons";
import { useEffect, useState } from "react";

import GraphData from "../types/GraphData";
import { GraphFile } from "../types/GraphFile";
import { Node } from "../types/Node";
import { Strain } from "../types/Strain";
import Graph from "./Graph";
import SideBar from "./SideBar";

const DEFAULT_STRAINS = [{ value: "all", label: "All" }];

const AppContent = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [graphFile, setGraphFile] = useState<File | null>(null);
  const [graphPause, setGraphPause] = useState<boolean>(true);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [selectedStrainID, setSelectedStrainID] = useState<string | null>(null);
  const [strains, setStrains] = useState<SelectItem[]>(DEFAULT_STRAINS);
  const [strainNodesIDs, setStrainNodesIDs] = useState<string[]>([]);

  useEffect(() => {
    if (!graphFile) {
      return;
    }

    const fileReader = new FileReader();
    fileReader.readAsText(graphFile);

    fileReader.onload = () => {
      const result = fileReader.result;
      if (typeof result === "string") {
        try {
          const file = JSON.parse(result);
          const graphData = GraphFile.parse(file); // Validate that the JSON matches the expected schema
          setGraphData({ nodes: graphData.nodes, links: graphData.links });
          setStrains(
            DEFAULT_STRAINS.concat(
              graphData.strains.map((strain: Strain) => ({
                value: strain.id.toString(),
                label: strain.name,
              })),
            ),
          );
          setSelectedStrainID("all");
          setSelectedNode(null);
          console.log("File loaded and validated.");
        } catch (err) {
          console.error(err);
        }
      }
    };

    fileReader.onprogress = () => {
      setLoading(true);
    };

    fileReader.onloadend = () => {
      setLoading(false);
    };

    fileReader.onerror = () => {
      console.error(fileReader.error);
    };
  }, [graphFile]);

  useEffect(() => {
    if (!selectedStrainID || !graphData) {
      return;
    }

    if (selectedStrainID === "all") {
      // Set to all nodes
      const allNodeIDs = graphData.nodes.map((node: Node) => node.id);
      setStrainNodesIDs(allNodeIDs);
    } else {
      // Set to nodes that match the selected strain
      const strainNodeIDs = graphData.nodes
        .filter((node: Node) => node.strains.includes(+selectedStrainID))
        .map((node: Node) => node.id);
      setStrainNodesIDs(strainNodeIDs);
    }

    // Deslect node
    setSelectedNode(null);
  }, [selectedStrainID]);

  return (
    <>
      <LoadingOverlay visible={loading} loader={<IconLoader />} />
      <Grid h="100%" w="100%">
        <Grid.Col span={2}>
          <SideBar
            numNodes={graphData ? graphData.nodes.length : 0}
            numLinks={graphData ? graphData.links.length : 0}
            selectedNode={selectedNode}
            selectedStrainID={selectedStrainID}
            setSelectedStrainID={setSelectedStrainID}
            strains={strains}
          />
        </Grid.Col>
        <Grid.Col span={9}>
          <Graph
            graphData={graphData}
            graphPause={graphPause}
            strainNodesIDs={strainNodesIDs}
            setGraphFile={setGraphFile}
            setSelectedNode={setSelectedNode}
          />
        </Grid.Col>
        <Grid.Col span={1}>
          <Flex h="100%" direction="column" align="center" justify="flex-end" gap="sm">
            <Tooltip position="left" label="Play/Pause" withArrow>
              <Button w="100%" onClick={() => setGraphPause(!graphPause)}>
                {graphPause ? <IconPlayerPause /> : <IconPlayerPlay />}
              </Button>
            </Tooltip>
            <Tooltip position="left" label="Clear graph data" withArrow>
              <Button
                w="100%"
                onClick={() => {
                  setGraphPause(true);
                  setSelectedNode(null);
                  setSelectedStrainID(null);
                  setStrains(DEFAULT_STRAINS);
                  setGraphFile(null);
                  setGraphData(null);
                }}
              >
                <IconRefresh />
              </Button>
            </Tooltip>
          </Flex>
        </Grid.Col>
      </Grid>
    </>
  );
};

export default AppContent;
