import json
import csv

# Load the JSON data from the file in the current directory
json_filename = 'instagram_profiles.json'

try:
    with open(json_filename, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    print(f"Data successfully loaded from {json_filename}")
except FileNotFoundError:
    print(f"Error: {json_filename} not found.")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_filename}.")
    exit()

# Initialize an empty list for the reformatted posts
reformatted_posts = []

# Access the recent_posts list
user_info = data.get('kaybykatrina', {})
recent_posts = user_info.get('recent_posts', [])

# Loop through each post and reformat
for idx, post in enumerate(recent_posts, start=1):
    new_post = {
        'post id': idx,  # Assign a unique post id
        'image_url': post.get('post_url', ''),
        'description': post.get('caption', ''),
        'video_url': post.get('video_url', '')
    }
    reformatted_posts.append(new_post)

# Write to CSV file
csv_filename = 'reformatted_posts.csv'
csv_columns = ['post id', 'image_url', 'description', 'video_url']

try:
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for post in reformatted_posts:
            writer.writerow(post)
    print(f"Data successfully written to {csv_filename}")
except IOError:
    print("I/O error while writing CSV file")

# Write to JSON file
output_json_filename = 'reformatted_posts.json'
with open(output_json_filename, 'w', encoding='utf-8') as jsonfile:
    json.dump(reformatted_posts, jsonfile, ensure_ascii=False, indent=4)
    print(f"Data successfully written to {output_json_filename}")
