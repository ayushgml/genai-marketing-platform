import instaloader
import os
import json
import re
from concurrent.futures import ThreadPoolExecutor

# Create an instance of Instaloader
L = instaloader.Instaloader()

# List of Instagram usernames you want to scrape
usernames = ['benefitcosmetics', 'maccosmetics', 'narsissist', 'toofaced', 'milkmakeup', 'smashboxcosmetics', 'covergirl', 'lauramercier', 'stilacosmetics', 'kikomilano']

# Function to scrape and save profile data
def scrape_profile(username):
    profile = instaloader.Profile.from_username(L.context, username)

    # Create a directory for saving the profile data
    save_path = os.path.join('insta-scraped', username)
    os.makedirs(save_path, exist_ok=True)

    post_number = 1  # Initialize post number

    posts_data = []  # List to store posts data

    for post in profile.get_posts():
        # Initialize data dictionary for the post
        post_data = {}

        post_data['username'] = username
        post_data['post_number'] = post_number

        # Get list of image URLs
        image_urls = []

        if post.typename == 'GraphSidecar':
            # Post with multiple images
            for node in post.get_sidecar_nodes():
                image_urls.append(node.display_url)
        else:
            # Single image or video
            image_urls.append(post.url)

        # Primary image URL is the first one
        post_data['primary_image_url'] = image_urls[0] if image_urls else None
        # Secondary image URLs are the remaining ones
        post_data['secondary_image_urls'] = image_urls[1:] if len(image_urls) > 1 else []

        # Caption
        post_data['caption'] = post.caption or ''

        # Extract hashtags from caption
        hashtags = re.findall(r'#\w+', post_data['caption'])
        post_data['hashtags'] = hashtags

        # Append post data to list
        posts_data.append(post_data)

        post_number += 1

    # Save posts data to a JSON file
    with open(os.path.join(save_path, f'{username}_posts.json'), 'w', encoding='utf-8') as f:
        json.dump(posts_data, f, ensure_ascii=False, indent=4)

    print(f'Scraping for {username} completed and saved in {save_path}')

# Use ThreadPoolExecutor for concurrent scraping
def scrape_all_profiles_concurrently(usernames):
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(scrape_profile, usernames)

# Start scraping all profiles concurrently
if __name__ == '__main__':
    print(f'Starting to scrape {len(usernames)} profiles...')
    scrape_all_profiles_concurrently(usernames)
    print('Scraping completed!')
