import gradio as gr
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import random

# --- Helper Functions ---
def parse_numbers(list_str: str):
    if not list_str or list_str.strip() == "":
        raise ValueError("Input list is empty. Please enter at least one number.")
    parts = list_str.split(",")
    numbers = []
    for p in parts:
        p = p.strip()
        if p == "": continue
        try:
            number = int(p)
        except ValueError:
            raise ValueError(f"'{p}' is not a valid integer.")
        numbers.append(number)
    if len(numbers) == 0:
        raise ValueError("No valid numbers found. Please enter integers separated by commas.")
    return numbers

def generate_test_array(case: str, size=12):
    if case == "Best Case (Sorted)":
        return list(range(1, size + 1))
    elif case == "Worst Case (Reverse Sorted)":
        return list(range(size, 0, -1))
    elif case == "Average Case (Random)":
        return random.sample(range(1, size * 2), size)
    else:
        return []

# Visualization
def make_bar_image(values, title, highlight_indices=None):
    if highlight_indices is None: highlight_indices = []
    colors = ['#C1CCD4'] * len(values)
    for idx in highlight_indices:
        if 0 <= idx < len(values):
            colors[idx] = '#4F8BF9'
    fig, ax = plt.subplots(figsize=(4, 2.5))
    ax.bar(range(len(values)), values, color=colors)
    ax.set_xticks(range(len(values)))
    ax.set_xticklabels([str(int(v)) for v in values])
    ax.set_ylabel("Value")
    ax.set_title(title)
    fig.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# --- Merge Sort Algorithm  ---
def merge(arr, low, mid, high, lines, visual_steps, depth):
    left_arr = arr[low:mid + 1]
    right_arr = arr[mid + 1:high + 1]
    i = j = 0; k = low
    indent = "  " * depth
    lines.append(f"{indent}Merge: {left_arr} and {right_arr}") 
    active_indices = list(range(low, high + 1))
    visual_steps.append((f"Merge Start: Combining [{low}-{mid}] and [{mid+1}-{high}]", arr.copy(), active_indices))
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]: 
            arr[k] = left_arr[i]
            lines.append(f"{indent}  -> take {left_arr[i]} from left")
            i += 1
        else: 
            arr[k] = right_arr[j]
            lines.append(f"{indent}  -> take {right_arr[j]} from right")
            j += 1
        k += 1
    while i < len(left_arr): 
        arr[k] = left_arr[i]
        lines.append(f"{indent}  -> append remaining {left_arr[i]} from left")
        i += 1; k += 1
    while j < len(right_arr): 
        arr[k] = right_arr[j]
        lines.append(f"{indent}  -> append remaining {right_arr[j]} from right")
        j += 1; k += 1
    lines.append(f"{indent}Result of segment [{low}-{high}]: {arr[low:high+1]}")
    visual_steps.append((f"Merge Complete: Segment [{low}-{high}] is sorted", arr.copy(), active_indices))

def merge_sort_trace(arr, low, high, lines, visual_steps, depth=0):
    indent = "  " * depth
    if low >= high:
        lines.append(f"{indent}Base case: List element at index {low} is sorted: {arr[low]}")
        visual_steps.append((f"Base Case: Element at index {low}", arr.copy(), [low]))
        return
    mid = (low + high) // 2
    lines.append(f"{indent}Call merge_sort on segment [{low}-{high}]: {arr[low:high+1]}")
    visual_steps.append((f"Splitting: Active Segment [{low}-{high}]", arr.copy(), list(range(low, high + 1))))
    lines.append(f"{indent}Split Left: Recurse on [{low}-{mid}]")
    merge_sort_trace(arr, low, mid, lines, visual_steps, depth + 1)
    lines.append(f"{indent}Split Right: Recurse on [{mid+1}-{high}]")
    merge_sort_trace(arr, mid + 1, high, lines, visual_steps, depth + 1)
    merge(arr, low, mid, high, lines, visual_steps, depth)


def run_merge_sort(custom_list_str: str, case_selection: str, show_steps: bool):
    if case_selection == "Define Custom Array":
        try: numbers = parse_numbers(custom_list_str)
        except ValueError as e: return f"❌ Input error: {e}", "", ""
    else: numbers = generate_test_array(case_selection)

    if not numbers: return "⚠️ Please define a custom list or select a test case.", "", ""
        
    full_arr = numbers.copy(); lines = []; visual_steps = []
    visual_steps.append(("Start: Unsorted Array", full_arr.copy(), list(range(len(full_arr)))))
    merge_sort_trace(full_arr, 0, len(full_arr) - 1, lines, visual_steps, depth=0)
    sorted_list = full_arr
    
    summary_lines = [f"✅ Merge Sort completed.", f"Input type: **{case_selection}**", f"Original list: {numbers}", f"Sorted list (ascending): {sorted_list}"]
    summary = "\n".join(summary_lines)
    
    # Generate the teaching view trace
    teaching_view = "\n".join(lines)
        
    images = []
    for idx, (label, state, highlights) in enumerate(visual_steps, start=1):
        title = f"Step {idx}: {label}" 
        img = make_bar_image(state, title, highlights)
        images.append(img)
        
    return summary, teaching_view, images

# --- CUSTOM THEME DEFINITION ---

custom_theme = gr.themes.Soft(
    primary_hue="blue",  
    secondary_hue="gray",
).set(
    body_background_fill="#E0FFFF", 
    block_background_fill="#FFFFFF", 
    button_primary_background_fill="#228B22", 
    button_primary_background_fill_hover="#1F7A1F", 
    button_primary_text_color="white", 
    color_accent_soft="#228B22",
)

# --- Gradio Interface Setup ---

with gr.Blocks(title="Merge Sort Visualizer") as demo: 
    gr.Markdown("## 📊 Recursive Merge Sort Visualizer")
    
    # Define outputs
    summary_output = gr.Textbox(label="Summary and Test Case Results", lines=10)
    # Set visible=True by default to match the checkbox's initial value
    teaching_view_output = gr.Textbox(label="Teaching View: Merge Sort Steps", lines=20, visible=True) 
    gallery_output = gr.Gallery(
        label="Visual Merge Sort (Click through the steps below!)",
        columns=1, 
        rows=1,
        height='auto',
        preview=False
    )
    
    with gr.Row():
        # Column 1: Visualization (Left Side)
        with gr.Column(scale=2):
            gr.Markdown("### Visualization Trace (Step-by-Step)")
            gallery_output 
            
        # Column 2: Inputs and Text Outputs (Right Side)
        with gr.Column(scale=1):
            gr.Markdown("### Controls and Results")
            
            # Input Controls
            case_selection_input = gr.Radio(
                ["Best Case (Sorted)", "Worst Case (Reverse Sorted)", "Average Case (Random)", "Define Custom Array"],
                label="1. Select Input Array Type",
                value="Average Case (Random)",
            )
            custom_list_input = gr.Textbox(
                label="2. Custom Array Input (e.g. 5, 2, 4, 7, 1, 3)",
                placeholder="Enter numbers separated by commas",
                lines=1,
            )
            show_steps_checkbox = gr.Checkbox(
                label="3. Show detailed console-like trace in Teaching View",
                value=True,
            )
            
            # Action Button
            run_button = gr.Button("▶️ Run Merge Sort and Visualize")
            
            gr.Markdown("---")
            
            # Outputs
            summary_output 
            teaching_view_output 
            
            # Ensure the checkbox controls the visibility of the teaching view
            def update_teaching_view_visibility(checked):
                return gr.update(visible=checked)

            show_steps_checkbox.change(
                update_teaching_view_visibility, 
                [show_steps_checkbox],
                [teaching_view_output]
            )

            # Define the interaction flow
            run_button.click(
                fn=run_merge_sort,
                inputs=[custom_list_input, case_selection_input, show_steps_checkbox],
                outputs=[summary_output, teaching_view_output, gallery_output]
            )

if __name__ == "__main__":
    demo.launch(theme=custom_theme)
