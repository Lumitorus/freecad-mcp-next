# Security

The FreeCAD RPC service executes commands inside FreeCAD and must be treated as a
local privileged interface.

- Keep remote connections disabled unless they are explicitly required.
- Bind to localhost and allow only `127.0.0.1` for normal desktop use.
- Never expose port `9875` directly to the public internet.
- Review prompts and generated Python before allowing arbitrary code execution.

Report vulnerabilities privately to the repository owner after the GitHub repository
is created. Do not include secrets or private CAD files in a public issue.

