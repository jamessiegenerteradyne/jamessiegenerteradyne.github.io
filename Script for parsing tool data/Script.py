import pandas as pd
import json

# Read Excel file
df = pd.read_excel("teradynetools.xlsx")


# Initialize the JSON data structure
data = []

# Group by Platform
duplicated_rows = []
for index, row in df.iterrows():
    if row['Platform'] == "UltraFLEX Family":
        row["Platform"] = "UltraFLEX, UltraFLEX Plus"
    categories = row['Platform'].split(',')
    for category in categories:
        duplicated_row = row.copy()
        duplicated_row['Platform'] = category.strip()
        duplicated_rows.append(duplicated_row)
platforms = []
df = pd.DataFrame(duplicated_rows)

grouped_platform = df.groupby('Platform')
# Iterate over platform groups
for platform, platform_group in grouped_platform:
    platform_split = platform.split(',')
    platforms.append(platform_split)
    for p in platform_split:
        platform_data = {
            "name": p.strip(),
            "children": []
        }

        # Group by Phase
        grouped_phase = platform_group.groupby('Phase')

        # Iterate over phase groups
        for phase, phase_group in grouped_phase:
            phase_data = {
                "name": phase,
                "children": []
            }

            # Group by Tool
            grouped_tool = phase_group.groupby('Tool')

            for tool, tool_group in grouped_tool:
                tool_data = {
                    "name": tool,
                    "description": "",
                    "clicked": "false"
                }
                if(type(tool_group.iloc[0,3]) == float):
                    tool_data['description'] = "No Description"
                else:
                    tool_data['description'] = tool_group.iloc[0,3].strip()
                # Append tool data under phase data
                phase_data['children'].append(tool_data)

            # Append phase data under platform data
            platform_data['children'].append(phase_data)

        # Append platform data to the main data structure
        data.append(platform_data)

# Convert to JSON
json_data = json.dumps(data, indent=2)
with open('json', 'w') as file:
    file.write("{\"name\": \"Platform\", \"children\":")
    file.write(json_data)
    file.write("}")
