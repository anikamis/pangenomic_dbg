import { AppShell, useMantineTheme } from "@mantine/core";

import AppContent from "./components/AppContent";
import Header from "./components/Header";

const App = () => {
  const theme = useMantineTheme();
  return (
    <AppShell
      className="page-wrap"
      styles={{
        main: {
          background: theme.colors.dark[8],
        },
      }}
      navbarOffsetBreakpoint="sm"
      asideOffsetBreakpoint="sm"
      header={<Header />}
      fixed
    >
      <AppContent />
    </AppShell>
  );
};

export default App;
