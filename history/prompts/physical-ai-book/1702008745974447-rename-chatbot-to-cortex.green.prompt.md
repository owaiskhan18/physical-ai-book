---
id: 1702008745974447
title: Rename Chatbot to "Cortex"
stage: green
date: 2025-12-07
surface: agent
model: claude-3
feature: physical-ai-book
branch: main
user: Owais
command: replace chatbot name with this --->   ''' Cortex '''
labels: ["chatbot", "branding", "ui-enhancement"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - handbook-site/src/components/FloatingChatbot/index.js
tests_yaml: |
  - Manual verification that the chatbot header displays "Cortex".
prompt_text: replace chatbot name with this --->   ''' Cortex '''
response_text: |
  I have successfully replaced the chatbot name with "Cortex".

  This completes the user's request. I will now create a PHR.
outcome: The chatbot's displayed name in the header has been successfully updated from "Archon" to "Cortex".
evaluation: The name change was directly implemented in the `FloatingChatbot/index.js` file as requested, ensuring the UI reflects the new name.
---