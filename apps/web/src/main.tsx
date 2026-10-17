import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error("Expected a root element to mount the Neer-Nilam application.");
}

createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
