from utils.helpers import log_info

class ToolManager:
    def __init__(self, config):
        self.config = config
        self.available_tools = ["web_request", "file_writer", "email_sender"]

    def list_tools(self):
        log_info("Listing available tools...")
        return self.available_tools

    def run_tool(self, tool_name: str, **kwargs):
        log_info(f"Running tool: {tool_name}")
        if tool_name == "web_request":
            return "Web request executed (placeholder)."
        if tool_name == "file_writer":
            return "File written successfully (placeholder)."
        if tool_name == "email_sender":
            return "Email sent (placeholder)."
        return "Tool not recognized."
