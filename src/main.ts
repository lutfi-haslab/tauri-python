import { message } from '@tauri-apps/plugin-dialog';
import { Channel } from "@tauri-apps/api/core";
import { pyInvoke } from './lib/tauri-plugin';

// DOM elements
let greetInputEl: HTMLInputElement | null;
let greetMsgEl: HTMLElement | null;

export interface Person {
  name: string;
}

export interface Greeting {
  message: string;
}

export async function greet(body: Person): Promise<Greeting> {
  const response = await pyInvoke<{ message: string }>("greet", body);
  
  console.log(response.message); // Should work if Python returns { "message": "..." }
  return { message: response.message };
}


async function handleGreet() {
  if (!greetInputEl || !greetMsgEl) return;

  try {
    // Call Python command with proper typing
    const response = await greet({ name: greetInputEl.value });

    // Update UI and show message
    greetMsgEl.textContent = response.message;
    await message(response.message, "Greeting");
  } catch (error) {
    console.error("Greet error:", error);
    await message("Failed to greet", "Error");
  }
}

async function setupTimer() {
  const timeLabel = document.querySelector("#time-label");
  if (!timeLabel) return;

  try {
    // Create a new Channel instance
    const timeChannel = new Channel<{ time: string }>();
    
    // Setup message handler
    timeChannel.onmessage = (timeData) => {
      console.log("Received time:", timeData);
      if (timeData && timeData.time) {
        timeLabel.textContent = timeData.time;
      }
    };

    console.log("Sending channel to Python...");
    await pyInvoke("start_timer", timeChannel);
    console.log("Timer started successfully");
  } catch (error) {
    console.error("Failed to start timer:", error);
    timeLabel.textContent = "Timer error: " + String(error);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  // Initialize elements
  greetInputEl = document.querySelector("#greet-input");
  greetMsgEl = document.querySelector("#greet-msg");

  // Setup form submission
  document.querySelector("#greet-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    handleGreet();
  });

  // Start timer
  setupTimer();
});