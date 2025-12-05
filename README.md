# CISC121-MergeSortProject
Hugging Face (Python) App for Merge Sort Visualization

Demo (Insert your GIF, screenshot, or short demo video here): https://www.youtube.com/watch?v=Fve5pBzABiQ

Hugging Face App: madisonmac789/MergeSortVisualization

Problem Breakdown & Computational Thinking

Algorithm Choice – Why Merge Sort? 

I chose Merge Sort because: 
It is a divide-and-conquer algorithm that always runs in O(n log n) time, no matter what the input looks like (best, average, or worst case). 
It has a very structured sequence: split → sort → merge, which makes it ideal for teaching and visualization.

Computational Thinking

1. Decomposition
    
To understand and implement Merge Sort, I broke the process into these smaller steps:
Take an input array (custom or auto-generated).
If the segment only has one element → this is the base case.
Split the array into a left half and a right half.
Recursively sort the left half.
Recursively sort the right half.
Merge the two sorted halves:
Compare the front elements of each half.
Place the smaller value first.
Continue until both halves are empty.
After each action, record: the current segment being worked on, whether the algorithm is splitting or merging, which indices are highlighted, the updated list for the next animation frame.
Repeat until the final fully sorted array is complete.

2. Pattern Recognition
  
   Merge Sort repeats the same structure over and over:
   Every segment is divided into two halves. Every division eventually reaches a base case of one element.
   Every merge step follows the same pattern: Compare left vs right. Insert the smaller. Move forward in that half.
   The recursion depth forms a balanced binary tree, which is why the time complexity is always O(n log n).

4. Abstraction 
    The user does not see the complicated internal work happening behind the scenes.
   The app hides:
   - Python’s recursive call stack.
   - Index tracking and boundary calculations.
   - Temporary left/right arrays created during merging.
   - All Gradio layout and update logic.
   - Matplotlib and PIL image generation steps.
   Instead, the user sees simplified, helpful visuals:
   - Clear bar-chart animations for each step.
   - Color-highlighted active segments. Labels explaining split and merge operations.
   - A “Teaching View” text explanation for every recursion event.
   - A final summary showing both the input and the sorted output.
   - This makes the experience educational while avoiding confusion.

Algorithm Design Input Options

Best Case (already sorted)
Worst Case (reverse sorted)
Average Case (random)
Custom input (e.g., 5, 2, 7, 1, 3) Processing Steps
The algorithm checks if the current segment size is 1 → if yes, return it as sorted.
Calculate the midpoint: mid = (low + high) // 2
Recursively call merge sort on the left half [low, mid].
Recursively call merge sort on the right half [mid+1, high].
Merge both halves: Compare the first elements of each half. Insert the smaller value into the new list.
Continue until both halves are empty.
At each stage, the app: Records the state, Generates a bar-chart image, Highlights active sections, Logs a text explanation.

Output

A complete gallery of animated steps
A textual breakdown of every recursive call and merge
The final sorted list

Flowchart: Start ↓ Input array (custom or generated) ↓ If segment size = 1 → Base Case ↓ Split array into Left and Right ↓ Recursively sort Left ↓ Recursively sort Right ↓ Merge Left and Right ↓ Record step + generate visualization ↓ If entire array merged → Done ↓ Output sorted array + all visualization steps

Steps to Run

Choose Your Input Type, select one: Best Case – sorted numbers (easiest pattern) Worst Case – reverse sorted (hardest pattern) Average Case – random values Custom – type your own list (example: 5, 2, 4, 7, 1, 3) If using Custom, enter your numbers separated by commas.

Click “Run Merge Sort and Visualize” When you press the button: The program reads your input. The Merge Sort algorithm begins. Each step of the algorithm is captured as an image.

Watch the Bar-Chart Animations Shows: The array splitting into smaller pieces Each segment being sorted The merging of values into the correct order Bars may change color to show active regions.

Read the Teaching Explanation: A text breakdown of what the algorithm is doing Messages such as: “Splitting array…” “Merging left and right segments…” “Comparing values…” “Base case reached…” This helps you learn exactly how the algorithm works (step by step).

View All Steps in the Gallery: A gallery appears showing: Every step of the algorithm All split and merge stages The complete visual history You can scroll through and study each part of the process.

Final Output The original array The fully sorted array Total number of steps recorded This completes the simulation.

Testing & Verification The program was tested thoroughly with: Small arrays (2–5 elements) Large arrays (20+ elements) Sorted inputs Reverse-sorted inputs Random inputs Duplicate values Invalid inputs (error messages shown correctly) All tests produced correct sorting results and stable visual output (see demo).

Author & Acknowledgment Created by Madison MacRury CISC-121 Project — 2025 Tools used: Python, Gradio, Matplotlib, Pillow
