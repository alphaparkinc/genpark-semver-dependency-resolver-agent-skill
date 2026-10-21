"""MCP Server for SemVer Dependency Resolver Agent.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import SemVerDependencyResolver

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "satisfies",
                                "description": "Check if a SemVer version satisfies a constraint range",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "version": {"type": "string"},
                                        "constraint": {"type": "string"}
                                    },
                                    "required": ["version", "constraint"]
                                }
                            },
                            {
                                "name": "resolve_best_version",
                                "description": "Resolve maximum satisfying SemVer version from candidate list",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "versions": {"type": "array"},
                                        "constraint": {"type": "string"}
                                    },
                                    "required": ["versions", "constraint"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                call_name = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if call_name == "satisfies":
                    res = {"satisfies": SemVerDependencyResolver.satisfies(args.get("version", ""), args.get("constraint", ""))}
                elif call_name == "resolve_best_version":
                    res = {"best_version": SemVerDependencyResolver.resolve_best_version(args.get("versions", []), args.get("constraint", ""))}
                else:
                    res = {"error": "Unknown tool"}
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
