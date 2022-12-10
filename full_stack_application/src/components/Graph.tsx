import { Graph as CosmosGraph, GraphConfigInterface } from "@cosmograph/cosmos";
import { useMantineTheme } from "@mantine/core";
import { useEffect, useRef, useState } from "react";

import GraphData from "../types/GraphData";
import { Link } from "../types/Link";
import { Node } from "../types/Node";
import FileUpload from "./FileUpload";

interface GraphProps {
  graphData: GraphData | null;
  graphPause: boolean;
  strainNodesIDs: string[];
  setGraphFile: React.Dispatch<React.SetStateAction<File | null>>;
  setSelectedNode: React.Dispatch<React.SetStateAction<Node | null>>;
}

const Graph = ({
  graphData,
  graphPause,
  strainNodesIDs,
  setGraphFile,
  setSelectedNode,
}: GraphProps) => {
  const theme = useMantineTheme();
  const cosmosCanvasRef = useRef<HTMLCanvasElement>(null);
  const [graph, setGraph] = useState<CosmosGraph<Node, Link> | null>(null);

  // Create the graph when the canvas ref is available and graph data is loaded
  useEffect(() => {
    if (!cosmosCanvasRef.current || !graphData) {
      return;
    }

    const graphConfig: GraphConfigInterface<Node, Link> = {
      backgroundColor: theme.colors.dark[6],
      spaceSize: 8192, // Max space size
      nodeColor: (node) => node.color,
      nodeSize: (node) => node.val,
      linkColor: "#909296",
      simulation: {
        linkDistance: 5,
      },
    };

    const cosmosGraph = new CosmosGraph(cosmosCanvasRef.current, graphConfig);

    // Graph event handlers
    cosmosGraph.config.events = {
      onClick: (node, i) => {
        if (node && i !== undefined) {
          setSelectedNode(node);
          cosmosGraph.selectNodeByIndex(i);
          cosmosGraph.zoomToNodeByIndex(i);
        } else {
          cosmosGraph.unselectNodes();
        }
      },
    };

    cosmosGraph.setData(graphData.nodes, graphData.links);
    cosmosGraph.fitView();
    setGraph(cosmosGraph);

    // Cleanup
    return () => {
      if (cosmosGraph) {
        cosmosGraph.destroy();
        setGraph(null);
      }
    };
  }, [cosmosCanvasRef, graphData]);

  // Pause and play the graph depending on pause state
  useEffect(() => {
    if (!graph) {
      return;
    }

    if (graphPause) {
      graph.start();
    } else {
      graph.pause();
    }
  }, [graphPause]);

  // Select the nodes that correspond to the selected strain
  useEffect(() => {
    if (!graph) {
      return;
    }

    graph.selectNodesByIds(strainNodesIDs);
  }, [strainNodesIDs]);

  return !graphData ? (
    <FileUpload setGraphFile={setGraphFile} />
  ) : (
    <canvas style={{ width: "100%", height: "100%", maxHeight: "800px" }} ref={cosmosCanvasRef} />
  );
};

export default Graph;
