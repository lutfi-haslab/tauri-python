import { invoke, InvokeOptions } from "@tauri-apps/api/core";

const PY_INVOKE_TAURI_CMD = "plugin:pytauri|pyfunc";
const PY_INVOKE_HEADER = "pyfunc";

type RawPyInvokeArgs = ArrayBuffer | Uint8Array;
type PyInvokeArgs = RawPyInvokeArgs | any;

/**
 * Invokes a Python function through the Tauri IPC mechanism.
 *
 * @param funcName - The name of the Python function to invoke.
 * @param body - The body to send to the Python function.
 * @param options - See {@link invoke} for more details.
 * @template T - The expected return type of the Python function.
 *
 *     ### NOTE
 *
 *     The following headers are reserved and you should not set them in the options:
 *         - `pyfunc`
 *         - `__PYTAURI*`
 *         - `PyTauri*`
 * @returns A promise resolving or rejecting to the backend response.
 */
export async function pyInvoke<T>(
  funcName: string,
  body?: PyInvokeArgs,
  options?: InvokeOptions
): Promise<T> {
  let bodyEncoded: RawPyInvokeArgs | undefined;

  if (
    body === undefined ||
    body instanceof ArrayBuffer ||
    body instanceof Uint8Array
  ) {
    bodyEncoded = body;
  } else {
    const bodyJson = JSON.stringify(body);
    bodyEncoded = new TextEncoder().encode(bodyJson);
  }

  const headers = new Headers(options?.headers);
  headers.set(PY_INVOKE_HEADER, funcName);

  // Perform the invoke call
  const result = await invoke(PY_INVOKE_TAURI_CMD, bodyEncoded, {
    ...options,
    headers,
  });

  // If the result is an ArrayBuffer or Uint8Array, decode it
  if (result instanceof ArrayBuffer || result instanceof Uint8Array) {
    const decoder = new TextDecoder("utf-8");
    const decodedString = decoder.decode(result as Uint8Array);
    try {
      return JSON.parse(decodedString) as T; // Assume it's JSON
    } catch {
      return decodedString as unknown as T; // Fallback to raw string
    }
  }

  // If already a primitive (string, number, etc.), return directly
  return result as T;
}