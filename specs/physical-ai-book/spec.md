# Specification: "The Physical AI Handbook"

This document provides the detailed specification for the content, structure, and technical implementation of "The Physical AI Handbook," based on the principles outlined in the project constitution.

---

## 1. Book Structure

The book will be organized into chapters, with each chapter containing a set of lessons. The initial release will focus on Chapter 1 to establish a strong foundation.

### Chapter 1: The Spark of Life - From Power to Pixels

This chapter is the "Hello, World!" of Physical AI. It guides the learner from a bare microcontroller to a simple, environmentally-aware system, establishing core skills and confidence.

*   **Lesson 1.1: Your First Circuit - Blinking an LED**
    *   **Description:** This lesson is the quintessential first step in hardware. Learners will assemble their very first circuit and write a simple program to make an LED blink. It's a small win that provides a massive confidence boost.
    *   **Learning Objectives:**
        *   Understand the basic components: microcontroller (Arduino/ESP32), breadboard, LED, resistor, jumper wires.
        *   Learn how to safely power the microcontroller.
        *   Write a basic program using the `setup()` and `loop()` functions.
        *   Control a digital output pin to turn an LED on and off.
        *   Understand the concept of a "delay" in program execution.

*   **Lesson 1.2: Sensing the World - Reading a Light Sensor**
    *   **Description:** After learning to create output (light), learners will now focus on input—sensing the ambient environment. They will wire a photoresistor and read its values, "seeing" the world through the eyes of their machine.
    *   **Learning Objectives:**
        *   Understand the function of a photoresistor and a voltage divider circuit.
        *   Learn to read analog input from a sensor.
        *   Use the Serial Monitor to print and visualize sensor data in real-time.
        *   Grasp the concept of mapping analog values to a specific range.

*   **Lesson 1.3: Creating a Reaction - The Automatic Night-Light**
    *   **Description:** This lesson closes the cyber-physical loop. Learners will combine the previous two lessons to create their first "smart" device: an automatic night-light that turns an LED on when the room gets dark.
    *   **Learning Objectives:**
        *   Use conditional logic (`if/else` statements) to make decisions in code.
        *   Integrate sensor input to control an actuator's output.
        *   Understand the structure of a complete, simple robotic system: sense -> think -> act.
        *   Debug a system where hardware and software interact.

---

## 2. Content Guidelines

These guidelines are derived directly from the "Brand Voice" and "Core Principles" sections of the constitution.

*   **Tone:** The writing must be encouraging, patient, and enthusiastic. It should feel like a knowledgeable friend is guiding the reader, not a dry textbook. Use "we" and "you" to create a collaborative feel.
*   **Style:**
    *   **Clarity and Brevity:** Use simple, direct sentences. Define technical terms immediately in simple language.
    *   **Visual First:** Every hardware step MUST be accompanied by a clear Fritzing-style diagram and, where possible, a high-quality photo of the real circuit. Use GIFs to show expected outcomes.
    *   **Action-Oriented:** Start sections with verbs. Lead with the goal (e.g., "Now, let's make the LED blink.").
*   **Instructional Approach (The "Build-First" Method):**
    1.  **State the Goal:** Begin each lesson by showing the final result (e.g., a GIF of the night-light).
    2.  **Build It:** Provide immediate, step-by-step instructions for assembling the circuit and writing the code.
    3.  **Run It:** Encourage the reader to upload the code and see it work. This provides instant gratification.
    4.  **Explain It:** After they've seen the result, break down *why* it works. Explain the new code functions and hardware components. This "just-in-time" theory is more effective as the learner has a working context.

---

## 3. Lesson Format

Every lesson markdown file must adhere to the following structure to ensure consistency and pedagogical effectiveness.

1.  **YAML Front Matter:** Metadata for Docusaurus (title, description, sidebar position).
2.  **Introduction Block:**
    *   `## What You'll Build`: A 1-2 sentence summary and a visual (GIF/image) of the completed project.
    *   `## What You'll Learn`: A bulleted list of key takeaways.
    *   `## Parts Needed`: A checklist of components with names, quantities, and ideally links to examples.
3.  **Hands-On Activity:**
    *   `### Step 1: Assemble the Circuit`: A Fritzing diagram and/or photo, with clear annotations.
    *   `### Step 2: Write the Code`: A complete code block with syntax highlighting.
    *   `### Step 3: Upload and Verify`: Instructions on how to compile, upload, and check that the project is working as expected.
4.  **Code & Concept Breakdown:**
    *   `## How It Works - The Code`: A block-by-block explanation of the new code introduced. Use line-highlighting in code blocks to draw attention.
    *   `## How It Works - The Concepts`: Brief explanations of any new electronics or programming principles.
5.  **Going Further (Exercises):**
    *   `## Challenges`: A section with 2-3 optional exercises that encourage the reader to modify and expand upon the lesson's project (e.g., "Can you make the LED fade in response to light levels?").

---

## 4. Docusaurus-Specific Requirements

The book will be built as a Docusaurus website. The following conventions must be followed.

*   **File Structure:**
    *   All content will reside in the `/docs` directory.
    *   Chapters will be top-level folders (e.g., `/docs/chapter-1`).
    *   Lessons will be markdown files within chapter folders (e.g., `/docs/chapter-1/lesson-1-1-blinking-an-led.md`). File names should be descriptive.
*   **Navigation and Sidebar:**
    *   Each chapter folder must contain a `_category_.json` file to define its title and position in the sidebar, ensuring proper ordering. Example:
        ```json
        {
          "label": "Chapter 1: The Spark of Life",
          "position": 1
        }
        ```
    *   The lesson files will be automatically picked up to generate the sidebar navigation.
*   **Markdown and MDX Formatting:**
    *   **Admonitions:** Use Docusaurus admonitions extensively to add context.
        *   `::note`: For general information.
        *   `::tip`: For helpful hints and best practices.
        *   `::warning`: For potential issues or things to watch out for (e.g., "Make sure the long leg of the LED is connected to the positive side").
        *   `::danger`: For critical safety warnings (e.g., "Never connect power and ground directly!").
    *   **Code Blocks:** All code blocks must specify the language (e.g., ` ```cpp ` for Arduino) and use line highlighting for explanations.
    *   **Custom Components:** Plan to create custom React components using MDX for reusable elements like the "Parts Needed" list to ensure consistent formatting.
