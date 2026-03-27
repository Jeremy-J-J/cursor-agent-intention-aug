export const ANSI_RESET = '\u001b[0m';
export const ANSI_GRAY = '\u001b[90m';
export const ANSI_GREEN = '\u001b[32m';
export const ANSI_RED = '\u001b[31m';
export const ANSI_BLUE = '\u001b[34m';
export const ANSI_CYAN = '\u001b[36m';
export const ANSI_YELLOW = '\u001b[33m';

export const formatStatus = (text: string) => `${ANSI_CYAN}${text}${ANSI_RESET}`;
export const formatThinking = (text: string) => `${ANSI_GRAY}${text}${ANSI_RESET}`;
export const formatResponse = (text: string) => `${ANSI_GREEN}${text}${ANSI_RESET}`;
export const formatError = (text: string) => `${ANSI_RED}${text}${ANSI_RESET}`;
export const formatTools = (text: string) => `${ANSI_YELLOW}${text}${ANSI_RESET}`;
export const formatPlan = (text: string) => `${ANSI_GREEN}${text}${ANSI_RESET}`;
export const formatFileOperation = (text: string) => `${ANSI_BLUE}${text}${ANSI_RESET}`;
export const formatCommand = (text: string) => `${ANSI_GREEN}${text}${ANSI_RESET}`;