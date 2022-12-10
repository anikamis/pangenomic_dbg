import { Group, Text, useMantineTheme } from "@mantine/core";
import { Dropzone } from "@mantine/dropzone";
import { IconFile, IconUpload, IconX } from "@tabler/icons";

interface FileUploadProps {
  setGraphFile: React.Dispatch<React.SetStateAction<File | null>>;
}

const FileUpload = ({ setGraphFile }: FileUploadProps) => {
  const theme = useMantineTheme();

  return (
    <Dropzone
      sx={{ width: "100%", height: "100%" }}
      onDrop={(files) => setGraphFile(files[0])}
      onReject={(files) => console.error("Rejected files:", files)}
      multiple={false}
      accept={["application/json"]}
    >
      <Group position="center" spacing="xl" style={{ minHeight: 220, pointerEvents: "none" }}>
        <Dropzone.Accept>
          <IconUpload
            size={50}
            stroke={1.5}
            color={theme.colors[theme.primaryColor][theme.colorScheme === "dark" ? 4 : 6]}
          />
        </Dropzone.Accept>
        <Dropzone.Reject>
          <IconX
            size={50}
            stroke={1.5}
            color={theme.colors.red[theme.colorScheme === "dark" ? 4 : 6]}
          />
        </Dropzone.Reject>
        <Dropzone.Idle>
          <IconFile size={50} stroke={1.5} />
        </Dropzone.Idle>

        <Text align="center" size="xl" inline>
          Drag a graph file here or click to a select file
        </Text>
      </Group>
    </Dropzone>
  );
};

export default FileUpload;
